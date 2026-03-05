import frappe
import csv
from io import StringIO


@frappe.whitelist()
def generate_wps_file(payroll_entry):

    payroll = frappe.get_doc("Payroll Entry", payroll_entry)

    output = StringIO()
    writer = csv.writer(output)

    # CSV Header
    writer.writerow([
        "Employee ID",
        "Employee Name",
        "IBAN",
        "Gross Salary",
        "Total Deduction",
        "Net Salary",
        "Payment Date"
    ])

    salary_slips = frappe.get_all(
        "Salary Slip",
        filters={"payroll_entry": payroll_entry},
        fields=[
            "employee",
            "employee_name",
            "bank_account_no",
            "gross_pay",
            "total_deduction",
            "net_pay"
        ]
    )

    for slip in salary_slips:

        writer.writerow([
            slip.employee,
            slip.employee_name,
            slip.bank_account_no,
            slip.gross_pay,
            slip.total_deduction,
            slip.net_pay,
            payroll.posting_date
        ])

    frappe.response["filename"] = "wps_salary.csv"
    frappe.response["filecontent"] = output.getvalue()
    frappe.response["type"] = "download"