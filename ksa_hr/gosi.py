import frappe


def calculate_gosi(doc, method):
    if not doc.employee:
        return

    emp = frappe.get_doc("Employee", doc.employee)

    nationality = emp.custom_nationality_type
    if not nationality:
        return

    # GOSI based on total earnings
    base_salary = sum(row.amount for row in doc.earnings)

    if base_salary == 0:
        return

    if nationality == "Saudi":
        gosi_employee = base_salary * 0.10
        gosi_employer = base_salary * 0.12
    else:
        gosi_employee = 0
        gosi_employer = base_salary * 0.02

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