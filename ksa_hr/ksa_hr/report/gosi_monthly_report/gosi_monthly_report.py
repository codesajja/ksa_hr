import frappe

def execute(filters=None):

    filters = filters or {}

    columns = [
        {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 200},
        {"label": "Branch", "fieldname": "branch", "fieldtype": "Data", "width": 200},
        {"label": "Employee GOSI", "fieldname": "employee_gosi", "fieldtype": "Currency", "width": 150},
        {"label": "Employer GOSI", "fieldname": "employer_gosi", "fieldtype": "Currency", "width": 150},
        {"label": "Total GOSI", "fieldname": "total_gosi", "fieldtype": "Currency", "width": 150},
    ]

    conditions = ""
    values = {}

    if filters.get("company"):
        conditions += " AND ss.company = %(company)s"
        values["company"] = filters.get("company")

    if filters.get("branch"):
        conditions += " AND ss.branch = %(branch)s"
        values["branch"] = filters.get("branch")

    if filters.get("from_date"):
        conditions += " AND ss.start_date >= %(from_date)s"
        values["from_date"] = filters.get("from_date")

    if filters.get("to_date"):
        conditions += " AND ss.end_date <= %(to_date)s"
        values["to_date"] = filters.get("to_date")

    data = frappe.db.sql(f"""
        SELECT
            e.employee_name,
            ss.branch,

            SUM(CASE
                WHEN sd.salary_component = 'GOSI - Employee'
                THEN sd.amount ELSE 0 END) as employee_gosi,

            SUM(CASE
                WHEN sd.salary_component = 'GOSI - Employer'
                THEN sd.amount ELSE 0 END) as employer_gosi,

            SUM(CASE
                WHEN sd.salary_component IN ('GOSI - Employee','GOSI - Employer')
                THEN sd.amount ELSE 0 END) as total_gosi

        FROM `tabSalary Slip` ss

        JOIN `tabSalary Detail` sd
            ON ss.name = sd.parent

        LEFT JOIN `tabEmployee` e
            ON ss.employee = e.name

        WHERE ss.docstatus = 1 {conditions}

        GROUP BY ss.employee, ss.branch

        ORDER BY e.employee_name
    """, values, as_dict=True)

    return columns, data