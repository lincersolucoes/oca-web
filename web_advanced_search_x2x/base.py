# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields, _
from odoo.models import BaseModel, Model
from odoo.tools.safe_eval import safe_eval
from odoo.osv import expression

@api.model
@api.returns('self',
    upgrade=lambda self, value, args, offset=0, limit=None, order=None, count=False: value if count else self.browse(value),
    downgrade=lambda self, value, args, offset=0, limit=None, order=None, count=False: value if count else value.ids)
def custom_search(self, args, offset=0, limit=None, order=None, count=False):
    if self.env.context.get('exclude_domain') and self.env.context.get('exclude_model') and self.env.context.get('exclude_model') == self._name:
        exclude_domain = self.env.context.get('exclude_domain')
        exclude_ids = self.with_context(exclude_domain=False).search(exclude_domain).ids
        args = expression.AND([args, [('id', 'not in', exclude_ids)]])

    res = BaseModel.search(self, args, offset=offset, limit=limit, order=order, count=count)
    return res


Model.search = custom_search