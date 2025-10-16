import frappe
from frappe.model.document import Document
from frappe.utils import cstr

class RolePermissionMaster(Document):
    def validate(self):
        self.validate_permission_name()
        self.validate_permission_combinations()
    
    def validate_permission_name(self):
        """Ensure permission name is unique"""
        if frappe.db.exists("Role Permission Master", {
            "permission_name": self.permission_name,
            "name": ("!=", self.name)
        }):
            frappe.throw("Permission Name must be unique")
    
    def validate_permission_combinations(self):
        """Validate logical permission combinations"""
        # Edit access requires view access
        if self.can_edit_head_office and not self.can_view_head_office:
            frappe.throw("Cannot grant edit access without view access for Head Office")
        if self.can_edit_extension_center and not self.can_view_extension_center:
            frappe.throw("Cannot grant edit access without view access for Extension Center")
        if self.can_edit_efc and not self.can_view_efc:
            frappe.throw("Cannot grant edit access without view access for EFC")
        if self.can_edit_schemes and not self.can_view_schemes:
            frappe.throw("Cannot grant edit access without view access for Schemes")
        if self.can_edit_faculty and not self.can_view_faculty:
            frappe.throw("Cannot grant edit access without view access for Faculty")
        if self.can_edit_employees and not self.can_view_employees:
            frappe.throw("Cannot grant edit access without view access for Employees")
        if self.can_edit_reports and not self.can_view_reports:
            frappe.throw("Cannot grant edit access without view access for Reports")

    def assign_permissions_to_role(self, role_name, permissions=None):
        """
        Assign permissions to role with enhanced RBAC support
        Args:
            role_name: Name of the role to assign permissions to
            permissions: Optional list of specific permissions to assign
        """
        if not permissions:
            permissions = [self]

        role = frappe.get_doc("Role", role_name)
        doctype_permissions = {
            "Head Office": {"can_view": self.can_view_head_office, "can_edit": self.can_edit_head_office},
            "Extension Center": {"can_view": self.can_view_extension_center, "can_edit": self.can_edit_extension_center},
            "EFC": {"can_view": self.can_view_efc, "can_edit": self.can_edit_efc},
            "Scheme": {"can_view": self.can_view_schemes, "can_edit": self.can_edit_schemes},
            "Faculty": {"can_view": self.can_view_faculty, "can_edit": self.can_edit_faculty},
            "Employee": {"can_view": self.can_view_employees, "can_edit": self.can_edit_employees},
            "Reports": {"can_view": self.can_view_reports, "can_edit": self.can_edit_reports}
        }

        # Remove existing permissions
        existing_perms = frappe.get_all("Custom DocPerm", 
            filters={"role": role_name},
            fields=["name"]
        )
        for perm in existing_perms:
            frappe.delete_doc("Custom DocPerm", perm.name)

        # Assign new permissions
        for doctype, perms in doctype_permissions.items():
            if perms["can_view"] or perms["can_edit"]:
                self.create_doctype_permission(role, doctype, perms)

        # Special handling for administrative permissions
        if self.can_manage_users:
            self.setup_user_management_permissions(role)
        if self.can_manage_roles:
            self.setup_role_management_permissions(role)
        if self.can_approve_training:
            self.setup_training_permissions(role)

        role.save(ignore_permissions=True)

    def create_doctype_permission(self, role, doctype, perms):
        """Create DocPerm entry for a specific doctype"""
        role.append("permissions", {
            "select": 1,
            "read": perms["can_view"],
            "write": perms["can_edit"],
            "create": perms["can_edit"],
            "delete": perms["can_edit"],
            "submit": perms["can_edit"],
            "cancel": perms["can_edit"],
            "amend": perms["can_edit"],
            "report": perms["can_view"],
            "export": self.can_export_data,
            "print": perms["can_view"],
            "email": perms["can_view"],
            "share": perms["can_edit"],
            "doctype": doctype
        })

    def setup_user_management_permissions(self, role):
        """Setup permissions for user management"""
        user_doctypes = ["User", "Employee", "Role Permission Master"]
        for dt in user_doctypes:
            self.create_doctype_permission(role, dt, {
                "can_view": 1,
                "can_edit": 1
            })

    def setup_role_management_permissions(self, role):
        """Setup permissions for role management"""
        role_doctypes = ["Role", "Role Permission Master", "Role Permission Assignment"]
        for dt in role_doctypes:
            self.create_doctype_permission(role, dt, {
                "can_view": 1,
                "can_edit": 1
            })

    def setup_training_permissions(self, role):
        """Setup permissions for training approval"""
        training_doctypes = ["Training Program", "Training Request", "Training Approval"]
        for dt in training_doctypes:
            self.create_doctype_permission(role, dt, {
                "can_view": 1,
                "can_edit": 1
            })

    def after_insert(self):
        """After insert hook to sync permissions"""
        self.sync_role_permissions()
        self.create_role_profile()

    def on_update(self):
        """On update hook to sync permissions"""
        self.sync_role_permissions()
        self.update_role_profile()

    def sync_role_permissions(self):
        """Sync permissions with all roles that use this permission"""
        role_permissions = frappe.get_all("Role Permission Assignment", 
            filters={"permission": self.name},
            fields=["role"]
        )
        for rp in role_permissions:
            self.assign_permissions_to_role(rp.role)
            
    def create_role_profile(self):
        """Create a role profile for this permission set"""
        if not frappe.db.exists("Role Profile", self.permission_name):
            role_profile = frappe.new_doc("Role Profile")
            role_profile.role_profile = self.permission_name
            role_profile.description = self.permission_description
            role_profile.insert(ignore_permissions=True)

    def update_role_profile(self):
        """Update the role profile associated with this permission set"""
        if frappe.db.exists("Role Profile", self.permission_name):
            role_profile = frappe.get_doc("Role Profile", self.permission_name)
            role_profile.description = self.permission_description
            role_profile.save(ignore_permissions=True)

    @frappe.whitelist()
    def copy_from_template(self, template_name):
        """Copy permissions from a template"""
        if not template_name:
            frappe.throw("Template name is required")

        template = frappe.get_doc("Role Permission Master", template_name)
        
        # Copy all permission fields
        for field in self.meta.fields:
            if field.fieldtype == "Check" and field.fieldname.startswith("can_"):
                self.set(field.fieldname, template.get(field.fieldname))
        
        self.save()