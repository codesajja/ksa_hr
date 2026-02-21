import frappe
from frappe.utils import today, add_days

def send_expiry_alerts():
    """Runs daily - Alerts for Iqama & Medical Insurance expiry"""

    alert_days = [15, 7, 3, 1, 0]

    for days in alert_days:
        target_date = add_days(today(), days)

      
        iqama_employees = frappe.get_all(
            "Employee",
            filters={
                "custom_iqama_expiry": target_date,
                "status": "Active"
            },
            fields=[
                "name",
                "employee_name",
                "custom_iqama_no",
                "custom_iqama_expiry",
                "user_id"
            ]
        )

        for emp in iqama_employees:
            iqama_info = f"<br>Iqama No: <b>{emp.custom_iqama_no}</b>" if emp.custom_iqama_no else ""

            frappe.sendmail(
                recipients=[emp.user_id] if emp.user_id else [],
                subject=f"⚠️ Iqama Expiry Alert – {emp.employee_name}",
                message=f"""
                    Dear HR Team,<br><br>
                    Employee <b>{emp.employee_name}</b> ({emp.name})'s
                    <b>Iqama</b> is expiring on
                    <b>{emp.custom_iqama_expiry}</b>
                    — <b>{days} days remaining</b>.{iqama_info}<br><br>
                    Please arrange renewal immediately to ensure compliance.
                """
            )

        
        insurance_employees = frappe.get_all(
            "Employee",
            filters={
                "custom_medical_insurance_expiry": target_date,
                "status": "Active"
            },
            fields=[
                "name",
                "employee_name",
                "custom_medical_insurance_no",
                "custom_medical_insurance_expiry",
                "custom_policy_no",
                "custom_insurance_provider",
                "custom_employee_share",
                "user_id"
            ]
        )

        for emp in insurance_employees:
            insurance_no = f"<br>Insurance No: <b>{emp.custom_medical_insurance_no}</b>" if emp.custom_medical_insurance_no else ""
            policy_info = f"<br>Policy No: <b>{emp.custom_policy_no}</b>" if emp.custom_policy_no else ""
            provider_info = f"<br>Provider: <b>{emp.custom_insurance_provider}</b>" if emp.custom_insurance_provider else ""
            share_info = f"<br>Employee Share: <b>{emp.custom_employee_share}</b>" if emp.custom_employee_share else ""

            frappe.sendmail(
                recipients=[emp.user_id] if emp.user_id else [],
                subject=f"⚠️ Medical Insurance Expiry Alert – {emp.employee_name}",
                message=f"""
                    Dear HR Team,<br><br>
                    Employee <b>{emp.employee_name}</b> ({emp.name})'s
                    <b>Medical Insurance</b> is expiring on
                    <b>{emp.custom_medical_insurance_expiry}</b>
                    — <b>{days} days remaining</b>.
                    {insurance_no}
                    {policy_info}
                    {provider_info}
                    {share_info}
                    <br><br>
                    Please renew immediately to maintain mandatory coverage.
                """
            )