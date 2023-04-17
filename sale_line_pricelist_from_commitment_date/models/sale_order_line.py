# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class SaleOrderLine(models.Model):

    _inherit = "sale.order.line"

    @api.depends('product_id', 'product_uom', 'product_uom_qty','commitment_date')
    def _compute_pricelist_item_id(self):
        print("product_id_change")
        for line in self:
            return super(
                SaleOrderLine,
                line.with_context(force_pricelist_date=line.commitment_date),
            )._compute_pricelist_item_id()

    @api.depends('product_id','commitment_date')
    def _compute_product_uom(self):
        print("product_uom_change")
        for line in self:
            return super(
                SaleOrderLine,
                line.with_context(force_pricelist_date=line.commitment_date),
            )._compute_product_uom()
        #)._compute_product_uom()

    @api.depends(
        "product_id", "price_unit", "product_uom", "product_uom_qty", "tax_id"
    )
    def _compute_discount(self):
        print("_compute_discount")
        for line in self:
            return super(
                SaleOrderLine,
                line.with_context(force_pricelist_date=line.commitment_date),
            )._compute_discount()
        #)._onchange_discount()
