# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _cart_find_product_line(
        self, product_id=None, line_id=None, start_date=None, **kwargs
    ):
        """ Override to filter on the pickup and return date for rental products. """
        lines = super()._cart_find_product_line(product_id, line_id, **kwargs)
        if not line_id and start_date:
            lines = lines.filtered(
                lambda l: l.commitment_date == start_date
            )
        return lines

    def _prepare_order_line_values(
        self, product_id, quantity, start_date=None, end_date=None, **kwargs
    ):
        """Add corresponding pickup and return date to rental line"""


        values = super()._prepare_order_line_values(product_id, quantity, **kwargs)
        product = self.env['product.product'].browse(product_id)
        if start_date:
            self.commitment_date = start_date
            values.update({
                'commitment_date': start_date,

                #'is_rental': True,
            })
            print("_prepare_order_line_values", start_date)
            #self.is_rental_order = True
        return values

