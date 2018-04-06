# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

import base64
import functools
import json
import logging
import werkzeug.utils
import werkzeug.wrappers

from odoo import http
from odoo.addons.website.models.website import unslug
from odoo.addons.web.controllers.main import Binary

from odoo.tools.translate import _

from odoo.http import content_disposition, dispatch_rpc, request, \
    serialize_exception as _serialize_exception

_logger = logging.getLogger(__name__)

def serialize_exception(f):
    @functools.wraps(f)
    def wrap(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception, e:
            _logger.exception("An exception occured during an http request")
            se = _serialize_exception(e)
            error = {
                'code': 200,
                'message': "Odoo Server Error",
                'data': se
            }
            return werkzeug.exceptions.InternalServerError(json.dumps(error))
    return wrap

class Binary(http.Controller):

    @http.route('/web/binary/upload_field_attachment', type='http', auth="user")
    @serialize_exception
    def upload_field_attachment(self, callback, model, ufile, field_name, id=0):
        Model = request.env['ir.attachment']
        out = """<script language="javascript" type="text/javascript">
                        var win = window.top.window;
                        win.jQuery(win).trigger(%s, %s);
                    </script>"""
        try:
            attachment = Model.create({
                'name': ufile.filename,
                'datas': base64.encodestring(ufile.read()),
                'datas_fname': ufile.filename,
                'res_model': model,
                'res_id': id and int(id) or 0,
                'res_field': field_name,
            })
            args = {
                'filename': ufile.filename,
                'mimetype': ufile.content_type,
                'id': attachment.id
            }
        except Exception:
            args = {'error': _("Something horrible happened")}
            _logger.exception("Fail to upload attachment %s" % ufile.filename)
        return out % (json.dumps(callback), json.dumps(args))