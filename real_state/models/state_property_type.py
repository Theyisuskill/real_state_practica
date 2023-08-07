from odoo import models, fields, api, _


class property_type(models.Model):
    
    _name= "estate_property.type"
    _description= 'property type'
    _order = 'name'
    
  
    name= fields.Char(required=True) 
    sequence = fields.Integer('Sequence' )
    property_id=fields.One2many('test.model_manuel', 'property_type_id', )
    property_offers_ids=fields.One2many('state_property.offer','property_type_id', string='offers' )
    offer_count = fields.Integer(string='Offer Count', compute='_compute_offer_count')

    @api.depends('property_offers_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.property_offers_ids)


    _sql_constraints = [
        ('unique_type_name',
         'UNIQUE(name)',
         'The property type name must be unique.')
    ]
    
    def button_open_offers(self):
        
        self.ensure_one()
        return {
            'name': _("Offers"),
            'type': 'ir.actions.act_window',
            'res_model': 'state_property.offer',
            'context': {'create': False},
            'view_mode': 'list',
            # 'res_id': self.move_id.id,
        }
    
    