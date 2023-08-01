from odoo import models, fields


class property_type(models.Model):
    
    _name= "estate_property.type"
    _description= 'property type'
    _order = 'name'
    
  
    name= fields.Char(required=True) 
    sequence = fields.Integer('Sequence' )
    property_ids=fields.One2many('test.model_manuel', 'property_type_id')
    

    _sql_constraints = [
        ('unique_type_name',
         'UNIQUE(name)',
         'El nombre de tipo de propiedad debe ser único.')
    ]