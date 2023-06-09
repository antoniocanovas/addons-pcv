# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    def _apply_pricelist_from_commitment_date(self):
        print("SO", "_apply_pricelist_from_commitment_date")
        self.ensure_one()
        for line in self.order_line:
            # Price unit is still modifiable if not quantity invoiced
            if not line.qty_invoiced:
                # Call product_uom_change as it only updates price_unit using pricelist
                line.with_context(
                    force_pricelist_date=self.commitment_date
                )._compute_pricelist_item_id()
                #).product_uom_change()

    @api.onchange("commitment_date", "pricelist_id")
    def onchange_price_with_commitment_date(self):
        print("SO", "onchange_price_with_commitment_date")
        self._apply_pricelist_from_commitment_date()

    def create(self, vals):
        print("SO", "create")
        if self._context.get("import_file"):
            return super().create(vals)
        sale = super().create(vals)
        if sale.commitment_date:
            sale._apply_pricelist_from_commitment_date()
        return sale

    def write(self, vals):
        print("SO", "write")

        if self._context.get("import_file"):
            return super().write(vals)
        if "commitment_date" not in vals and "pricelist_id" not in vals:
            return super().write(vals)
        for sale in self:
            old_commitment_date = sale.commitment_date
            old_pricelist = sale.pricelist_id
            super(SaleOrder, sale).write(vals)
            if (
                old_commitment_date != sale.commitment_date
                or old_pricelist != sale.pricelist_id
            ):
                sale._apply_pricelist_from_commitment_date()
        return True

    def update_prices(self):
        print("SO", "update_prices")
        self.ensure_one()
        return super(
            SaleOrder,
            self.with_context(force_pricelist_date=self.commitment_date),
        ).update_prices()
