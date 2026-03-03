import frappe


def calculate_gosi(doc, method):
    if not doc.employee:
        return

    emp = frappe.get_doc("Employee", doc.employee)

    nationality = emp.custom_nationality_type
    if not nationality:
        return

    # Get Basic salary from earnings
    base_salary = 0
    for row in doc.earnings:
        if row.salary_component == "Basic":
            base_salary = row.amount
            break

    if base_salary == 0:
        return

    # Calculate GOSI
    if nationality == "Saudi":
        gosi_employee = base_salary * 0.10
        gosi_employer = base_salary * 0.12
    else:
        gosi_employee = 0
        gosi_employer = base_salary * 0.02

    # Ensure deduction rows exist
    deduction_map = {d.salary_component: d for d in doc.deductions}

    if "GOSI - Employee" not in deduction_map:
        doc.append("deductions", {
            "salary_component": "GOSI - Employee",
            "amount": gosi_employee
        })
    else:
        deduction_map["GOSI - Employee"].amount = gosi_employee

    if "GOSI - Employer" not in deduction_map:
        doc.append("deductions", {
            "salary_component": "GOSI - Employer",
            "amount": gosi_employer
        })
    else:
        deduction_map["GOSI - Employer"].amount = gosi_employer