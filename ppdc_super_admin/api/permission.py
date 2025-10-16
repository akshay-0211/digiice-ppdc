'EOF'
import frappe

def has_app_permission():
    """
    Permission check for PPDC Super Admin app
    Returns True if user has permission to access the app
    """
    # Allow all logged-in users for now
    # Later you can add role-based checks like:
    # return "Super Admin" in frappe.get_roles()
    return True
