frappe.ui.form.on('Employee', {
    refresh: function(frm) {
        check_expiry_alerts(frm);

        // Route attachments to employee's folder
        if (frm.doc.name && frm.doc.employee_name) {
            frm.attachments.attachment_control.options = {
                folder: `Home/Employee Documents/${frm.doc.name} - ${frm.doc.employee_name}`,
                restrictions: {}
            };
        }
    },
    custom_visa_expiry_date: function(frm) {
        check_expiry_alerts(frm);
    },
    custom_iqama_expiry: function(frm) {
        check_expiry_alerts(frm);
    },
    custom_medical_insurance_expiry: function(frm) {
        check_expiry_alerts(frm);
    }
});

function check_expiry_alerts(frm) {

    let today = frappe.datetime.get_today();
    let messages = [];
    let has_expired = false;

    // ===== GENERIC CHECK FUNCTION =====
    function evaluate_expiry(date_value, label) {
        if (!date_value) return;

        let diff = frappe.datetime.get_diff(date_value, today);

        if (diff < 0) {
            has_expired = true;
            messages.push(
                __("⚠ {0} has already expired.", [label])
            );
        } 
        else if (diff <= 30) {
            messages.push(
                __("⚠ {0} will expire within {1} day(s).", [label, diff])
            );
        }
    }

    // ===== CHECK ALL DOCUMENTS =====
    evaluate_expiry(frm.doc.custom_visa_expiry_date, "Visa");
    evaluate_expiry(frm.doc.custom_iqama_expiry, "Iqama");
    evaluate_expiry(frm.doc.custom_medical_insurance_expiry, "Medical Insurance");

    // ===== SHOW SINGLE POPUP =====
    if (messages.length > 0) {
        frappe.msgprint({
            title: __("Document Expiry Alert"),
            message: messages.join("<br><br>"),
            indicator: has_expired ? "red" : "orange"
        });
    }
}