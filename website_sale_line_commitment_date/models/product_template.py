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


    def _get_default_renting_dates(
        self, start_date, end_date, only_template, website, duration, unit
    ):
        """ Get default renting dates to help user

        :param datetime start_date: a start_date which is directly returned if defined
        :param datetime end_date: a end_date which is directly returned if defined
        :param bool only_template: whether only the template information are needed, in this case,
                                   there will be no need to give the default renting dates.
        :param Website website: the website currently browsed by the user
        :param int duration: the duration expressed in int, in the unit given
        :param string unit: The duration unit, which can be 'hour', 'day', 'week' or 'month'
        """
        if start_date or end_date or only_template:
            return start_date, end_date

        if website and request:
            sol_rental = website.sale_get_order().order_line.filtered('is_rental')[:1]
            if sol_rental:
                end_date = max(
                    sol_rental.return_date,
                    self._get_default_end_date(sol_rental.start_date, duration, unit)
                )
                return sol_rental.start_date, end_date

        default_date = self._get_default_start_date()
        return default_date, self._get_default_end_date(default_date, duration, unit)

    def _get_default_start_date(self):
        """ Get the default pickup date and make it extensible """
        tz = timezone(self.env.user.tz or self.env.context.get('tz') or 'UTC')
        date = utc.localize(fields.Datetime.now()).astimezone(tz)
        date += relativedelta(days=1, minute=0, second=0, microsecond=0)
        return self._get_first_potential_date(date.astimezone(UTC).replace(tzinfo=None))

    def _get_default_end_date(self, start_date, duration, unit):
        """ Get the default return date based on pickup date and duration

        :param datetime start_date: the default start_date
        :param int duration: the duration expressed in int, in the unit given
        :param string unit: The duration unit, which can be 'hour', 'day', 'week' or 'month'
        """
        return self._get_first_potential_date(max(
            start_date + relativedelta(**{f'{unit}s': duration}),
            start_date + self.env.company._get_minimal_rental_duration()
        ))

    def _get_first_potential_date(self, date):
        """ Get the first potential date which respects company unavailability days settings
        """
        tz = timezone(self.env.user.tz or self.env.context.get('tz') or 'UTC')
        days_forbidden = self.env.company._get_renting_forbidden_days()
        weekday = utc.localize(date).astimezone(tz).isoweekday()
        for i in range(7):
            if ((weekday + i) % 7 or 7) not in days_forbidden:
                break
        return date + relativedelta(days=i)

    def _search_render_results_prices(self, mapping, combination_info):
        if not combination_info['is_rental']:
            return super()._search_render_results_prices(mapping, combination_info)

        return self.env['ir.ui.view']._render_template(
            'website_sale_renting.rental_search_result_price',
            values={
                'currency': mapping['detail']['display_currency'],
                'price': combination_info['price'],
                'duration': combination_info['rental_duration'],
                'unit': combination_info['rental_unit'],
            }
        ), None

    def _get_sales_prices(self, pricelist):
        prices = super()._get_sales_prices(pricelist)

        for template in self:
            if not template.dateservice_ok:
                continue
            pricing = self.env['product.pricing']._get_first_suitable_pricing(template, pricelist)
            if pricing:
                prices[template.id]['rental_duration'] = pricing.recurrence_id.duration
                prices[template.id]['rental_unit'] = pricing._get_unit_label(pricing.recurrence_id.duration)
            else:
                prices[template.id]['rental_duration'] = 0
                prices[template.id]['rental_unit'] = False

        return prices

    def _website_show_quick_add(self):
        self.ensure_one()
        return not self.dateservice_ok and super()._website_show_quick_add()

    def _search_get_detail(self, website, order, options):
        search_details = super()._search_get_detail(website, order, options)
        if options.get('rent_only') or (options.get('from_date') and options.get('to_date')):
            search_details['base_domain'].append([('dateservice_ok', '=', True)])
        return search_details
