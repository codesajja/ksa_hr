import frappe
from frappe.utils import today, add_days

def send_expiry_alerts():
    """Runs daily - Alerts for Iqama & Medical Insurance expiry (in-app popups)"""

    alert_days = [15, 7, 3, 1, 0]

    for days in alert_days:
        target_date = add_days(today(), days)

        # ─── Iqama Alerts ───────────────────────────────────────────
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
            if not emp.user_id:
                continue

            iqama_info = f" | Iqama No: {emp.custom_iqama_no}" if emp.custom_iqama_no else ""

            frappe.publish_realtime(
                event="msgprint",
                message=f"⚠️ Iqama Expiry Alert: {emp.employee_name} ({emp.name})'s Iqama is expiring on {emp.custom_iqama_expiry} — {days} days remaining.{iqama_info} Please arrange renewal immediately.",
                user=emp.user_id
            )

            # Also create a persistent in-app notification in the bell icon
            notification = frappe.get_doc({
                "doctype": "Notification Log",
                "subject": f"⚠️ Iqama Expiry – {emp.employee_name} ({days} days remaining)",
                "email_content": (
                    f"Employee <b>{emp.employee_name}</b> ({emp.name})'s Iqama is expiring on "
                    f"<b>{emp.custom_iqama_expiry}</b> — <b>{days} days remaining</b>."
                    + (f"<br>Iqama No: <b>{emp.custom_iqama_no}</b>" if emp.custom_iqama_no else "")
                    + "<br>Please arrange renewal immediately to ensure compliance."
                ),
                "for_user": emp.user_id,
                "type": "Alert",
                "document_type": "Employee",
                "document_name": emp.name,
            })
            notification.insert(ignore_permissions=True)

        # ─── Medical Insurance Alerts ────────────────────────────────
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
            if not emp.user_id:
                continue

            # Build detail string for the popup
            details = []
            if emp.custom_medical_insurance_no:
                details.append(f"Insurance No: {emp.custom_medical_insurance_no}")
            if emp.custom_policy_no:
                details.append(f"Policy No: {emp.custom_policy_no}")
            if emp.custom_insurance_provider:
                details.append(f"Provider: {emp.custom_insurance_provider}")
            if emp.custom_employee_share:
                details.append(f"Employee Share: {emp.custom_employee_share}")

            detail_str = " | ".join(details)

            frappe.publish_realtime(
                event="msgprint",
                message=f"⚠️ Medical Insurance Expiry Alert: {emp.employee_name} ({emp.name})'s Medical Insurance is expiring on {emp.custom_medical_insurance_expiry} — {days} days remaining. {detail_str} Please renew immediately.",
                user=emp.user_id
            )

            # Build HTML content for the bell icon notification
            content_parts = (
                f"Employee <b>{emp.employee_name}</b> ({emp.name})'s Medical Insurance is expiring on "
                f"<b>{emp.custom_medical_insurance_expiry}</b> — <b>{days} days remaining</b>."
            )
            if emp.custom_medical_insurance_no:
                content_parts += f"<br>Insurance No: <b>{emp.custom_medical_insurance_no}</b>"
            if emp.custom_policy_no:
                content_parts += f"<br>Policy No: <b>{emp.custom_policy_no}</b>"
            if emp.custom_insurance_provider:
                content_parts += f"<br>Provider: <b>{emp.custom_insurance_provider}</b>"
            if emp.custom_employee_share:
                content_parts += f"<br>Employee Share: <b>{emp.custom_employee_share}</b>"
            content_parts += "<br>Please renew immediately to maintain mandatory coverage."

            notification = frappe.get_doc({
                "doctype": "Notification Log",
                "subject": f"⚠️ Medical Insurance Expiry – {emp.employee_name} ({days} days remaining)",
                "email_content": content_parts,
                "for_user": emp.user_id,
                "type": "Alert",
                "document_type": "Employee",
                "document_name": emp.name,
            })
            notification.insert(ignore_permissions=True)

    frappe.db.commit()