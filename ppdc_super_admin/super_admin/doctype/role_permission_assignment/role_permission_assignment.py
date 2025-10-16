import frappe
from frappe.model.document import Document

class RolePermissionAssignment(Document):
    def validate(self):
        self.validate_duplicate_permissions()
    
    def validate_duplicate_permissions(self):
        for perm in self.role_permissions:
            count = 0
            for p in self.role_permissions:
                if p.permission == perm.permission:
                    count += 1
                if count > 1:
                    frappe.throw(f"Permission {perm.permission} is assigned multiple times")
    
    def on_update(self):
        self.sync_role_permissions()
    
    def sync_role_permissions(self):
        """Sync all permissions to the role"""
        role = frappe.get_doc("Role", self.role)
        permissions = []
        
        for perm in self.role_permissions:
            permission_doc = frappe.get_doc("Role Permission Master", perm.permission)
            permissions.append(permission_doc)
        
        # Clear existing permissions except system defaults
        role.permissions = [p for p in role.permissions if p.role == "System Manager"]
        
        # Assign new permissions
        for permission in permissions:
            role.append("permissions", {
                "select": 1,
                "read": 1,
                "write": permission.can_edit or 0,
                "create": permission.can_edit or 0,
                "delete": 0,
                "submit": 0,
                "cancel": 0,
                "amend": 0,
                "report": 1,
                "export": permission.can_export_data or 0
            })
        
        role.save(ignore_permissions=True)
        
        # Update all users with this role
        users = frappe.get_all("Has Role", filters={"role": self.role}, fields=["parent"])
        for user in users:
            frappe.clear_cache(user.parent)