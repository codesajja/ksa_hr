import frappe
import csv
from io import StringIO

@frappe.whitelist()
def generate_wps_file(payroll_entry):

    payroll = frappe.get_doc("Payroll Entry", payroll_entry)
    company = frappe.get_doc("Company", payroll.company)

    output = StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "Employee ID",
        "Bank Account",
        "Iqama No",
        "Net Salary",
        "Payment Date",
        "Employer ID"
    ])

    salary_slips = frappe.get_all(
        "Salary Slip",
        filters={"payroll_entry": payroll_entry},
        fields=["employee","bank_account_no","net_pay"]
    )

    for slip in salary_slips:

        employee = frappe.get_doc("Employee", slip.employee)

        writer.writerow([
            slip.employee,
            slip.bank_account_no,
            employee.custom_iqama_no,
            slip.net_pay,
            payroll.posting_date,
            company.tax_id
        ])

    frappe.response["filename"] = "wps_salary.csv"
    frappe.response["filecontent"] = output.getvalue()
    frappe.response["type"] = "download"