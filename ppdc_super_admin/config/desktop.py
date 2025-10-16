# config/desktop.py
from frappe import _

def get_data():
    return [
        {
            "module_name": "PPDC Super Admin",
            "color": "grey",
            "icon": "octicon octicon-file-directory",
            "type": "module",
            "label": _("PPDC Super Admin"),
            "category": "Modules"
        }
    ]