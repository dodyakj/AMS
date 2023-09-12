odoo.define("search_table_widget.DataTable", function (require) {
  "use strict";

  var ControlPanel = require("web.ControlPanel");
  var core = require("web.core");
  var data = require("web.data");
  var common = require("web.form_common");
  var ListView = require("web.ListView");
  require("web.ListEditor");
  var utils = require("web.utils");
  var ViewManager = require("web.ViewManager");

  var _t = core._t;
  var COMMANDS = common.commands;
  var list_widget_registry = core.list_widget_registry;

  var AbstractManyField = common.AbstractField.extend({
    init: function (field_manager, node) {
      var self = this;
      this._super(field_manager, node);
      this.dataset = new X2ManyDataSet(
        this,
        this.field.relation,
        this.build_context()
      );
      this.dataset.x2m = this;
      this.dataset.parent_view = this.view;
      this.dataset.child_name = this.name;
      this.set("value", []);
      this.starting_ids = [];
      this.mutex = new utils.Mutex();
      this.view.on("load_record", this, this._on_load_record);
      this.dataset.on("dataset_changed", this, function () {
        var options = _.clone(_.last(arguments));
        if (!_.isObject(options) || _.isArray(options)) {
          options = {};
        }
        if (
          !self.internal_dataset_changed &&
          !options.internal_dataset_changed
        ) {
          self.trigger("change:commands", options);
        }
      });
      this.on("change:commands", this, function (options) {
        self._inhibit_on_change_flag = !!options._inhibit_on_change_flag;
        self.set({
          value: self.dataset.ids.slice()
        });
        self._inhibit_on_change_flag = false;
      });
    },

    set_value_from_record: function (record) {
      this._super.apply(this, arguments);
      this.starting_ids = [];
      if (
        record.id &&
        record[this.name] &&
        (!isNaN(record.id) ||
          record.id.indexOf(this.dataset.virtual_id_prefix) === -1)
      ) {
        this.starting_ids = this.get("value").slice();
      }
    },

    _on_load_record: function (record) {
      this.trigger("load_record", record);
    },

    set_value: function (ids) {
      ids = (ids || []).slice();
      if (
        _.find(ids, function (id) {
          return typeof id === "string";
        })
      ) {
        throw new Error(
          "set_value of '" +
          this.name +
          "' must receive an list of ids without virtual ids.",
          ids
        );
      }
      if (
        _.find(ids, function (id) {
          return typeof id !== "number";
        })
      ) {
        return this.send_commands(ids, {
          _inhibit_on_change_flag: this._inhibit_on_change_flag
        });
      }
      this.dataset.reset_ids(ids);
      return $.when(this._super(ids));
    },

    internal_set_value: function (ids) {
      if (_.isEqual(ids, this.get("value"))) {
        return;
      }
      var tmp = this.no_rerender;
      this.no_rerender = true;
      var def = this.data_replace(ids.slice());
      this.no_rerender = tmp;
      return def;
    },

    commit_value: function () {
      return this.mutex.def;
    },

    data_create: function (data, options) {
      return this.send_commands([COMMANDS.create(data)], options);
    },

    data_update: function (id, data, options) {
      return this.send_commands([COMMANDS.update(id, data)], options);
    },

    data_link: function (id, options) {
      return this.send_commands([COMMANDS.link_to(id)], options);
    },

    data_link_multi: function (ids, options) {
      return this.send_commands(
        _.map(ids, function (id) {
          return COMMANDS.link_to(id);
        }),
        options
      );
    },

    data_delete: function (id) {
      return this.send_commands([COMMANDS.delete(id)]);
    },

    data_forget: function (id) {
      return this.send_commands([COMMANDS.forget(id)]);
    },

    data_replace: function (ids, options) {
      return this.send_commands([COMMANDS.replace_with(ids)], options);
    },

    data_read: function (ids, fields, options) {
      return this.dataset.read_ids(ids, fields, options);
    },

    send_commands: function (command_list, options) {
      var self = this;
      var def = $.Deferred();
      var dataset = this.dataset;
      var res = true;
      options = options || {};
      var internal_options = _.extend({}, options, {
        internal_dataset_changed: true
      });

      _.each(command_list, function (command) {
        self.mutex.exec(function () {
          var id = command[1];
          switch (command[0]) {
            case COMMANDS.CREATE:
              var data = _.clone(command[2]);
              delete data.id;
              return dataset.create(data, internal_options).then(function (id) {
                dataset.ids.push(id);
                res = id;
              });
            case COMMANDS.UPDATE:
              return dataset
                .write(id, command[2], internal_options)
                .then(function () {
                  if (dataset.ids.indexOf(id) === -1) {
                    dataset.ids.push(id);
                    res = id;
                  }
                });
            case COMMANDS.FORGET:
              return dataset.unlink([id]);
            case COMMANDS.DELETE:
              return dataset.unlink([id]);
            case COMMANDS.LINK_TO:
              if (dataset.ids.indexOf(id) === -1) {
                return dataset.add_ids([id], internal_options);
              }
              return;
            case COMMANDS.DELETE_ALL:
              return dataset.reset_ids([], {
                keep_read_data: true
              });
            case COMMANDS.REPLACE_WITH:
              dataset.ids = [];
              return dataset.alter_ids(command[2], internal_options);
            default:
              throw new Error(
                "send_commands to '" +
                self.name +
                "' receive a non command value." +
                "\n" +
                JSON.stringify(command_list)
              );
          }
        });
      });

      this.mutex.def.then(function () {
        self.trigger("change:commands", options);
        def.resolve(res);
      });
      return def;
    },

    get_value: function () {
      var self = this,
        is_one2many = this.field.type === "one2many",
        not_delete = this.options.not_delete,
        starting_ids = this.starting_ids.slice(),
        replace_with_ids = [],
        add_ids = [],
        command_list = [],
        id,
        index,
        record;

      _.each(this.get("value"), function (id) {
        index = starting_ids.indexOf(id);
        if (index !== -1) {
          starting_ids.splice(index, 1);
        }
        var record = self.dataset.get_cache(id);
        if (!_.isEmpty(record.changes)) {
          var values = _.clone(record.changes);
          // format many2one values
          for (var k in values) {
            if (
              values[k] instanceof Array &&
              values[k].length === 2 &&
              typeof values[k][0] === "number" &&
              typeof values[k][1] === "string"
            ) {
              values[k] = values[k][0];
            }
          }
          if (record.to_create) {
            command_list.push(COMMANDS.create(values));
          } else {
            command_list.push(COMMANDS.update(record.id, values));
          }
          return;
        }
        if (!is_one2many || not_delete || self.dataset.delete_all) {
          replace_with_ids.push(id);
        } else {
          command_list.push(COMMANDS.link_to(id));
        }
      });
      if (
        (!is_one2many || not_delete || self.dataset.delete_all) &&
        (replace_with_ids.length || starting_ids.length)
      ) {
        _.each(command_list, function (command) {
          if (command[0] === COMMANDS.UPDATE) {
            replace_with_ids.push(command[1]);
          }
        });
        command_list.unshift(COMMANDS.replace_with(replace_with_ids));
      }

      _.each(starting_ids, function (id) {
        if (is_one2many && !not_delete) {
          command_list.push(COMMANDS.delete(id));
        } else if (is_one2many && !self.dataset.delete_all) {
          command_list.push(COMMANDS.forget(id));
        }
      });

      return command_list;
    },

    is_valid: function () {
      return this.mutex.def.state() === "resolved" && this._super();
    },

    is_false: function () {
      return _(this.get("value")).isEmpty();
    },

    destroy: function () {
      this.view.off("load_record", this, this._on_load_record);
      this._super();
    }
  });

  var FieldX2Many = AbstractManyField.extend({
    multi_selection: false,
    disable_utility_classes: true,
    x2many_views: {},
    view_options: {},
    default_view: "tree",
    init: function (field_manager, node) {
      this._super(field_manager, node);

      this.is_loaded = $.Deferred();
      this.initial_is_loaded = this.is_loaded;
      this.is_started = false;
      this.set_value([]);
    },
    start: function () {
      this._super.apply(this, arguments);
      var self = this;

      this.load_views();
      var destroy = function () {
        self.is_loaded = self.is_loaded.then(function () {
          self.renderElement();
          self.viewmanager.destroy();
          return $.when(self.load_views()).done(function () {
            self.reload_current_view();
          });
        });
      };
      this.is_loaded.done(function () {
        self.on("change:effective_readonly", self, destroy);
      });
      this.view.on("on_button_cancel", this, destroy);
      this.is_started = true;
      this.reload_current_view();
    },
    load_views: function () {
      var self = this;

      var view_types = this.node.attrs.mode;
      view_types = !!view_types ? view_types.split(",") : [this.default_view];
      var views = [];
      _.each(view_types, function (view_type) {
        if (!_.include(["list", "tree", "graph", "kanban"], view_type)) {
          throw new Error(
            _.str.sprintf(
              _t("View type '%s' is not supported in X2Many."),
              view_type
            )
          );
        }
        var view = {
          view_id: false,
          view_type: view_type === "tree" ? "list" : view_type,
          fields_view: self.field.views && self.field.views[view_type],
          options: {}
        };
        if (view.view_type === "list") {
          _.extend(view.options, {
            action_buttons: false,
            addable: null,
            selectable: self.multi_selection,
            sortable: true,
            import_enabled: false,
            deletable: true
          });
          if (self.get("effective_readonly")) {
            _.extend(view.options, {
              deletable: null,
              reorderable: false
            });
          }
        } else if (view.view_type === "kanban") {
          _.extend(view.options, {
            action_buttons: true,
            confirm_on_delete: false
          });
          if (self.get("effective_readonly")) {
            _.extend(view.options, {
              action_buttons: false,
              quick_creatable: false,
              creatable: false,
              read_only_mode: true
            });
          }
        }
        views.push(view);
      });
      this.views = views;

      this.viewmanager = new X2ManyViewManager(
        this,
        this.dataset,
        views,
        this.view_options,
        this.x2many_views
      );
      this.viewmanager.x2m = self;
      var def = $.Deferred().done(function () {
        self.initial_is_loaded.resolve();
      });
      this.viewmanager.on("controller_inited", self, function (
        view_type,
        controller
      ) {
        controller.x2m = self;
        if (view_type == "list") {
          if (self.get("effective_readonly")) {
            controller.on("edit:before", self, function (e) {
              e.cancel = true;
            });
            _(controller.columns).find(function (column) {
              if (
                !(column instanceof list_widget_registry.get("field.handle"))
              ) {
                return false;
              }
              column.modifiers.invisible = true;
              return true;
            });
          }
        } else if (view_type == "graph") {
          self.reload_current_view();
        }
        def.resolve();
      });
      this.viewmanager.on("switch_mode", self, function (n_mode) {
        $.when(self.commit_value()).done(function () {
          if (n_mode === "list") {
            utils.async_when().done(function () {
              self.reload_current_view();
            });
          }
        });
      });
      utils.async_when().done(function () {
        self.$el.addClass("o_view_manager_content");
        self.alive(self.viewmanager.attachTo(self.$el));
      });
      return def;
    },
    reload_current_view: function () {
      var self = this;
      self.is_loaded = self.is_loaded.then(function () {
        var view = self.get_active_view();
        if (view.type === "list") {
          view.controller.current_min = 1;
          return view.controller.reload_content();
        } else if (view.controller.do_search) {
          return view.controller.do_search(
            self.build_domain(),
            self.dataset.get_context(),
            []
          );
        }
      }, undefined);
      return self.is_loaded;
    },
    get_active_view: function () {
      return this.viewmanager && this.viewmanager.active_view;
    },
    set_value: function (value_) {
      var self = this;
      this._super(value_).then(function () {
        if (self.is_started && !self.no_rerender) {
          return self.reload_current_view();
        }
      });
    },
    commit_value: function () {
      var view = this.get_active_view();
      if (view && view.type === "list" && view.controller.__focus) {
        return $.when(this.mutex.def, view.controller._on_blur_one2many());
      }
      return this.mutex.def;
    },
    is_syntax_valid: function () {
      var view = this.get_active_view();
      if (!view) {
        return true;
      }
      switch (this.viewmanager.active_view.type) {
        case "form":
          return _(view.controller.fields)
            .chain()
            .invoke("is_valid")
            .all(_.identity)
            .value();
        case "list":
          return view.controller.is_valid();
      }
      return true;
    },
    is_false: function () {
      return _(this.dataset.ids).isEmpty();
    },
    is_set: function () {
      return true;
    }
  });

  var X2ManyDataSet = data.BufferedDataSet.extend({
    get_context: function () {
      this.context = this.x2m.build_context();
      var self = this;
      _.each(arguments, function (context) {
        self.context.add(context);
      });
      return this.context;
    }
  });

  var X2ManyViewManager = ViewManager.extend({
    custom_events: {
      scrollTo: function () {}
    },
    init: function (parent, dataset, views, flags, x2many_views) {
      flags = _.extend({}, flags, {
        headless: false,
        search_view: false,
        action_buttons: true,
        pager: false,
        sidebar: false
      });
      this.control_panel = new ControlPanel(parent, "X2ManyControlPanel");
      this.set_cp_bus(this.control_panel.get_bus());
      this._super(parent, dataset, views, flags);
      this.registry = core.view_registry.extend(x2many_views);
    },
    start: function () {
      this.control_panel.prependTo(this.$el);
      return this._super();
    },
    switch_mode: function (mode, unused) {
      if (mode !== "form") {
        return this._super(mode, unused);
      }
      var self = this;
      var id =
        self.x2m.dataset.index !== null ?
        self.x2m.dataset.ids[self.x2m.dataset.index] :
        null;
      var pop = new common.FormViewDialog(this, {
        res_model: self.x2m.field.relation,
        res_id: id,
        context: self.x2m.build_context(),
        title: _t("Open: ") + self.x2m.string,
        create_function: function (data, options) {
          return self.x2m.data_create(data, options);
        },
        write_function: function (id, data, options) {
          return self.x2m.data_update(id, data, options).done(function () {
            self.x2m.reload_current_view();
          });
        },
        alternative_form_view: self.x2m.field.views ?
          self.x2m.field.views.form :
          undefined,
        parent_view: self.x2m.view,
        child_name: self.x2m.name,
        read_function: function (ids, fields, options) {
          return self.x2m.data_read(ids, fields, options);
        },
        form_view_options: {
          not_interactible_on_create: true
        },
        readonly: self.x2m.get("effective_readonly")
      }).open();
      pop.on("elements_selected", self, function () {
        self.x2m.reload_current_view();
      });
    }
  });

  var X2ManyListView = ListView.extend({
    is_valid: function () {
      if (!this.fields_view || !this.editable()) {
        return true;
      }
      if (_.isEmpty(this.records.records)) {
        return true;
      }
      var fields = this.editor.form.fields;
      var current_values = {};
      _.each(fields, function (field) {
        field._inhibit_on_change_flag = true;
        field.__no_rerender = field.no_rerender;
        field.no_rerender = true;
        current_values[field.name] = field.get("value");
      });
      var ids = _.map(this.records.records, function (item) {
        return item.attributes.id;
      });
      var cached_records = _.filter(this.dataset.cache, function (item) {
        return (
          _.contains(ids, item.id) && !_.isEmpty(item.values) && !item.to_delete
        );
      });
      var valid = _.every(cached_records, function (record) {
        _.each(fields, function (field) {
          var value = record.values[field.name];
          field._inhibit_on_change_flag = true;
          field.no_rerender = true;
          field.set_value(
            _.isArray(value) && _.isArray(value[0]) ?
            [COMMANDS.delete_all()].concat(value) :
            value
          );
        });
        return _.every(fields, function (field) {
          field.process_modifiers();
          field._check_css_flags();
          return field.is_valid();
        });
      });
      _.each(fields, function (field) {
        field.set("value", current_values[field.name], {
          silent: true
        });
        field._inhibit_on_change_flag = false;
        field.no_rerender = field.__no_rerender;
      });
      return valid;
    },
    render_pager: function ($node, options) {
      this._limit = this.dataset.size();
      options = _.extend(options || {}, {
        single_page_hidden: true
      });
      this._super($node, options);
    },
    display_nocontent_helper: function () {
      return false;
    }
  });

  var X2ManyList = ListView.List.extend({
    pad_table_to: function (count) {
      if (
        !this.view.is_action_enabled("create") ||
        this.view.x2m.get("effective_readonly")
      ) {
        this._super(count);
        return;
      }

      this._super(count > 0 ? count - 1 : 0);
      var self = this;
      var columns = _(this.columns).filter(function (column) {
        return column.invisible !== "1";
      }).length;
      if (this.options.selectable) {
        columns++;
      }
      if (this.options.deletable) {
        columns++;
      }

      var $cell = $("<td>", {
        // colspan: columns,
        class: "o_form_field_x2many_list_row_add"
      }).append(
        $("<a>", {
          href: "#"
        })
        .text(_t(" - Add an item - "))
        .click(function (e) {
          e.preventDefault();
          e.stopPropagation();
          var def;
          if (self.view.editable()) {
            if (self.view.editor.form.__blur_timeout) {
              clearTimeout(self.view.editor.form.__blur_timeout);
              self.view.editor.form.__blur_timeout = false;
            }
            def = self.view.save_edition();
          }
          $.when(def).done(self.view.do_add_record.bind(self));
        })
      );
      var $padding = this.$current.find("tr:not([data-id]):last");
      var $newrow = $("<tr>");
      if ($padding.length) {
        $cell.appendTo($newrow);
        for (let index = 0; index < columns; index++) {
          const $emptyCell = $("<td>", {
            class: "o_form_field_x2many_list_row_add"
          });
          $emptyCell.appendTo($newrow);
        }
        $padding.after($newrow);
      } else {
        $cell.appendTo($newrow);
        for (let index = 0; index < (columns - 1); index++) {
          const $emptyCell = $("<td>", {
            class: "o_form_field_x2many_list_row_add"
          });
          $emptyCell.appendTo($newrow);
        }
        this.$current.find("tr:first").before($newrow);
      }
    }
  });

  var One2ManyListView = X2ManyListView.extend({
    init: function () {
      this._super.apply(this, arguments);
      this.options = _.extend(this.options, {
        GroupsType: One2ManyGroups,
        ListType: X2ManyList
      });
      this.on("edit:after", this, this.proxy("_after_edit"));
      this.on("save:before cancel:before", this, this.proxy("_before_unedit"));

      core.bus.on("click", this, this._on_click_outside);

      this.dataset.on("dataset_changed", this, function () {
        this._dataset_changed = true;
        this.dataset.x2m._dirty_flag = true;
      });
      this.dataset.x2m.on("load_record", this, function () {
        this._dataset_changed = false;
      });

      this.on("warning", this, function (e) {
        if (this.editable()) {
          e.stop_propagation();
        }
      });
    },
    do_add_record: function () {
      if (this.editable()) {
        this._super.apply(this, arguments);
      } else {
        var self = this;
        new common.SelectCreateDialog(this, {
          res_model: self.x2m.field.relation,
          domain: self.x2m.build_domain(),
          context: self.x2m.build_context(),
          title: _t("Create: ") + self.x2m.string,
          initial_view: "form",
          alternative_form_view: self.x2m.field.views ?
            self.x2m.field.views.form :
            undefined,
          create_function: function (data, options) {
            return self.x2m.data_create(data, options);
          },
          read_function: function (ids, fields, options) {
            return self.x2m.data_read(ids, fields, options);
          },
          parent_view: self.x2m.view,
          child_name: self.x2m.name,
          form_view_options: {
            not_interactible_on_create: true
          },
          on_selected: function () {
            self.x2m.reload_current_view();
          }
        }).open();
      }
    },
    do_activate_record: function (index, id) {
      var self = this;
      new common.FormViewDialog(self, {
        res_model: self.x2m.field.relation,
        res_id: id,
        context: self.x2m.build_context(),
        title: _t("Open: ") + self.x2m.string,
        write_function: function (id, data, options) {
          return self.x2m.data_update(id, data, options).done(function () {
            self.x2m.reload_current_view();
          });
        },
        create_function: function (data, options) {
          return self.x2m.data_create(data, options).done(function () {
            self.x2m.reload_current_view();
          });
        },
        alternative_form_view: self.x2m.field.views ?
          self.x2m.field.views.form :
          undefined,
        parent_view: self.x2m.view,
        child_name: self.x2m.name,
        read_function: function (ids, fields, options) {
          return self.x2m.data_read(ids, fields, options);
        },
        form_view_options: {
          not_interactible_on_create: true
        },
        readonly:
          !this.is_action_enabled("edit") || self.x2m.get("effective_readonly")
      }).open();
    },
    do_button_action: function (name, id, callback) {
      if (!_.isNumber(id)) {
        this.do_warn(
          _t("Action Button"),
          _t("The o2m record must be saved before an action can be used")
        );
        return;
      }
      var parent_form = this.x2m.view;
      var self = this;
      this.save_edition()
        .then(function () {
          if (parent_form) {
            return parent_form.save();
          } else {
            return $.when();
          }
        })
        .done(function () {
          var ds = self.x2m.dataset;
          var changed_records = _.find(ds.cache, function (record) {
            return (
              record.to_create || record.to_delete || !_.isEmpty(record.changes)
            );
          });
          if (!self.x2m.options.reload_on_button && !changed_records) {
            self.handle_button(name, id, callback);
          } else {
            self.handle_button(name, id, function () {
              self.x2m.view.reload();
            });
          }
        });
    },
    start_edition: function (record, options) {
      if (!this.__focus) {
        this._on_focus_one2many();
      }
      return this._super(record, options);
    },
    reload_content: function () {
      var self = this;
      if (self.__focus) {
        self._on_blur_one2many();
        return this._super().then(function () {
          var record_being_edited = self.records.get(
            self.editor.form.datarecord.id
          );
          if (record_being_edited) {
            self.start_edition(record_being_edited);
          }
        });
      }
      return this._super().then(function () {
        if (!$.fn.DataTable.isDataTable(self.$("table"))) {
          self.$("table").css("width", "100%");
          self.$("table").DataTable({
            responsive: true,
            ordering: false,
            aLengthMenu: [
              [10, 25, 50, 100, 200, -1],
              [10, 25, 50, 100, 200, "All"]
            ],
            iDisplayLength: 10
          });
        }
      });
    },
    _on_focus_one2many: function () {
      if (!this.editor.is_editing()) {
        return;
      }
      this.dataset.x2m.internal_dataset_changed = true;
      this._dataset_changed = false;
      this.__focus = true;
    },
    _on_click_outside: function (e) {
      if (this.__ignore_blur || !this.editor.is_editing()) {
        return;
      }

      var $target = $(e.target);

      var click_outside =
        $target.closest(".ui-autocomplete,.btn,.modal-backdrop").length === 0;

      var $o2m = $target.closest(".o_list_editable");
      if ($o2m.length && $o2m[0] === this.el) {
        click_outside = false;
      }

      var $modal = $target.closest(".modal");
      if ($modal.length) {
        var $currentModal = this.$el.closest(".modal");
        if ($currentModal.length === 0 || $currentModal[0] !== $modal[0]) {
          click_outside = false;
        }
      }

      if (click_outside) {
        this._on_blur_one2many();
      }
    },
    _on_blur_one2many: function () {
      if (this.__ignore_blur) {
        return $.when();
      }

      this.__ignore_blur = true;
      this.__focus = false;
      this.dataset.x2m.internal_dataset_changed = false;

      var self = this;
      return this.save_edition(true)
        .done(function () {
          if (self._dataset_changed) {
            self.dataset.trigger("dataset_changed");
          }
        })
        .always(function () {
          self.__ignore_blur = false;
        });
    },
    _after_edit: function () {
      this.editor.form.on("blurred", this, this._on_blur_one2many);

      this.editor.form.widgetFocused();
    },
    _before_unedit: function () {
      this.editor.form.off("blurred", this, this._on_blur_one2many);
    },
    do_delete: function (ids) {
      var confirm = window.confirm;
      window.confirm = function () {
        return true;
      };
      try {
        return this._super(ids);
      } finally {
        window.confirm = confirm;
      }
    },
    reload_record: function (record, options) {
      if (!options || !options.do_not_evict) {
        this.dataset.evict_record(record.get("id"));
      }

      return this._super(record);
    }
  });

  var One2ManyGroups = ListView.Groups.extend({
    setup_resequence_rows: function () {
      if (!this.view.x2m.get("effective_readonly")) {
        this._super.apply(this, arguments);
      }
    }
  });

  var FieldOne2Many = FieldX2Many.extend({
    init: function () {
      this._super.apply(this, arguments);
      this.x2many_views = {
        kanban: core.view_registry.get("one2many_kanban"),
        list: One2ManyListView
      };
    },
    start: function () {
      this.$el.addClass("o_form_field_one2many");
      return this._super.apply(this, arguments);
    },
    commit_value: function () {
      var self = this;
      return this.is_loaded.then(function () {
        var view = self.viewmanager.active_view;
        if (view.type === "list" && view.controller.editable()) {
          return self.mutex.def.then(function () {
            return view.controller.save_edition();
          });
        }
        return self.mutex.def;
      });
    },
    is_false: function () {
      return false;
    }
  });

  core.form_widget_registry.add("datatable", FieldOne2Many);
});