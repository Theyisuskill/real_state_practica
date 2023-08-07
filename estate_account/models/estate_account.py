from odoo import models, fields, api

class EstateProperty(models.Model):
    _inherit = 'test.model_manuel'

    def action_mark_as_sold(self):
        # Primer paso: invalidar el método action_sold
        
        res = super(EstateProperty, self).action_mark_as_sold()
        estate_property = self.property_type_id
        invoice_values = {
        'move_type': 'out_invoice'
        }
        invoice = self.env['account.move'].create(invoice_values)
        invoice_line_1 = {
            'name': '6 del precio de venta',
            'quantity': 1,
            'price_unit': self.selling_price * 0.06,
        }
        invoice_line_2 = {
            'name': 'Gastos administrativos',
            'quantity': 1,
            'price_unit': 100.00,
        }
        invoice.write({
            'invoice_line_ids': [(0, 0, invoice_line_1), (0, 0, invoice_line_2)],
        })
        return res
