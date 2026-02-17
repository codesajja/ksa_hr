import frappe
from frappe.utils import today, add_days

def send_expiry_alerts():
    """Runs daily - alerts HR about Iqama & Insurance expiring in 30, 14, 7 days"""
    alert_days = [30, 14, 7]

    for days in alert_days:
        target_date = add_days(today(), days)

        employees = frappe.get_all(
            "Employee",
            filters={
                "iqama_expiry_date": target_date,
                "status": "Active"
            },
            fields=["name", "employee_name", "iqama_expiry_date", "user_id"]
        )

        for emp in employees:
            frappe.sendmail(
                recipients=[emp.user_id] if emp.user_id else [],
                subject=f"⚠️ Iqama Expiry Alert – {emp.employee_name}",
                message=f"""
                    Dear HR Team,<br><br>
                    Employee <b>{emp.employee_name}</b> ({emp.name})'s
                    <b>Iqama</b> is expiring on <b>{emp.iqama_expiry_date}</b>
                    — <b>{days} days remaining</b>.<br><br>
                    Please arrange renewal immediately.
                """
            )

        insured = frappe.get_all(
            "Employee",
            filters={
                "medical_insurance_expiry": target_date,
                "status": "Active"
            },
            fields=["name", "employee_name", "medical_insurance_expiry", "user_id"]
        )

        for emp in insured:
            frappe.sendmail(
                recipients=[emp.user_id] if emp.user_id else [],
                subject=f"⚠️ Medical Insurance Expiry Alert – {emp.employee_name}",
                message=f"""
                    Dear HR Team,<br><br>
                    Employee <b>{emp.employee_name}</b> ({emp.name})'s
                    <b>Medical Insurance</b> is expiring on
                    <b>{emp.medical_insurance_expiry}</b>
                    — <b>{days} days remaining</b>.<br><br>
                    Please renew immediately.
                """
            )