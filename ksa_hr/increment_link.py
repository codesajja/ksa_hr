import frappe
from frappe.utils import nowdate


def apply_increment_on_submit(doc, method):
    """
    Link Appraisal to Increment.
    Creates Additional Salary based on final_score.
    """

    # 1️⃣ Validate score
    if not doc.final_score:
        return

    increment_percent = 0

    if doc.final_score >= 4:
        increment_percent = 10
    elif doc.final_score >= 3:
        increment_percent = 5
    else:
        return  # No increment


    # 2️⃣ Prevent duplicate increment for same appraisal
    existing = frappe.get_all(
        "Additional Salary",
        filters={
            "employee": doc.employee,
            "ref_doctype": "Appraisal",
            "ref_docname": doc.name,
            "docstatus": 1
        }
    )

    if existing:
        return


    # 3️⃣ Get active Salary Structure Assignment
    assignment = frappe.get_value(
        "Salary Structure Assignment",
        {"employee": doc.employee, "docstatus": 1},
        ["salary_structure"],
        as_dict=True
    )

    if not assignment:
        frappe.throw("No active Salary Structure Assignment found.")


    salary_structure = frappe.get_doc(
        "Salary Structure",
        assignment.salary_structure
    )


    # 4️⃣ Calculate total fixed earnings
    total_fixed = 0

    for row in salary_structure.earnings:
        if not row.formula:  # ignore formula-based components
            total_fixed += row.amount

    if total_fixed <= 0:
        frappe.throw("No fixed earnings found in Salary Structure.")


    # 5️⃣ Calculate increment amount
    increment_amount = (total_fixed * increment_percent) / 100


    # 6️⃣ Create Additional Salary
    additional_salary = frappe.get_doc({
        "doctype": "Additional Salary",
        "employee": doc.employee,
        "salary_component": "Increment",
        "amount": increment_amount,
        "payroll_date": nowdate(),
        "company": doc.company,
        "ref_doctype": "Appraisal",
        "ref_docname": doc.name
    })

    additional_salary.insert(ignore_permissions=True)
    additional_salary.submit()

    frappe.msgprint(
        f"{increment_percent}% increment applied successfully."
    )