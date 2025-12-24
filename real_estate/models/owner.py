from odoo import models, fields, api

class Owner(models.Model):
    _name = 'owner'
    _description = 'owner'
    _inherit=['mail.thread','mail.activity.mixin']

    name = fields.Char(string="Name", required=True)
    img = fields.Binary(string="    ")
    gender = fields.Selection(string="Gender", selection=[('m', 'Male'), ('f', 'Female'), ], required=False, )
    property_ids = fields.One2many(comodel_name="property", inverse_name="owner_id", string="property", required=False, )

    def action_create_property(self):
        if self.gender == "m":
            title = "Mr"
        elif self.gender == "f":
            title = "Ms"
        else:
            title = ""
        return {
            'type': 'ir.actions.act_window',
            'name': f"Create Property for {title} {self.name.capitalize()}",
            'res_model': 'property',
            'view_mode': 'form',
            'target': 'current',

            'context': {
                'default_owner_id': self.id
            }
        }


    def owner_excel_report(self):
        active_ids = self.env.context.get("active_ids")
        return {
            'type': 'ir.actions.act_url',
            'url': f'/owner/excel/report/{active_ids}',
            'target': 'new'

        }
