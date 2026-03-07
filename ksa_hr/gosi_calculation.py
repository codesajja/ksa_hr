import frappe

def calculate_gosi(doc, method):

    # Stop if nationality not set
    if not doc.custom_nationality_type:
        return

    # Get GOSI Settings
    settings = frappe.get_single("GOSI Settings")

    employee_percent = 0
    employer_percent = 0

    # Find correct percentage from settings table
    for row in settings.gosi_table:
        if row.employee_type == doc.custom_nationality_type:
            employee_percent = row.employee_percent
            employer_percent = row.employer_percent
            break

    # Components that should NOT be included in GOSI calculation
    exclude_components = [
        "EOS Benefit",
        "Leave Encashment"
    ]

    # Calculate GOSI base from earnings
    gosi_base = 0
    for earning in doc.earnings:
        if earning.salary_component not in exclude_components:
            gosi_base += earning.amount

    # Calculate GOSI amounts
    employee_gosi = gosi_base * employee_percent / 100
    employer_gosi = gosi_base * employer_percent / 100

    employee_found = False
    employer_found = False

    # Update existing deductions
    for d in doc.deductions:

        if d.salary_component == "GOSI - Employee":
            d.amount = employee_gosi
            employee_found = True

        if d.salary_component == "GOSI - Employer":
            d.amount = employer_gosi
            employer_found = True

    # Add deduction if missing
    if not employee_found:
        doc.append("deductions", {
            "salary_component": "GOSI - Employee",
            "amount": employee_gosi
        })

    if not employer_found:
        doc.append("deductions", {
            "salary_component": "GOSI - Employer",
            "amount": employer_gosi
        })