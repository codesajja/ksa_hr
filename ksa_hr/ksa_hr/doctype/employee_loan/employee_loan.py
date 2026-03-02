import frappe
from frappe.model.document import Document


class EmployeeLoan(Document):
    pass


def on_submit(doc, method=None):
    """
    When Employee Loan is submitted,
    create Additional Salary automatically.
    """

    # Prevent duplicate Additional Salary
    existing = frappe.db.get_value(
        "Additional Salary",
        {"custom_employee_loan": doc.name},
        "name"
    )

    if existing:
        return

    additional_salary = frappe.new_doc("Additional Salary")
    additional_salary.employee = doc.employee
    additional_salary.salary_component = doc.salary_component
    additional_salary.amount = doc.monthly_installment
    additional_salary.payroll_date = doc.repayment_start_date
    additional_salary.company = frappe.defaults.get_user_default("Company")

    # 🔥 IMPORTANT: Use correct DB fieldname
    additional_salary.custom_employee_loan = doc.name

    additional_salary.insert(ignore_permissions=True)
    additional_salary.submit()


# 🔥 Used by JS to redirect safely
@frappe.whitelist()
def get_additional_salary_from_loan(loan_name):
    return frappe.db.get_value(
        "Additional Salary",
        {"custom_employee_loan": loan_name},
        "name"
    )