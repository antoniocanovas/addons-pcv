# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class ProductPricelist(models.Model):

    _inherit = "product.pricelist"

    def _compute_price_rule_multi(self, products, qty, uom=None, date=False, **kwargs):
        print("_compute_price_rule_multi")
        force_pricelist_date = self.env.context.get("force_pricelist_date")
        if force_pricelist_date:
            date = force_pricelist_date
        return super()._compute_price_rule_multi(products, qty, uom, date, **kwargs)

    def _compute_price_rule(self, products, qty, uom=None, date=False, **kwargs):
        print("_compute_price_rule")
        force_pricelist_date = self.env.context.get("force_pricelist_date")
        print("FORCE", force_pricelist_date)
        if force_pricelist_date:
            date = force_pricelist_date
        return super()._compute_price_rule(products, qty, uom, date, **kwargs)

    def _get_products_price(self, products, quantity, uom=None, date=False, **kwargs):
        print("_get_products_price")
        force_pricelist_date = self.env.context.get("force_pricelist_date")
        if force_pricelist_date:
            date = force_pricelist_date
        return super()._get_products_price(products, quantity, uom, date, **kwargs)

    def _get_product_price(self, product, quantity, uom=None, date=False, **kwargs):
        print("_get_product_price")
        force_pricelist_date = self.env.context.get("force_pricelist_date")
        if force_pricelist_date:
            date = force_pricelist_date
        return super()._get_product_price(product, quantity, uom, date, **kwargs)

    def _get_product_price_rule(self, product, quantity, uom=None, date=False, **kwargs):
        print("_get_product_price_rule")
        force_pricelist_date = self.env.context.get("force_pricelist_date")
        if force_pricelist_date:
            date = force_pricelist_date
        return super()._get_product_price_rule(product, quantity, uom, date, **kwargs)
    def _get_product_rule(self, product, quantity, uom=None, date=False, **kwargs):
        print("_get_product_rule")
        force_pricelist_date = self.env.context.get("force_pricelist_date")
        if force_pricelist_date:
            date = force_pricelist_date
        return super()._get_product_rule(product, quantity, uom, date, **kwargs)