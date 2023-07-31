from odoo import fields, models, api, exceptions
from datetime import timedelta


class property_offer(models.Model):
    
    _name= "state_property.offer"
    
    
    price= fields.Float()
    status=fields.Selection([('accepted', 'aceptar'),
                             ('refused', 'rechazado')], copy=False)
    partner_id=fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('test.model_manuel' )
    create_date = fields.Date(string='Create Date', default=fields.Date.context_today)
    validity = fields.Integer(string='Validity', default=7)
    date_deadline = fields.Date(string='Deadline Date', compute='_compute_date_deadline', inverse='_inverse_date_deadline', store=True)
    
    def action_accept(self):
        self.ensure_one()
        if self.status == 'accepted':
            return
        
        # Check if another offer has already been accepted for the property
        existing_offer = self.env['estate.property.offer'].search([
            ('property_id', '=', self.property_id.id),
            ('status', '=', 'accepted')
        ])
        if existing_offer:
            raise exceptions.UserError("Another offer has already been accepted for this property.")
        
        self.status = 'accepted'
        self.property_id.buyer = self.partner_id.id
        self.property_id.seller = self.price
        
    def action_reject(self):
        self.ensure_one()
        if self.status == 'refused':
            return

        self.status = 'refused'
    
    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date and record.validity:
                record.date_deadline = record.create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline and record.create_date:
                record.validity = (record.date_deadline - record.create_date).days
    
    