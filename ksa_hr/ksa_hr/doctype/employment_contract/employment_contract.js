// Copyright (c) 2026, Prajakta and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Employment Contract", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on('Employment Contract', {
    probation_period: function(frm) {
        if (frm.doc.start_date && frm.doc.probation_period) {
            let probation_end = frappe.datetime.add_days(
                frm.doc.start_date,
                frm.doc.probation_period
            );
            frm.set_value('probation_end_date', probation_end);
        }
    },

    start_date: function(frm) {
        if (frm.doc.start_date && frm.doc.probation_period) {
            let probation_end = frappe.datetime.add_days(
                frm.doc.start_date,
                frm.doc.probation_period
            );
            frm.set_value('probation_end_date', probation_end);
        }
    },

    end_date: function(frm) {
        if (frm.doc.end_date) {
            frm.set_value('renewal_due_date', frm.doc.end_date);
        }
    },

    // -------------------------
    // Refresh Event (Reminder Logic)
    // -------------------------
    refresh: function(frm) {

        if (!frm.doc.renewal_due_date || !frm.doc.renewal_reminder_days) {
            return;
        }

        let today = frappe.datetime.get_today();

        let reminder_date = frappe.datetime.add_days(
            frm.doc.renewal_due_date,
            -frm.doc.renewal_reminder_days
        );

        // Contract Renewal Reminder
        if (today >= reminder_date && today <= frm.doc.renewal_due_date) {
            frappe.msgprint({
                title: __('Renewal Reminder'),
                message: __('This contract is due for renewal soon.'),
                indicator: 'orange'
            });
        }

        // Contract Expired
        if (today > frm.doc.renewal_due_date) {
            frappe.msgprint({
                title: __('Contract Expired'),
                message: __('This contract has expired.'),
                indicator: 'red'
            });
        }
    }


});
