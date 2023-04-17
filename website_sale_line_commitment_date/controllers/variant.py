# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.addons.website_sale.controllers.variant import WebsiteSaleVariantController
from odoo.addons.website_sale_line_commitment_date.controllers.product import parse_date


class WebsiteSaleRentingVariantController(WebsiteSaleVariantController):
    @http.route()
    def get_combination_info_website(
        self, *args, context=None, start_date=None, **kwargs
    ):
        print("get_combination_info_website", start_date)
        """ Override to parse and add to context optional pickup and return dates.
        """
        context = context if context is not None else {}
        if start_date:
            context.update(start_date=parse_date(start_date))
        return super().get_combination_info_website(
            *args, context=context, start_date=start_date, **kwargs
        )
