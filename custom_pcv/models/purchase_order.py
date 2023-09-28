# Copyright 2023 Serincloud SL - Ingenieriacloud.com

from odoo import fields, models, api

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    # Pedidos de venta de los que proviene esta compra:
    @api.depends('order_line.sale_line_id')
    def _get_sale_orders_ids(self):
        for record in self:
            sale_orders = []
            for li in record.order_line:
                if (li.sale_line_id.id) and (li.id not in sale_orders):
                    sale_orders.append(li.id)
            record['sale_order_ids'] = [(6,0,sale_orders)]
    sale_order_ids = fields.Many2many(comodel_name='sale.order', string='Sale orders', store=True,
                                      relation='purchase2sale_m2m_rel',
                                      compute='_get_sale_orders_ids')

    @api.depends('sale_order_ids')
    def _get_events_name(self):
        for record in self:
            events, names = [], ""
            for li in record.order_line:
                event = li.sale_line_id.order_id.event_id
                if (event.id) and (event.name) and (event.id not in events):
                    events.append(event.id)
                    names += event.name + " "
            record['event_name'] = names
    event_name = fields.Char('Event', store=False, compute='_get_events_name')

    @api.depends('sale_order_ids')
    def _get_stand_numbers(self):
        for record in self:
            stand_numbers, names = [], ""
            for li in record.order_line:
                event = li.sale_line_id.order_id.event_id
                if (event.id) and (li.sale_line_id.order_id.stand_number not in stand_numbers):
                    stand_numbers.append(li.sale_line_id.order_id.stand_number)
                    names += str(li.sale_line_id.order_id.stand_number) + " " + str(li.sale_line_id.order_id.stand_name) + ". "
            record['stand_number'] = names
    stand_number = fields.Char('Stand', store=False, compute='_get_stand_numbers')

    # PCV ha hecho el pedido de venta, va a ser siempre el mismo según el cliente así que m2o al primero:
    @api.depends('sale_order_ids')
    def _get_sale_customer(self):
        for record in self:
            sale_customer = False
            for li in record.order_line:
                if (li.sale_line_id.order_partner_id.id) and (sale_customer == False):
                    sale_customer = li.sale_line_id.order_partner_id.id
            record['sale_partner_id'] = sale_customer
    sale_partner_id = fields.Many2one('res.partner', string='Customer', store=False, compute='_get_sale_customer')

    # Función para confirmar automáticamente los pedidos que vienen del comercio electrónico (ver acción automática):
    def website_sale_purchase_auto_confirm(self):
        for record in self:
            confirm = False
            for li in record.order_line:
                if (li.sale_line_id.id) and (li.sale_order_id.team_id.id == li.sale_line_id.order_id.website_id.salesteam_id.id):
                    confirm = True
            if (confirm == True):
                record.button_confirm()