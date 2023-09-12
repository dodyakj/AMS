# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, HRMS Dashboard
#    Copyright (C) 2018 Hilar AK All Rights Reserved
#    https://www.linkedin.com/in/hilar-ak/
#    <hilarak@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import models, fields, api
from odoo.http import request
import datetime

class IASHelp(models.Model):
    _name = 'ams.help'
    _rec_name = "version"

    release_date = fields.Date(string="Release Date")
    version = fields.Char(string="Version")
    doc = fields.One2many('ams.help.doc','help_id')



class IASHelpDoc(models.Model):
    _name = 'ams.help.doc'

    name = fields.Char()
    cover = fields.Binary()
    file_cover = fields.Char()
    release_date = fields.Date(string="Release Date")
    version = fields.Char(string="Version")
    doc = fields.Binary(filename='name')
    help_id = fields.Many2one('ams.help')

class HrDashboard(models.Model):
    _name = 'ams.dashboard'
    _description = 'HR Dashboard'

    name = fields.Char("")

    @api.model
    def get_document(self):
        doc_id = self.env['ams.help'].sudo().search_read([], limit=1)
        cr = self.env.cr
        query = """ Select name,version,release_date,id,file_cover from ias_help_doc"""
        cr.execute(query)
        docs = cr.dictfetchall()
        if doc_id:
            data = {
                'release_date' : doc_id[0]['release_date'],
                'version' : doc_id[0]['version'],
                'doc' : docs
            }
            doc_id[0].update(data)

        print "++++++++++++"
        print doc_id
        print "++++++++++++"
        return doc_id
