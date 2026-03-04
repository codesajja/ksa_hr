# Copyright (c) 2026, Prajakta and contributors
# For license information, please see license.txt

# import frappe

import frappe

def execute(filters=None):

    filters = filters or {}
    conditions = " WHERE status = 'Active' "
    values = {}

    if filters.get("company"):
        conditions += " AND company = %(company)s"
        values["company"] = filters.get("company")

    if filters.get("branch"):
        conditions += " AND branch = %(branch)s"
        values["branch"] = filters.get("branch")

    if filters.get("department"):
        conditions += " AND department = %(department)s"
        values["department"] = filters.get("department")

    data = frappe.db.sql(f"""
        SELECT
            department,
            branch,
            COUNT(name) as total_employees,
            SUM(CASE WHEN custom_nationality_type = 'Saudi' THEN 1 ELSE 0 END) as saudi_employees
        FROM `tabEmployee`
        {conditions}
        GROUP BY department, branch
    """, values, as_dict=True)

    for row in data:
        if row.total_employees:
            percentage = (row.saudi_employees / row.total_employees) * 100
            row["saudization_percentage"] = round(percentage, 2)
        else:
            row["saudization_percentage"] = 0

    columns = [
        {"label": "Department", "fieldname": "department", "fieldtype": "Link", "options": "Department"},
        {"label": "Branch", "fieldname": "branch", "fieldtype": "Link", "options": "Branch"},
        {"label": "Total Employees", "fieldname": "total_employees", "fieldtype": "Int"},
        {"label": "Saudi Employees", "fieldname": "saudi_employees", "fieldtype": "Int"},
        {"label": "Saudization %", "fieldname": "saudization_percentage", "fieldtype": "Percent"},
    ]

    return columns, data