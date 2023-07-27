from odoo import models, fields


class property_type(models.Model):
    
    _name= "estate_property.type"
    
    name= fields.Char(required=True) 
    postcode=fields.Float(required=True)