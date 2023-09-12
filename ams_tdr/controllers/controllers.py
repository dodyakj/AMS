import logging
import pprint
import werkzeug
from werkzeug.wrappers import Response
import json
import base64

from odoo import http
from odoo.http import request
from datetime import datetime, timedelta, date

_logger = logging.getLogger(__name__)

class AmsDashboard(http.Controller):

    @http.route(['/mtr_state/<mtr>'], type='http', auth="public", website=True, csrf=False)
    def get_mtr(self,mtr):
        # res = super(AmsDashboard, self).get_mtr(mtr)
        # res = request.env['ams.mtr'].sudo().search([('id','=',mtr.id)],limit=1)
        # res = mtr
        cron = request.env['ir.cron'].search(['&',('model','=','ams.mtr'),'&',('function','=','process_data_part'),('args','=','['+str(mtr)+']')])
        if(cron.active == False):
            res = request.env['ams.mtr'].sudo().search([('id','=',mtr)],limit=1)
            ret = {'state' : res.data_status}
            return json.dumps(ret)
        else:
            ret = {'state' : False}
            return json.dumps(ret)
        # if(res.data_status):
        #     return Response('True',content_type='text',status=200)
        # else:
        #     return Response('False',content_type='text',status=500)