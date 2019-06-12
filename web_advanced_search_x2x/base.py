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
    if isinstance(args, list):
        args_with_id = 'id' in [x[0] for x in args if isinstance(x, (tuple, list)) and len(x) == 3] # If we are already sending an arg with id we will skip it because it will be [('id','in',[1])] and we are going to be on formview.
    else:
        args_with_id = False

    if self.env.context.get('exclude_domain') and self.env.context.get('exclude_model') and self.env.context.get('exclude_model') == self._name and not args_with_id:
        exclude_domain = self.env.context.get('exclude_domain')
        exclude_ids = self.with_context(exclude_domain=False).search(exclude_domain).ids
        args = expression.AND([args, [('id', 'not in', exclude_ids)]])

    res = BaseModel.search(self, args, offset=offset, limit=limit, order=order, count=count)
    return res


@api.model
def custom_read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
    if isinstance(domain, list):
        args_with_id = 'id' in [x[0] for x in domain if isinstance(x, (tuple, list)) and len(x) == 3]
    else:
        args_with_id = False

    if self.env.context.get('exclude_domain') and self.env.context.get('exclude_model') and self.env.context.get('exclude_model') == self._name and not args_with_id:
        exclude_domain = self.env.context.get('exclude_domain')
        exclude_ids = self.with_context(exclude_domain=False).search(exclude_domain).ids
        domain = expression.AND([domain, [('id', 'not in', exclude_ids)]])

    res = BaseModel.read_group(self, domain, fields, groupby, offset=offset, limit=limit, orderby=orderby, lazy=lazy)
    return res


Model.search = custom_search
Model.read_group = custom_read_group
