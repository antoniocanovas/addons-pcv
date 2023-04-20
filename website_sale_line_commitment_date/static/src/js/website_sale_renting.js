/** @odoo-module **/

import { WebsiteSale } from 'website_sale.website_sale';
import { DateserviceMixin } from '@website_sale_line_commitment_date/js/dateservice_mixin';

WebsiteSale.include(DateserviceMixin);
WebsiteSale.include({
     events: Object.assign(WebsiteSale.prototype.events, {
       // 'change .js_main_product .o_website_sale_daterange_picker input.datetimepicker-input': '_onDatePickerApply',
       // 'apply input.datetimepicker-input': '_updateRootProduct',
    }),
    /**
     * Assign the renting dates to the rootProduct for rental products.
     *
     * @override
     */
    _updateRootProduct($form, productId) {
        console.log("DEBUG 11")
        this._super(...arguments);
        const date = this._getRentingDates();
        console.log("URP1" + date);
        console.log(date)
        Object.assign(this.rootProduct, this._getRentingDates());
        console.log("URP2" + this.rootProduct)
        console.log(this.rootProduct)
    },

    /**
     * Redirect to the shop page with the appropriate dates as search.
     */
    _onDatePickerApply: function (ev) {
        console.log("TEST UPDATE")

        const dateservice = this._getRentingDate();
        console.log(dateservice)
        if (dateservice) {
           // get current URL parameters
            const searchParams = new URLSearchParams(window.location.search);
            searchParams.set("start_date",dateservice);
            const searchString = searchParams.toString();
            window.location = `/shop` + searchString.length ? `?${searchString}` : ``;
            //this.isRedirecting = true;
        }
    },
});
