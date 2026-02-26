frappe.ui.form.on('Appraisal', {

    refresh: function(frm) {
        check_appraisal_reminder(frm);
    },

    custom_appraisal_frequency: function(frm) {
        check_appraisal_reminder(frm);
    },

    custom_last_appraisal_date: function(frm) {
        check_appraisal_reminder(frm);
    }
});


function check_appraisal_reminder(frm) {

    if (!frm.doc.custom_appraisal_frequency || !frm.doc.custom_last_appraisal_date) {
        return;
    }

    let today = frappe.datetime.get_today();

    let diff_days = frappe.datetime.get_diff(
        today,
        frm.doc.custom_last_appraisal_date
    );

    let threshold = 0;

    if (frm.doc.custom_appraisal_frequency === "Monthly") {
        threshold = 30;
    } 
    else if (frm.doc.custom_appraisal_frequency === "Quarterly") {
        threshold = 90;
    } 
    else if (frm.doc.custom_appraisal_frequency === "Mid-Year") {
        threshold = 182;
    } 
    else if (frm.doc.custom_appraisal_frequency === "Yearly") {
        threshold = 365;
    }

    if (diff_days >= threshold) {
        frappe.msgprint({
            title: __("Appraisal Reminder"),
            message: __("⚠ This appraisal cycle is due."),
            indicator: "orange"
        });
    }
}