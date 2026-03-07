import frappe


def ensure_parent_folder():
    parent_folder = "Home/Employee Documents"

    if not frappe.db.exists("File", {
        "file_name": "Employee Documents",
        "is_folder": 1,
        "folder": "Home"
    }):

        frappe.get_doc({
            "doctype": "File",
            "file_name": "Employee Documents",
            "folder": "Home",
            "is_folder": 1,
            "is_private": 1
        }).insert(ignore_permissions=True)


def create_employee_folder(doc, method=None):
    """Create private folder for employee"""

    ensure_parent_folder()

    folder_name = f"{doc.name} - {doc.employee_name}"
    parent_folder = "Home/Employee Documents"

    if not frappe.db.exists("File", {
        "file_name": folder_name,
        "is_folder": 1,
        "folder": parent_folder
    }):

        frappe.get_doc({
            "doctype": "File",
            "file_name": folder_name,
            "folder": parent_folder,
            "is_folder": 1,
            "is_private": 1
        }).insert(ignore_permissions=True)

    move_employee_attachments(doc)


def move_employee_attachments(doc, method=None):

    target_folder = f"Home/Employee Documents/{doc.name} - {doc.employee_name}"

    files = frappe.get_all(
        "File",
        filters={
            "attached_to_doctype": "Employee",
            "attached_to_name": doc.name
        },
        fields=["name", "folder"]
    )

    for file in files:
        if file.folder != target_folder:
            frappe.db.set_value(
                "File",
                file.name,
                {
                    "folder": target_folder,
                    "is_private": 1
                }
            )