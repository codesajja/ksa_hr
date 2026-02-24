frappe.ui.form.on('Employee', {
    refresh: function(frm) {
        check_expiry_alerts(frm);
    },
    custom_visa_expiry_date: function(frm) {
        check_expiry_alerts(frm);
    },
    custom_iqama_expiry: function(frm) {
        check_expiry_alerts(frm);
    }
});

function check_expiry_alerts(frm) {

    let today = frappe.datetime.get_today();
    let messages = [];
    let has_expired = false;

    // ===== VISA CHECK =====
    if (frm.doc.custom_visa_expiry_date) {

        let visa_diff = frappe.datetime.get_diff(
            frm.doc.custom_visa_expiry_date,
            today
        );

        if (visa_diff < 0) {
            has_expired = true;
            messages.push(
                __("⚠ Visa has already expired.")
            );
        } 
        else if (visa_diff <= 30) {
            messages.push(
                __("⚠ Visa will expire within {0} day(s).", [visa_diff])
            );
        }
    }

    // ===== IQAMA CHECK =====
    if (frm.doc.custom_iqama_expiry) {

        let iqama_diff = frappe.datetime.get_diff(
            frm.doc.custom_iqama_expiry,
            today
        );

        if (iqama_diff < 0) {
            has_expired = true;
            messages.push(
                __("⚠ Iqama has already expired.")
            );
        } 
        else if (iqama_diff <= 30) {
            messages.push(
                __("⚠ Iqama will expire within {0} day(s).", [iqama_diff])
            );
        }
    }

    // ===== SHOW SINGLE POPUP =====
    if (messages.length > 0) {

        frappe.msgprint({
            title: __("Document Expiry Alert"),
            message: messages.join("<br><br>"),
            indicator: has_expired ? "red" : "orange"
        });

    }
}