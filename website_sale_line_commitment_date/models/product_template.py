# Part of Odoo. See LICENSE file for full copyright and licensing details.

from dateutil.relativedelta import relativedelta
from math import ceil
from pytz import timezone, utc, UTC

from odoo import fields, models
from odoo.http import request
from odoo.addons.sale_temporal.models.product_pricing import PERIOD_RATIO
from odoo.tools import format_amount

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    ##### cambiamos rent_ok  => dateservice_ok
    dateservice_ok = fields.Boolean(
        string="Dated",
        help="Allow renting of this product.")

    def _get_combination_info(
        self, combination=False, product_id=False, add_qty=1, pricelist=False,
        parent_combination=False, only_template=False
    ):
        """Override to add the information about renting for rental products

        If the product is dateservice_ok, this override adds the following information about the renting :
            - is_rental: Whether combination is rental,
            - rental_duration: The duration of the first defined product pricing on this product
            - rental_unit: The unit of the first defined product pricing on this product
            - default_start_date: If no pickup nor rental date in context, the start_date of the
                                   first renting sale order line in the cart;
            - default_end_date: If no pickup nor rental date in context, the end_date of the
                                   first renting sale order line in the cart;
            - current_rental_duration: If no pickup nor rental date in context, see rental_duration,
                                       otherwise, the duration between pickup and rental date in the
                                       current_rental_unit unit.
            - current_rental_unit: If no pickup nor rental date in context, see rental_unit,
                                   otherwise the unit of the best pricing for the renting between
                                   pickup and rental date.
            - current_rental_price: If no pickup nor rental date in context, see price,
                                    otherwise the price of the best pricing for the renting between
                                    pickup and rental date.
        """
        self.ensure_one()
        print("PRODUCT_TEMPLATE SAMPLE" )
        combination_info = super()._get_combination_info(
            combination=combination, product_id=product_id, add_qty=add_qty, pricelist=pricelist,
            parent_combination=parent_combination, only_template=only_template
        )

        if self.dateservice_ok:
            print(self.dateservice_ok)
            return {
                **combination_info,
                'is_dateservice': True,
            }

        if not self.dateservice_ok:
            # I wonder if it's useful to fill this dict with unused values.
            return {
                **combination_info,
                'is_dateservice': False,
            }

    def _website_show_quick_add(self):
        self.ensure_one()
        return not self.dateservice_ok and super()._website_show_quick_add()

    def _search_get_detail(self, website, order, options):
        search_details = super()._search_get_detail(website, order, options)
        if options.get('rent_only') or (options.get('from_date') and options.get('to_date')):
            search_details['base_domain'].append([('dateservice_ok', '=', True)])
        return search_details
