/** @odoo-module **/

import { _t, _lt } from 'web.core';
import { sprintf } from "@web/core/utils/strings";

export const msecPerUnit = {
    hour: 3600 * 1000,
    day: 3600 * 1000 * 24,
    week: 3600 * 1000 * 24 * 7,
    month: 3600 * 1000 * 24 * 30,
};
export const unitMessages = {
    hour: _lt("(%s hours)."),
    day: _lt("(%s days)."),
    week: _lt("(%s weeks)."),
    month: _lt("(%s months)."),
};

export const RentingMixin = {

    /**
     * Get the message to display if the renting has invalid dates.
     *
     * @param {moment} startDate
     * @param {moment} endDate
     * @private
     */

    _getDateFromInputOrDefault(picker, fieldName, inputName) {
        console.log("DEBUG 13")
        let date = picker && picker[fieldName];
        if (!date || !date._isValid) {
            const $defaultDate = this.el.querySelector('input[name="default_' + inputName + '"]');
            date = $defaultDate && $defaultDate.value;
        } else {
            date = date.toISOString();
        }
        console.log("DEBUG 14")
        return date;
    },

    /**
     * Get the renting pickup and return dates from the website sale renting daterange picker object.
     *
     * @param {$.Element} $product
     */
    _getRentingDates($product) {
        console.log("DEBUG 12")
        const dateservice = ($product || this.$el).find('input[name=date_service]').val();
        /*if (dateservice.length){
            console.log(dateservice.value)
            return {
                start_date: dateservice.value
            }
        }*/
        if (dateservice) {
            console.log("FECHA SELECCIONADA:" + dateservice)
             return {
                start_date: dateservice,
            }
            //return {
            //    start_date: this._getDateFromInputOrDefault(picker, 'startDate', 'start_date'),
                //end_date: this._getDateFromInputOrDefault(picker, 'endDate', 'end_date'),
            //};
        }


        //const rentingDates = ($product || this.$el).find('input[name=renting_dates]');
        /*if (rentingDates.length) {
            const picker = rentingDates.data('datetimepicker');
            console.log(picker)
            return {
                start_date: this._getDateFromInputOrDefault(picker, 'startDate', 'start_date'),
                //end_date: this._getDateFromInputOrDefault(picker, 'endDate', 'end_date'),
            };
        }*/
        return {};
    },

};
