from odoo import fields, models


class property_tag(models.Model):
    
    _name= "state_property.tag"
    _description= 'property tag'
    _order = 'name'
    
    name= fields.Char()
    color=fields.Integer()
    
    _sql_constraints = [
        ('unique_tag_name',
         'UNIQUE(name)',
         'El nombre de etiqueta de propiedad debe ser único.')
    ]