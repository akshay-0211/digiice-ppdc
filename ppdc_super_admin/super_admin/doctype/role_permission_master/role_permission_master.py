import frappe
from frappe.model.document import Document

class RolePermissionMaster(Document):
    def validate(self):
        self.validate_permission_name()
    
    def validate_permission_name(self):
        if frappe.db.exists("Role Permission Master", {
            "permission_name": self.permission_name,
            "name": ("!=", self.name)
        }):
            frappe.throw("Permission Name must be unique")

    def assign_permissions_to_role(self, role_name, permissions):
        """Assign permissions to role"""
        role = frappe.get_doc("Role", role_name)
        for perm in permissions:
            if not frappe.db.exists("Custom DocPerm", {
                "parent": role.name,
                "permlevel": 0,
                "role": role.name
            }):
                role.append("permissions", {
                    "select": 1,
                    "read": 1,
                    "write": perm.get("can_edit", 0),
                    "create": perm.get("can_edit", 0),
                    "delete": 0,
                    "submit": 0,
                    "cancel": 0,
                    "amend": 0,
                    "report": 1,
                    "export": perm.get("can_export_data", 0),
                })
        role.save(ignore_permissions=True)

    def after_insert(self):
        """After insert hook to sync permissions"""
        self.sync_role_permissions()

    def on_update(self):
        """On update hook to sync permissions"""
        self.sync_role_permissions()

    def sync_role_permissions(self):
        """Sync permissions with all roles that use this permission"""
        role_permissions = frappe.get_all("Role Permission Assignment", 
            filters={"permission": self.name},
            fields=["role"]
        )
        for rp in role_permissions:
            self.assign_permissions_to_role(rp.role, [self])