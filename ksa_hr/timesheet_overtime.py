import frappe

def calculate_overtime(doc, method):
    standard_hours = 8
    total_ot = 0

    if not doc.time_logs:
        doc.custom_total_ot_hours = 0
        return

    for row in doc.time_logs:
        hrs = row.hours or 0

        if hrs > standard_hours:
            total_ot += (hrs - standard_hours)

    doc.custom_total_ot_hours = total_ot