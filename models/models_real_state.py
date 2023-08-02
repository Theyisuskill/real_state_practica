from odoo import models, fields, api, exceptions
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo.tools.float_utils import float_compare, float_is_zero

class TestModel(models.Model):
    _name = "test.model_manuel"
    _description= "real state yisus"
    _rec_name = 'title'
    _order = 'id desc'

    
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
    garden=fields.Boolean()
    garden_area = fields.Integer(attrs="{'invisible': [('garden', '=', False)]}")
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
                            ('offer_received', ' reservada'),
                            ('offer_accepted',' aceptada'),
                            ('sold', 'Pagado'),
                            ('canceled', 'Cancelado')],required=True,copy=False, default= 'new', readonly=True, string="State",
                            attrs="{'invisible': [('refused', '=', False)]}")
    
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    seller_id = fields.Many2one(
        "res.users", string="Salesman", index=True, default=lambda self: self.env.user
    )
    cozy_id= fields.Many2many("state_property.tag", required=True, )
    new_fiel_ids = fields.One2many('state_property.offer', 'property_id', string='Offers')
    total_area=fields.Float(compute="_compute_total")
    best_price= fields.Char(compute="_compute_description") 
    property_type_id = fields.Many2one("estate_property.type", )
    
   
    
    @api.constrains('expected_price', 'selling_price')
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2) and float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=2) == -1:
                raise exceptions.ValidationError("Selling price cannot be less than 90% of the expected price.")
    
    _sql_constraints = [
        ('check_expected_price_positive',
         'CHECK(expected_price > 0)',
         'El precio esperado debe ser estrictamente positivo.') 
    ]
    _sql_constraints = [
        ('check_selling_price_positive',
         'CHECK(selling_price >= 0)',
         'El precio de venta debe ser positivo.')
    ]
    

    def action_cancel(self):
        if self.state == 'sold':
            raise exceptions.UserError("Cannot cancel a sold property.")
        self.state = 'canceled'

    def action_mark_as_sold(self):
        if self.state == 'canceled':
            raise exceptions.UserError("Cannot mark a canceled property as sold.")
        self.state = 'sold'
    
    
    
    @api.depends("living_area","garden_area")
    def _compute_total(self):
        
        for record in self:
            record.total_area= record.living_area + record.garden_area
            
    
    
    @api.depends("new_fiel_ids.price")        
    def _compute_description(self):
        
        for record in self: 
            prices=record.new_fiel_ids.mapped("price")
            record.best_price= max(prices) if prices else 0.0
    
    @api.onchange('garage')
    def _onchange_has_garden(self):
        if self.garage:
            self.garden_area = 10.0
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0.0
            self.garden_orientation = False