/** @odoo-module **/
import { _t, _lt } from 'web.core';
import { WebsiteSale } from 'website_sale.website_sale';
import { DateserviceMixin } from '@website_sale_line_commitment_date/js/dateservice_mixin';

WebsiteSale.include(DateserviceMixin);
WebsiteSale.include({
     events: Object.assign(WebsiteSale.prototype.events, {
        //'change .js_main_product .o_website_sale_daterange_picker input.datetimepicker-input': '_onDatePickerApply',
       // 'apply input.datetimepicker-input': '_updateRootProduct',
    }),
    /**
     * Assign the renting dates to the rootProduct for rental products.
     *
     * @override
     */
    _updateRootProduct($form, productId) {
        this._super(...arguments);
        const date = this._getDateService();
        Object.assign(this.rootProduct, this._getDateService());
    },

    _onClickAdd(ev) {
        const $form = this.$(ev.currentTarget).closest('form');
        if ($form.find('input[name="is_dateservice"]').val()) {
            if (!this._verifyValidDateService($form)) {
                ev.stopPropagation();
                return Promise.resolve();
            }
        }

        return this._super(...arguments);
    },

    _verifyValidDateService($parent) {
        const rentingDates = this._getDateService();
        let message
        if (!rentingDates['start_date']) {
            const input = this.el.querySelector('input[name=date_service]');
            if (input) {
                input.classList.add('border-danger');
            }
            message = _t("Please select a date for the selected service.");
        }
        if (message) {
              this.el.querySelector('span[name=dateservice_warning_message]').innerText = message;
              this.el.querySelector('.o_dateservice_warning').classList.remove('d-none');
                // only disable when there is a message. Hence, it doesn't override other disabling.
              this._toggleDisable($parent.closest('form'), !message);
        } else {
                this.el.querySelector('.o_dateservice_warning').classList.add('d-none');
        }
            return !message;

    },

    /**
     * Redirect to the shop page with the appropriate dates as search.
     */
    /*_onDatePickerApply: function (ev) {

        console.log("SUPERTEST" + dateservice)
        const dateservice = this._getRentingDates();
        if (dateservice) {
           // get current URL parameters
            const searchParams = new URLSearchParams(window.location.search);
            searchParams.set("start_date",dateservice);
            const searchString = searchParams.toString();
            window.location = `/shop` + searchString.length ? `?${searchString}` : ``;
            //this.isRedirecting = true;
        }
    },*/
});
