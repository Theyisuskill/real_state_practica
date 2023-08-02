from odoo import fields, models, api, exceptions
from datetime import timedelta



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
        self.state = "accepted"
        self.property_id.buyer_id = self.partner_id.id
        self.property_id.selling_price = self.price
        # self.property_id.selling_price = self.action_mark_as_sold



    def reject_offer(self):
        self.ensure_one()
        self.state = "refused"


    @api.depends('accept_offer', 'reject_offer')
    def _compute_botones_visibles(self):
        for record in self:
            if record.campo_1 == 'accepted':
                record.boton_1_visible = False
            else:
                record.boton_1_visible = True

            if record.campo_2 == 'refused':
                record.boton_2_visible = False
            else:
                record.boton_2_visible = True