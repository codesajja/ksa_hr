import frappe

def calculate_final_settlement(doc, method):

    settlement_components = ["EOS Benefit", "Leave Encashment"]

    # ---------- FINAL SETTLEMENT OFF ----------
    if not getattr(doc, "custom_final_settlement", 0):

        for row in list(doc.earnings):
            if row.salary_component in settlement_components:
                doc.earnings.remove(row)

        doc.run_method("calculate_net_pay")

        # FIX YTD when settlement removed
        doc.gross_year_to_date = sum(e.amount for e in doc.earnings)

        return


    # ---------- FINAL SETTLEMENT ON ----------

    employee = frappe.get_doc("Employee", doc.employee)

    if not employee.date_of_joining or not employee.relieving_date:
        return


    base_salary = sum(
        e.amount for e in doc.earnings
        if e.salary_component not in settlement_components
    )

    daily_salary = base_salary / 30


    service_days = (employee.relieving_date - employee.date_of_joining).days
    service_years = service_days / 365


    if service_years <= 5:
        eos = daily_salary * 15 * service_years
    else:
        eos = (daily_salary * 15 * 5) + (daily_salary * 30 * (service_years - 5))


    # Remove old EOS
    for row in list(doc.earnings):
        if row.salary_component == "EOS Benefit":
            doc.earnings.remove(row)

    doc.append("earnings", {
        "salary_component": "EOS Benefit",
        "amount": eos
    })


    leave_balance = frappe.db.get_value(
        "Leave Allocation",
        {
            "employee": doc.employee,
            "leave_type": "Annual Leave",
            "docstatus": 1
        },
        "total_leaves_allocated"
    )

    if leave_balance:

        leave_encashment = daily_salary * leave_balance

        for row in list(doc.earnings):
            if row.salary_component == "Leave Encashment":
                doc.earnings.remove(row)

        doc.append("earnings", {
            "salary_component": "Leave Encashment",
            "amount": leave_encashment
        })


    doc.run_method("calculate_net_pay")

    # YTD should only include regular salary
    doc.gross_year_to_date = base_salary