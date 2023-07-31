from odoo import fields, models


class property_tag(models.Model):
    
    _name= "state_property.tag"
    
    
    name= fields.Char()