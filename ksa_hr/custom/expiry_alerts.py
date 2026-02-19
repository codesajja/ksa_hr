import frappe
from frappe.utils import today, add_days

def send_expiry_alerts():
    """Runs daily - alerts HR about Iqama & Medical Insurance expiring in 30, 14, 7 days"""
    alert_days = [30, 14, 7]

    for days in alert_days:
        target_date = add_days(today(), days)

        employees = frappe.get_all(
            "Employee",
            filters={
                "custom_iqama_expiry_date": target_date,
                "status": "Active"
            },
            fields=[
                "name", 
                "employee_name", 
                "custom_iqama_expiry_date",
                "custom_iqama_no",
                "user_id"
            ]
        )

        for emp in employees:
            iqama_info = f"<br>Iqama No.: <b>{emp.custom_iqama_no}</b>" if emp.custom_iqama_no else ""
            
            frappe.sendmail(
                recipients=[emp.user_id] if emp.user_id else [],
                subject=f"⚠️ Iqama Expiry Alert – {emp.employee_name}",
                message=f"""
                    Dear HR Team,<br><br>
                    Employee <b>{emp.employee_name}</b> ({emp.name})'s
                    <b>Iqama</b> is expiring on <b>{emp.custom_iqama_expiry_date}</b>
                    — <b>{days} days remaining</b>.{iqama_info}<br><br>
                    Please arrange renewal immediately to ensure compliance with Saudi labor regulations.
                """
            )

        insured = frappe.get_all(
            "Employee",
            filters={
                "custom_medical_insurance_expiry": target_date,
                "status": "Active"
            },
            fields=[
                "name", 
                "employee_name", 
                "custom_medical_insurance_expiry", 
                "custom_insurance_provider",
                "custom_insurance_policy_number",
                "custom_medical_insurance_no",
                "user_id"
            ]
        )

        for emp in insured:
            provider_info = f"<br>Provider: <b>{emp.custom_insurance_provider}</b>" if emp.custom_insurance_provider else ""
            policy_info = f"<br>Policy No.: <b>{emp.custom_insurance_policy_number}</b>" if emp.custom_insurance_policy_number else ""
            insurance_no_info = f"<br>Insurance No.: <b>{emp.custom_medical_insurance_no}</b>" if emp.custom_medical_insurance_no else ""
            
            frappe.sendmail(
                recipients=[emp.user_id] if emp.user_id else [],
                subject=f"⚠️ Medical Insurance Expiry Alert – {emp.employee_name}",
                message=f"""
                    Dear HR Team,<br><br>
                    Employee <b>{emp.employee_name}</b> ({emp.name})'s
                    <b>Medical Insurance</b> is expiring on
                    <b>{emp.custom_medical_insurance_expiry}</b>
                    — <b>{days} days remaining</b>.{provider_info}{policy_info}{insurance_no_info}<br><br>
                    Please renew immediately to maintain mandatory coverage.
                """
            )