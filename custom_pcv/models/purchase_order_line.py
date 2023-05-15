# Copyright 2023 Serincloud SL - Ingenieriacloud.com

from odoo import fields, models, api

class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"


    @api.depends('create_date')
    def _get_sale_event(self):
        for record in self:
            record.event_id = record.sale_order_id.event_id.id
    event_id = fields.Many2one('event.event', string='Event',
                                      domain=[('stage_id.is_finished','=',False),('is_published','=',True)],
                                      compute='_get_sale_event'
                               )

    @api.depends('create_date')
    def _get_sale_stand_name(self):
        for record in self:
            record.event_id = record.sale_order_id.stand_name
    stand_name      = fields.Char('Stand name', store=True,
                                  compute='_get_sale_stand_name'
                                  )

    @api.depends('create_date')
    def _get_sale_stand_number(self):
        for record in self:
            record.event_id = record.sale_order_id.stand_number
    stand_number    = fields.Char('Stand number', store=True,
                                  compute='_get_sale_stand_number'
                                  )