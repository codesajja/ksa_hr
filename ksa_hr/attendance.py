import frappe
from datetime import datetime

def calculate_attendance_overtime(doc, method):

    # Standard hours rule
    if doc.custom_is_ramadan:
        standard_hours = 6
    else:
        standard_hours = 8

    doc.custom_standard_hours = standard_hours

    # Get checkins for that employee and date
    checkins = frappe.get_all(
        "Employee Checkin",
        filters={
            "employee": doc.employee,
            "time": ["between", [f"{doc.attendance_date} 00:00:00", f"{doc.attendance_date} 23:59:59"]]
        },
        fields=["time"],
        order_by="time asc"
    )

    if len(checkins) < 2:
        doc.custom_overtime_hours = 0
        return

    first_in = checkins[0].time
    last_out = checkins[-1].time

    working_hours = (last_out - first_in).total_seconds() / 3600

    if working_hours > standard_hours:
        doc.custom_overtime_hours = working_hours - standard_hours
    else:
        doc.custom_overtime_hours = 0