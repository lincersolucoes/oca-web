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

    new_args = []

    for cond in args or []:
        if isinstance(cond, (tuple, list)) and cond[1] in ['domain', 'not_in_domain']:
            model = self._name
            if isinstance(cond[2], (tuple, list)):
                for fieldname in cond[0].split('.'):
                    field = self.env[model]._fields[fieldname]
                    if field.type in ('one2many', 'many2many','many2one'):
                        comodel = field.comodel_name
                        domain_ids = self.env[comodel].search(cond[2]).ids
                        if cond[1] == 'domain':
                            new_args.append([cond[0], 'in', domain_ids])
                        elif cond[1] == 'not_in_domain':
                            exclude_ids = self.search([[cond[0], 'in', domain_ids]]).ids
                            new_args.append(['id', 'not in', exclude_ids])

        else:
            new_args.append(cond)

    #if self.env.context.get('exclude_domain') and self.env.context.get('exclude_model') and self.env.context.get('exclude_model') == self._name and not args_with_id:
    #    exclude_domain = self.env.context.get('exclude_domain')
    #    exclude_ids = self.with_context(exclude_domain=False).search(exclude_domain).ids
    #    args = expression.AND([args, [('id', 'not in', exclude_ids)]])

    res = BaseModel.search(self, new_args, offset=offset, limit=limit, order=order, count=count)
    return res


@api.model
def custom_read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
    if isinstance(domain, list):
        args_with_id = 'id' in [x[0] for x in domain if isinstance(x, (tuple, list)) and len(x) == 3]
    else:
        args_with_id = False

    new_domain = []

    for cond in domain or []:
        if isinstance(cond, (tuple, list)) and cond[1] in ['domain', 'not_in_domain']:
            model = self._name
            if isinstance(cond[2], (tuple, list)):
                for fieldname in cond[0].split('.'):
                    field = self.env[model]._fields[fieldname]
                    if field.type in ('one2many', 'many2many', 'many2one'):
                        comodel = field.comodel_name
                        domain_ids = self.env[comodel].search(cond[2]).ids
                        if cond[1] == 'domain':
                            new_domain.append([cond[0], 'in', domain_ids])
                        elif cond[1] == 'not_in_domain':
                            exclude_ids = self.search([[cond[0], 'in', domain_ids]]).ids
                            new_domain.append(['id', 'not in', exclude_ids])

        else:
            new_domain.append(cond)

    # if self.env.context.get('exclude_domain') and self.env.context.get('exclude_model') and self.env.context.get('exclude_model') == self._name and not args_with_id:
    #     exclude_domain = self.env.context.get('exclude_domain')
    #     exclude_ids = self.with_context(exclude_domain=False).search(exclude_domain).ids
    #     domain = expression.AND([domain, [('id', 'not in', exclude_ids)]])

    res = BaseModel.read_group(self, new_domain, fields, groupby, offset=offset, limit=limit, orderby=orderby, lazy=lazy)
    return res


Model.search = custom_search
Model.read_group = custom_read_group
