# -*-coding:utf-8-*-

from odoo import models, fields, api
from odoo.osv import expression

class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):

        # Trick to fix this part on Ir.attachment model
        # if not any(arg[0] in ('id', 'res_field') for arg in args):
        #    args.insert(0, ('res_field', '=', False))

        if not any(arg[0] in ('id', 'res_field') for arg in args):
            override_domain = ['|',('res_field', '=', False),('res_field', '!=', False)]
            args = expression.AND([args, override_domain])

        return super(IrAttachment, self).search(
            args, offset=offset, limit=limit, order=order, count=count)