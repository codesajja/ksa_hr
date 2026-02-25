import frappe

def create_employee_folder(doc, method):
    """Creates a private folder for the employee on first save"""
    folder_name = f"{doc.name} - {doc.employee_name}"
    parent_folder = "Home/Employee Documents"

    existing = frappe.db.exists("File", {
        "file_name": folder_name,
        "is_folder": 1,
        "folder": parent_folder
    })

    if not existing:
        folder = frappe.get_doc({
            "doctype": "File",
            "file_name": folder_name,
            "folder": parent_folder,
            "is_folder": 1,
            "is_private": 1
        })
        folder.insert(ignore_permissions=True)
        frappe.db.commit()

    move_employee_attachments(doc)


def move_employee_attachments(doc, method=None):
    """Moves any attached files to the employee's folder"""
    target_folder = f"Home/Employee Documents/{doc.name} - {doc.employee_name}"

    # Get ALL files attached to this employee regardless of field
    files = frappe.get_all("File", filters={
        "attached_to_doctype": "Employee",
        "attached_to_name": doc.name
    }, fields=["name", "folder"])

    for file in files:
        if file.folder != target_folder:
            f = frappe.get_doc("File", file["name"])
            f.folder = target_folder
            f.is_private = 1
            f.save(ignore_permissions=True)

    frappe.db.commit()