
# import frappe

# def calculate_final_settlement(doc, method):
#     settlement_components = ["EOS Benefit", "Leave Encashment"]

#     # Always remove settlement components first (clean slate)
#     doc.earnings = [
#         e for e in doc.earnings
#         if e.salary_component not in settlement_components
#     ]

#     # Recalculate base gross (without settlement)
#     base_gross = sum(e.amount for e in doc.earnings)

#     # ---------- GET FISCAL YEAR ----------
#     fiscal_year = frappe.db.get_value(
#         "Fiscal Year",
#         {
#             "year_start_date": ["<=", doc.start_date],
#             "year_end_date": [">=", doc.end_date]
#         },
#         ["year_start_date", "year_end_date"],
#         as_dict=True
#     )

#     if not fiscal_year:
#         # Fallback: use calendar year
#         year = doc.start_date.year
#         fy_start = f"{year}-01-01"
#         fy_end = f"{year}-12-31"
#     else:
#         fy_start = fiscal_year.year_start_date
#         fy_end = fiscal_year.year_end_date

#     # ---------- SUM PREVIOUS SUBMITTED SLIPS (same employee, same fiscal year, exclude current) ----------
#     previous_gross = frappe.db.sql("""
#         SELECT COALESCE(SUM(gross_pay), 0)
#         FROM `tabSalary Slip`
#         WHERE employee = %s
#           AND docstatus = 1
#           AND start_date >= %s
#           AND end_date <= %s
#           AND name != %s
#     """, (doc.employee, fy_start, fy_end, doc.name))[0][0]

#     # ---------- FINAL SETTLEMENT OFF ----------
#     if not doc.custom_final_settlement:
#         doc.gross_pay = base_gross
#         doc.gross_year_to_date = base_gross + previous_gross
#         return

#     # ---------- FINAL SETTLEMENT ON ----------
#     employee = frappe.get_doc("Employee", doc.employee)

#     if not employee.date_of_joining or not employee.relieving_date:
#         doc.gross_pay = base_gross
#         doc.gross_year_to_date = base_gross + previous_gross
#         return

#     daily_salary = base_gross / 30

#     # Service duration
#     service_days = (employee.relieving_date - employee.date_of_joining).days
#     service_years = service_days / 365

#     # EOS calculation
#     if service_years <= 5:
#         eos = daily_salary * 15 * service_years
#     else:
#         eos = (daily_salary * 15 * 5) + (daily_salary * 30 * (service_years - 5))

#     # Add EOS row
#     doc.append("earnings", {
#         "salary_component": "EOS Benefit",
#         "amount": round(eos, 2)
#     })

#     # Get Leave Balance
#     leave_balance = frappe.db.get_value(
#         "Leave Allocation",
#         {
#             "employee": doc.employee,
#             "leave_type": "Annual Leave",
#             "docstatus": 1
#         },
#         "total_leaves_allocated"
#     ) or 0

#     leave_encashment = 0
#     if leave_balance:
#         leave_encashment = daily_salary * leave_balance
#         doc.append("earnings", {
#             "salary_component": "Leave Encashment",
#             "amount": round(leave_encashment, 2)
#         })

#     # Explicitly update gross pay totals
#     total_gross = base_gross + round(eos, 2) + round(leave_encashment, 2)
#     doc.gross_pay = total_gross
#     doc.gross_year_to_date = total_gross + previous_gross


import frappe
from frappe.utils import getdate

def calculate_final_settlement(doc, method):
    settlement_components = ["EOS Benefit", "Leave Encashment"]

    # Always remove settlement components first (clean slate)
    doc.earnings = [
        e for e in doc.earnings
        if e.salary_component not in settlement_components
    ]

    # Recalculate base gross (without settlement)
    base_gross = sum(e.amount for e in doc.earnings)

    # ---------- GET FISCAL YEAR ----------
    fiscal_year = frappe.db.get_value(
        "Fiscal Year",
        {
            "year_start_date": ["<=", doc.start_date],
            "year_end_date": [">=", doc.end_date]
        },
        ["year_start_date", "year_end_date"],
        as_dict=True
    )

    if not fiscal_year:
        year = doc.start_date.year
        fy_start = f"{year}-01-01"
        fy_end = f"{year}-12-31"
    else:
        fy_start = fiscal_year.year_start_date
        fy_end = fiscal_year.year_end_date

    # ---------- SUM PREVIOUS SUBMITTED SLIPS ----------
    previous_gross = frappe.db.sql("""
        SELECT COALESCE(SUM(gross_pay), 0)
        FROM `tabSalary Slip`
        WHERE employee = %s
          AND docstatus = 1
          AND start_date >= %s
          AND end_date <= %s
          AND name != %s
    """, (doc.employee, fy_start, fy_end, doc.name))[0][0]

    # ---------- FINAL SETTLEMENT OFF ----------
    if not doc.custom_final_settlement:
        doc.gross_pay = base_gross
        doc.gross_year_to_date = base_gross + previous_gross
        return

    # ---------- FINAL SETTLEMENT ON ----------
    employee = frappe.get_doc("Employee", doc.employee)

    if not employee.date_of_joining or not employee.relieving_date:
        doc.gross_pay = base_gross
        doc.gross_year_to_date = base_gross + previous_gross
        return

    doj = getdate(employee.date_of_joining)
    lwd = getdate(employee.relieving_date)

    years = (lwd - doj).days / 365
    basic = base_gross  # using base gross as the basic salary reference

    # KSA EOS Rule
    if years < 2:
        eos = 0
    elif years <= 5:
        eos = (basic / 2) * years
    else:
        eos = basic * years

    eos = round(eos, 2)

    # Add EOS row
    doc.append("earnings", {
        "salary_component": "EOS Benefit",
        "amount": eos
    })

    # Get Leave Balance
    leave_balance = frappe.db.get_value(
        "Leave Allocation",
        {
            "employee": doc.employee,
            "leave_type": "Annual Leave",
            "docstatus": 1
        },
        "total_leaves_allocated"
    ) or 0

    leave_encashment = 0
    if leave_balance:
        daily_salary = base_gross / 30
        leave_encashment = round(daily_salary * leave_balance, 2)
        doc.append("earnings", {
            "salary_component": "Leave Encashment",
            "amount": leave_encashment
        })

    # Explicitly update gross pay totals
    total_gross = base_gross + eos + leave_encashment
    doc.gross_pay = total_gross
    doc.gross_year_to_date = total_gross + previous_gross