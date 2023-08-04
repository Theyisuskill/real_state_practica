from odoo import models, fields, api

class EstateProperty(models.Model):
    _inherit = 'test.model_manuel'

    def action_mark_as_sold(self):
        # Primer paso: invalidar el método action_sold
        
        res = super(EstateProperty, self).action_mark_as_sold()

        estate_property = self.property_type_id
        
        move_types = [
            ('entry', 'Journal Entry'),
            ('out_invoice', 'Customer Invoice'),
            ('out_refund', 'Customer Credit Note'),
            ('in_invoice', 'Vendor Bill'),
            ('in_refund', 'Vendor Credit Note'),
            ('out_receipt', 'Sales Receipt'),
            ('in_receipt', 'Purchase Receipt'),
        ]

        
        invoice_values = {
        'move_type': 'out_invoice'
        # Otros campos de la factura
        # ...
        }
        invoice = self.env['account.move'].create(invoice_values)
        # Tercer paso: agregar líneas de factura 
        invoice_line_1 = {
            'name': '6% del precio de venta',
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
