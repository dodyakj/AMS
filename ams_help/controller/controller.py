
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

class ams_help_cover(http.Controller):

    @http.route(['/ams_help/<model("ams.help.doc"):manual>/image.jpeg'], type='http', auth="public", website=True, csrf=False)
    def get_manual(self,manual):
        # res = super(AmsDashboard, self).get_manual(manual)
        # res = request.env['manual.acquisition'].sudo().search([('id','=',manual.id)],limit=1)
        # res = manual
        if(manual.cover):
            return Response(base64.decodestring(manual.cover),content_type='image/jpeg',status=200)
        else:
            return Response('',content_type='text',status=500)
class ams_help_doc(http.Controller):

    @http.route(['/ams_help/<model("ams.help.doc"):doc>/doc.pdf'], type='http', auth="public", website=True, csrf=False)
    def get_doc(self,doc):
        # res = super(AmsDashboard, self).get_doc(doc)
        # res = request.env['doc.acquisition'].sudo().search([('id','=',doc.id)],limit=1)
        # res = doc
        if(doc.doc):
            return Response(base64.decodestring(doc.doc),content_type='application/pdf',status=200)
        else:
            return Response('',content_type='text',status=500)