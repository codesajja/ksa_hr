# # import frappe
# # from frappe.utils import getdate

# # def apply_employee_loan_deduction(doc, method=None):

# #     if not doc.employee:
# #         return

# #     # Get submitted loan (docstatus = 1 means Approved)
# #     loan = frappe.get_all(
# #         "Employee Loan",
# #         filters={
# #             "employee": doc.employee,
# #             "docstatus": 1
# #         },
# #         fields=[
# #             "monthly_installment",
# #             "repayment_start_date",
# #             "salary_component"
# #         ],
# #         limit=1
# #     )

# #     if not loan:
# #         return

# #     loan = loan[0]

# #     if not loan.repayment_start_date:
# #         return

# #     if getdate(doc.start_date) < getdate(loan.repayment_start_date):
# #         return

# #     # Update deduction row
# #     for d in doc.deductions:
# #         if d.salary_component == loan.salary_component:
# #             d.amount = loan.monthly_installment
# #             d.default_amount = loan.monthly_installment

# #     doc.calculate_net_pay()

# import frappe
# from frappe.utils import nowdate, get_first_day, get_last_day


# @frappe.whitelist()
# def create_salary_slip_from_loan(loan_name):

#     loan = frappe.get_doc("Employee Loan", loan_name)

#     salary_slip = frappe.new_doc("Salary Slip")
#     salary_slip.employee = loan.employee
#     salary_slip.start_date = get_first_day(nowdate())
#     salary_slip.end_date = get_last_day(nowdate())
#     salary_slip.posting_date = nowdate()
#     salary_slip.employee_loan = loan.name

#     salary_slip.insert(ignore_permissions=True)

#     return salary_slip.name


# # 🔥 THIS WAS MISSING
# def apply_employee_loan_deduction(doc, method=None):

#     if not doc.employee_loan:
#         return

#     loan = frappe.get_doc("Employee Loan", doc.employee_loan)

#     # Remove old Employee Loan deduction rows
#     doc.deductions = [
#         d for d in doc.deductions
#         if d.salary_component != "Employee Loan"
#     ]

#     doc.append("deductions", {
#         "salary_component": "Employee Loan",
#         "amount": loan.monthly_installment
#     })

#     # Remove existing loan deduction if exists
#     doc.deductions = [
#         d for d in doc.deductions
#         if d.salary_component != "Employee Loan"
#     ]

#     doc.append("deductions", {
#         "salary_component": "Employee Loan",
#         "amount": loan.monthly_installment
#     })