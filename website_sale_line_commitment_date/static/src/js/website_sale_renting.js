/** @odoo-module **/

import { WebsiteSale } from 'website_sale.website_sale';
import { DateserviceMixin } from '@website_sale_line_commitment_date/js/dateservice_mixin';

WebsiteSale.include(DateserviceMixin);
WebsiteSale.include({
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


});
