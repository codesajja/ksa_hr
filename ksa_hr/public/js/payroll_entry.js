frappe.ui.form.on("Payroll Entry", {
    refresh(frm) {

        if (frm.doc.docstatus === 1) {

            frm.add_custom_button("Generate WPS File", function () {

                window.open(
                    "/api/method/ksa_hr.wps_generator.generate_wps_file?payroll_entry=" + frm.doc.name
                );

            });

        }

    }
});