from odoo import models, fields
from datetime import datetime
from dateutil.relativedelta import relativedelta

class TestModel(models.Model):
    _name = "test.model_manuel"
    _description= "real state yisus"
    _rec_name = 'title'
    
    title= fields.Char(required=True)
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
    ],help="cardinality")
    avalible_date= fields.Boolean()
    date_disponibility = fields.Datetime(default=lambda self: datetime.now() + relativedelta(months=3), copy=False)
    active=fields.Boolean()
    state=fields.Selection([('new', 'Nuevo'),
                            ('offer_received', 'Oferta reservada'),
                            ('offer_accepted','Oferta aceptada'),
                            ('sold', 'Agotado'),
                            ('canceled', 'Cancelado')],required=True,copy=False, default= 'new')
    
    buyer= fields.Many2one()
    seller= fields.Many2one()
    