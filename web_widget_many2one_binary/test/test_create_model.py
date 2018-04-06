# -*- coding: utf-8 -*-

from odoo import api, fields, models

class ExampleModel(models.Model):
    _name = 'example.model'

    testing_field = fields.Many2one("ir.attachment", "Test")

    # This code needs to be created in each model where we want to store the id of the record that has the m2o to ir.attachment
    # Write method is already covered with controllers. On create, Attachment is created on the fly so there is no res_id
    @api.model
    def create(self, vals):
        res = super(ExampleModel, self).create(vals)
        for key, val in vals.iteritems():
            field = self._fields.get(key)
            if field.type == 'many2one'and field.comodel_name == 'ir.attachment' and val:
                self.env['ir.attachment'].browse(val).write({'res_id': res.id})
        return res