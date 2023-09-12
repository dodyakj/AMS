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

    @http.route(['/aircraft_image/<model("aircraft.acquisition"):aircraft>/image.jpeg'], type='http', auth="public", website=True, csrf=False)
    def get_aircraft(self,aircraft):
        # res = super(AmsDashboard, self).get_aircraft(aircraft)
        res = request.env['aircraft.acquisition'].sudo().search([('id','=',aircraft.id)],limit=1)
        # res = aircraft
        if(res.image):
            return Response(base64.decodestring(res.image),content_type='image/jpeg',status=200)
        else:
            return Response('',content_type='text',status=500)