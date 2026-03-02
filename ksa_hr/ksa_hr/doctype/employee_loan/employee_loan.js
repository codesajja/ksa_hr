frappe.ui.form.on('Employee Loan', {
    refresh: function(frm) {

        // Only after submit
        if (frm.doc.docstatus === 1 && !frm._redirected) {

            frm._redirected = true;

            // Small delay to ensure backend finished
            setTimeout(function() {

                frappe.call({
                    method: "ksa_hr.ksa_hr.doctype.employee_loan.employee_loan.get_additional_salary_from_loan",
                    args: {
                        loan_name: frm.doc.name
                    },
                    callback: function(r) {
                        if (r.message) {

                            frappe.show_alert({
                                message: "Additional Salary Created Successfully",
                                indicator: "green"
                            });

                            frappe.set_route("Form", "Additional Salary", r.message);
                        }
                    }
                });

            }, 800);
        }
    }
});