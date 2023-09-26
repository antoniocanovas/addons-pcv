# Copyright 2023 Serincloud SL - Ingenieriacloud.com

from odoo import fields, models, api

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    # Pedidos de venta de los que proviene esta compra:
    @api.depends('order_line.sale_line_id')
    def _get_sale_orders(self):
        for record in self:
            sale_orders = []
            for li in record.order_line:
                if (li.sale_line_id.id) and (li.id not in sale_orders):
                    sale_orders.append(li.id)
            record['sale_order_ids'] = [(6,0,sale_orders)]
    sale_order_ids = fields.Many2many(string='Sale orders', store=True, compute='_get_sale_orders',
                                      comodel_name='sale.order',
                                      relation='purchase_sale_order_rel',
                                      column1='purchase_id',
                                      column2='sale_id',
                                      )

    # Función para confirmar automáticamente los pedidos que vienen del comercio electrónico (ver acción automática):
    def website_sale_purchase_auto_confirm(self):
        for record in self:
            confirm = False
            for li in record.order_line:
                if (li.sale_line_id.id) and (li.sale_order_id.team_id.id == li.sale_line_id.order_id.website_id.salesteam_id.id):
                    confirm = True
            if (confirm == True):
                record.button_confirm()