from typing import Dict, List, Optional, Any, TypedDict, Union, cast
import frappe
from frappe.model.document import Document
from frappe.types import DF

class RolePermissionDocument(TypedDict):
    permission_name: str
    can_view_head_office: bool
    can_edit_head_office: bool
    can_view_extension_center: bool
    can_edit_extension_center: bool
    can_view_efc: bool
    can_edit_efc: bool
    can_view_schemes: bool
    can_edit_schemes: bool
    can_view_faculty: bool
    can_edit_faculty: bool
    can_view_employees: bool
    can_edit_employees: bool
    can_view_reports: bool
    can_edit_reports: bool
    can_approve_training: bool
    can_export_data: bool
    can_manage_users: bool
    can_manage_roles: bool

class Permission(TypedDict):
    permission: str

class DocPerm(TypedDict):
    doctype: str
    select: int
    read: int
    write: int
    create: int
    delete: int
    submit: int
    cancel: int
    amend: int
    report: int
    export: int
    share: int
    print: int
    email: int

class PermissionChanges(TypedDict):
    added: Dict[str, bool]
    removed: Dict[str, bool]
    modified: Dict[str, Dict[str, bool]]

class RolePermissionAssignment(Document):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(RolePermissionAssignment, self).__init__(*args, **kwargs)
        
        # Initialize document attributes with proper types
        self.name: str = kwargs.get("name", "")
        self.role: str = kwargs.get("role", "")
        self.role_permissions: List[Permission] = kwargs.get("role_permissions", [])
    
    def validate(self) -> None:
        """Validate the role permission assignment"""
        self.validate_duplicate_permissions()
        self.validate_role_conflicts()
        self.validate_permission_dependencies()
    
    def validate_duplicate_permissions(self) -> None:
        """Ensure no duplicate permissions are assigned"""
        permissions_seen: set = set()
        role_perms = cast(List[Permission], self.get("role_permissions", []))
        
        for perm_row in role_perms:
            perm_name = perm_row.get("permission", "")
            if perm_name in permissions_seen:
                frappe.throw(f"Permission {perm_name} is assigned multiple times")
            permissions_seen.add(perm_name)
    
    def validate_role_conflicts(self) -> None:
        """Check for conflicting role combinations"""
        role_perms = cast(List[Permission], self.get("role_permissions", []))
        perm_list = [p.get("permission", "") for p in role_perms]
        
        # Check for admin/user conflict
        if "Administrator" in perm_list and "User" in perm_list:
            frappe.throw("Cannot combine Administrator and User permissions")
            
        # Check for system manager modifications
        role = cast(str, self.get("role"))
        if role == "System Manager":
            frappe.throw("Cannot modify System Manager permissions")

    def validate_permission_dependencies(self) -> None:
        """Validate permission dependencies"""
        role_perms = cast(List[Permission], self.get("role_permissions", []))
        for perm_row in role_perms:
            permission_doc = frappe.get_doc("Role Permission Master", perm_row.get("permission", ""))
            perm_doc = cast(RolePermissionDocument, permission_doc)
            
            # Check module dependencies
            if perm_doc["can_edit_head_office"] and not perm_doc["can_view_head_office"]:
                frappe.throw(f"Permission {perm_row.get('permission')} requires View Head Office access for Edit access")
                
            # Check other module dependencies
            self.check_module_dependencies(perm_doc)
    
    def check_module_dependencies(self, permission_doc: RolePermissionDocument) -> None:
        """Check dependencies between different modules"""
        modules = [
            ("head_office", "Head Office"),
            ("extension_center", "Extension Center"),
            ("efc", "EFC"),
            ("schemes", "Schemes"),
            ("faculty", "Faculty"),
            ("employees", "Employees"),
            ("reports", "Reports")
        ]
        
        for module, label in modules:
            view_perm = f"can_view_{module}"
            edit_perm = f"can_edit_{module}"
            
            has_view = permission_doc.get(view_perm, False)
            has_edit = permission_doc.get(edit_perm, False)
            
            if has_edit and not has_view:
                frappe.throw(f"Permission {permission_doc['permission_name']} requires View {label} access for Edit access")
    
    def on_update(self) -> None:
        """On update hook"""
        self.sync_role_permissions()
        self.update_user_permissions()
    
    def sync_role_permissions(self) -> None:
        """Sync all permissions to the role"""
        role = frappe.get_doc("Role", self.get("role"))
        permissions: List[RolePermissionDocument] = []
        
        # Get all permission documents
        role_perms = cast(List[Permission], self.get("role_permissions", []))
        for perm_row in role_perms:
            permission_doc = frappe.get_doc("Role Permission Master", perm_row.get("permission", ""))
            permissions.append(cast(RolePermissionDocument, permission_doc))
        
        # Clear existing custom permissions
        custom_perms = frappe.get_all(
            "Custom DocPerm", 
            filters={"role": self.get("role")},
            fields=["name"]
        )
        for perm in custom_perms:
            frappe.delete_doc("Custom DocPerm", perm.name)
        
        # Merge and apply permissions
        effective_perms = self.get_effective_permissions(permissions)
        self.apply_effective_permissions(role, effective_perms)
        
        role.save(ignore_permissions=True)
    
    def get_effective_permissions(self, permissions: List[RolePermissionDocument]) -> Dict[str, bool]:
        """Calculate effective permissions from all assigned permissions"""
        effective: Dict[str, bool] = {
            "can_view_head_office": False,
            "can_edit_head_office": False,
            "can_view_extension_center": False,
            "can_edit_extension_center": False,
            "can_view_efc": False,
            "can_edit_efc": False,
            "can_view_schemes": False,
            "can_edit_schemes": False,
            "can_view_faculty": False,
            "can_edit_faculty": False,
            "can_view_employees": False,
            "can_edit_employees": False,
            "can_view_reports": False,
            "can_edit_reports": False,
            "can_approve_training": False,
            "can_export_data": False,
            "can_manage_users": False,
            "can_manage_roles": False
        }
        
        # Merge permissions using OR logic
        for permission in permissions:
            for perm_key in effective:
                if perm_key in permission:
                    effective[perm_key] = effective[perm_key] or permission.get(perm_key, False)
        
        return effective
    
    def apply_effective_permissions(self, role: Document, effective_perms: Dict[str, bool]) -> None:
        """Apply effective permissions to the role"""
        # Map of doctypes to their permission fields
        doctype_perms = {
            "Head Office": ("can_view_head_office", "can_edit_head_office"),
            "Extension Center": ("can_view_extension_center", "can_edit_extension_center"),
            "EFC": ("can_view_efc", "can_edit_efc"),
            "Scheme": ("can_view_schemes", "can_edit_schemes"),
            "Faculty": ("can_view_faculty", "can_edit_faculty"),
            "Employee": ("can_view_employees", "can_edit_employees"),
            "Report": ("can_view_reports", "can_edit_reports")
        }
        
        # Apply permissions for each doctype
        for doctype, (view_perm, edit_perm) in doctype_perms.items():
            if effective_perms.get(view_perm, False) or effective_perms.get(edit_perm, False):
                perm_dict: DocPerm = {
                    "doctype": doctype,
                    "select": 1,
                    "read": 1 if effective_perms.get(view_perm, False) else 0,
                    "write": 1 if effective_perms.get(edit_perm, False) else 0,
                    "create": 1 if effective_perms.get(edit_perm, False) else 0,
                    "delete": 1 if effective_perms.get(edit_perm, False) else 0,
                    "submit": 1 if effective_perms.get(edit_perm, False) else 0,
                    "cancel": 1 if effective_perms.get(edit_perm, False) else 0,
                    "amend": 1 if effective_perms.get(edit_perm, False) else 0,
                    "report": 1 if effective_perms.get(view_perm, False) else 0,
                    "export": 1 if effective_perms.get("can_export_data", False) else 0,
                    "share": 1 if effective_perms.get(edit_perm, False) else 0,
                    "print": 1 if effective_perms.get(view_perm, False) else 0,
                    "email": 1 if effective_perms.get(view_perm, False) else 0
                }
                role.append("permissions", perm_dict)
        
        # Apply special permissions
        if effective_perms.get("can_manage_users", False):
            self.setup_user_management_permissions(role)
        if effective_perms.get("can_manage_roles", False):
            self.setup_role_management_permissions(role)
        if effective_perms.get("can_approve_training", False):
            self.setup_training_permissions(role)
    
    def setup_user_management_permissions(self, role: Document) -> None:
        """Setup user management permissions"""
        user_doctypes = ["User", "Employee", "Role Permission Master"]
        for dt in user_doctypes:
            perm_dict: DocPerm = {
                "doctype": dt,
                "select": 1,
                "read": 1,
                "write": 1,
                "create": 1,
                "delete": 1,
                "submit": 0,
                "cancel": 0,
                "amend": 0,
                "report": 1,
                "export": 1,
                "share": 1,
                "print": 1,
                "email": 1
            }
            role.append("permissions", perm_dict)
    
    def setup_role_management_permissions(self, role: Document) -> None:
        """Setup role management permissions"""
        role_doctypes = ["Role", "Role Permission Master", "Role Permission Assignment"]
        for dt in role_doctypes:
            perm_dict: DocPerm = {
                "doctype": dt,
                "select": 1,
                "read": 1,
                "write": 1,
                "create": 1,
                "delete": 1,
                "submit": 0,
                "cancel": 0,
                "amend": 0,
                "report": 1,
                "export": 1,
                "share": 1,
                "print": 1,
                "email": 1
            }
            role.append("permissions", perm_dict)
    
    def setup_training_permissions(self, role: Document) -> None:
        """Setup training approval permissions"""
        training_doctypes = ["Training Program", "Training Request", "Training Approval"]
        for dt in training_doctypes:
            perm_dict: DocPerm = {
                "doctype": dt,
                "select": 1,
                "read": 1,
                "write": 1,
                "create": 1,
                "delete": 0,
                "submit": 1,
                "cancel": 1,
                "amend": 1,
                "report": 1,
                "export": 1,
                "share": 1,
                "print": 1,
                "email": 1
            }
            role.append("permissions", perm_dict)
    
    def update_user_permissions(self) -> None:
        """Update permissions for all users with this role"""
        users = frappe.get_all(
            "Has Role",
            filters={"role": self.get("role")},
            fields=["parent as user"]
        )
        
        for user in users:
            # Clear permission cache
            frappe.clear_cache(user.user)
            
            # Rebuild user permissions
            frappe.permissions.add_user_permission(
                "Role Permission Assignment",
                cast(str, self.name),
                user.user
            )
    
    @frappe.whitelist()
    def get_affected_users(self) -> List[Dict[str, str]]:
        """Get list of users affected by this permission change"""
        return frappe.get_all(
            "Has Role",
            filters={"role": self.get("role")},
            fields=["parent as user", "parenttype"],
            as_list=False
        )
    
    @frappe.whitelist()
    def preview_permission_changes(self) -> PermissionChanges:
        """Preview the effect of permission changes"""
        old_permissions = self.get_current_permissions()
        new_permissions = self.get_effective_permissions([
            cast(RolePermissionDocument, frappe.get_doc("Role Permission Master", p.get("permission", "")))
            for p in cast(List[Permission], self.get("role_permissions", []))
        ])
        
        changes: PermissionChanges = {
            "added": {},
            "removed": {},
            "modified": {}
        }
        
        for perm in new_permissions:
            if perm not in old_permissions:
                changes["added"][perm] = new_permissions[perm]
            elif old_permissions[perm] != new_permissions[perm]:
                changes["modified"][perm] = {
                    "old": old_permissions[perm],
                    "new": new_permissions[perm]
                }
        
        for perm in old_permissions:
            if perm not in new_permissions:
                changes["removed"][perm] = old_permissions[perm]
        
        return changes
    
    def get_current_permissions(self) -> Dict[str, bool]:
        """Get current effective permissions"""
        if not frappe.db.exists("Role Permission Assignment", self.name):
            return {}
            
        old_doc = frappe.get_doc("Role Permission Assignment", cast(str, self.name))
        role_perms = cast(List[Permission], getattr(old_doc, "role_permissions", []))
        
        return self.get_effective_permissions([
            cast(RolePermissionDocument, frappe.get_doc("Role Permission Master", p.get("permission", "")))
            for p in role_perms
        ])