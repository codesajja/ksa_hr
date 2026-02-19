import frappe
from frappe import _

def validate_job_applicant(doc, method):
    
    if doc.status == "Accepted":
        missing = []

        if not doc.custom_visa_valid:
            missing.append("Visa Valid")

        if not doc.custom_medical_test_completed:
            missing.append("Medical Test Completed")

        if not doc.custom_police_clearance_verified:
            missing.append("Police Clearance Verified")

        if not doc.custom_gosi_registration_completed:
            missing.append("GOSI Registration Completed")

        if not doc.custom_passport_copy:
            missing.append("Passport Copy")

        if not doc.custom_visa_copy:
            missing.append("Visa Copy")

        if not doc.custom_medical_report:
            missing.append("Medical Report")

        if not doc.custom_police_clearance_certificate:
            missing.append("Police Clearance Certificate")

        if missing:
            frappe.throw(
                _("The following KSA compliance verifications must be completed before accepting this applicant:<br><br>")
                + "<b>• " + "<br>• ".join(missing) + "</b>",
                title=_("KSA Recruitment Compliance Required")
            )