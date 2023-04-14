/** @odoo-module **/

import { WebsiteSale } from 'website_sale.website_sale';
import { RentingMixin } from '@website_sale_dateservice/js/renting_mixin';

WebsiteSale.include(RentingMixin);
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
