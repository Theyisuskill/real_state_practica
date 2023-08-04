from odoo import fields, models, api, exceptions
from datetime import timedelta
from odoo.exceptions import UserError


class property_offer(models.Model):

    _name= "state_property.offer"
    _description= 'property offer'
    _order = 'price desc'


    price= fields.Float()
    state=fields.Selection([('accepted', 'aceptar'),
                             ('refused', 'rechazado')], copy=False)
    partner_id=fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('test.model_manuel' )
    create_date = fields.Date(string='Create Date', default=fields.Date.context_today)
    validity = fields.Integer(string='Validity', default=7)
    date_deadline = fields.Date(string='Deadline Date', compute='_compute_date_deadline', inverse='_inverse_date_deadline', store=True)
    property_type_id = fields.Many2one('estate_property.type', string='Property Type', related='property_id.property_type_id', store=True)


    _sql_constraints = [
        ('check_price_positive',
         'CHECK(price >= 0)',
         'El precio de venta debe ser positivo.')
    ]
    
    
    
    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date and record.validity:
                record.date_deadline = record.create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline and record.create_date:
                record.validity = (record.date_deadline - record.create_date).days


    def accept_offer(self):
        self.ensure_one()

        self.property_id.state = 'offer_accepted'
        self.state = 'accepted'
        self.property_id.buyer_id = self.partner_id.id
        self.property_id.selling_price = self.price
        # self.property_id.selling_price = self.action_mark_as_sold


    def reject_offer(self):
        self.ensure_one()
        self.state = "refused"
        

    @api.model
    def create(self, vals):
        # Obtener la propiedad asociada a la oferta
        property_id = vals.get('property_id')
        property = self.env['test.model_manuel'].browse(property_id)

        # Verificar si el importe de la oferta es inferior al de una oferta existente
        existing_offer = self.search([('property_id', '=', property_id)], order='price desc', limit=1)
        if existing_offer and vals.get('price') < existing_offer.price:
            raise UserError(('No puedes crear una oferta con un importe inferior al de una oferta existente.'))

        # Crear la oferta
        offer = super(property_offer, self).create(vals)

        # Establecer el estado de la propiedad en "Oferta recibida"
        property.state = 'offer_received'

        return offer