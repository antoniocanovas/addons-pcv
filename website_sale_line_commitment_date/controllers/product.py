# Part of Odoo. See LICENSE file for full copyright and licensing details.

from dateutil.parser import parse

from odoo.http import request
from odoo import http

from odoo.addons.website_sale.controllers.main import WebsiteSale

def parse_date(date):
    return date and parse(date).replace(tzinfo=None)


class WebsiteSaleRenting(WebsiteSale):

    @http.route()
    def cart_update(self, *args, start_date=None, **kw):
        """ Override to parse to datetime optional pickup and return dates.
        """
        print("CART UPDATE")
        start_date = parse_date(start_date)
        print("CART UPDATE", start_date)
        return super().cart_update(*args, start_date=start_date, **kw)

    @http.route()
    def cart_update_json(self, *args, start_date=None, **kwargs):
        """ Override to parse to datetime optional pickup and return dates.
        """
        start_date = parse_date(start_date)
        print("CART UPDATE JSON", start_date)
        return super().cart_update_json(
            *args, start_date=start_date, **kwargs
        )