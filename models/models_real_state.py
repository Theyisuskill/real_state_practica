from odoo import models, fields
from datetime import datetime
from dateutil.relativedelta import relativedelta

class TestModel(models.Model):
    _name = "test.model_manuel"
    _description= "real state yisus"
    
    name= fields.Char(required=True)
    description= fields.Text()
    postcode= fields.Char()
    date_availability=fields.Date()
    expected_price= fields.Float(required=True )
    selling_price = fields.Float(readonly=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'Norte'),
        ('south', 'Sur'),
        ('east', 'Este'),
        ('west', 'Oeste')
    ],help="Type is used to separate Leads and Opportunities")
    avalible_date= fields.Boolean()
    date_disponibility = fields.Datetime(default=lambda self: datetime.now() + relativedelta(months=3))
    active=fields.Boolean()
    