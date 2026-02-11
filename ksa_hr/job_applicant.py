import frappe

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

        if missing:
            frappe.throw(
                "The following KSA verifications must be completed before accepting:<br><br>"
                + ", ".join(missing)
            )
