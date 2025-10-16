# Copyright (c) 2025, Digiice Development Team and contributors
# For license information, please see license.txt

from typing import Dict, List, Optional, Any, TypedDict, Union, cast
import frappe
from frappe.model.document import Document
from frappe.types import DF
from frappe import _

class EmployeeRole(TypedDict):
    role: str
    permission: str
    permission_description: str

class User(Document):
    enabled: bool
    roles: List[Dict[str, str]]
    email: str
    first_name: str
    username: str
    name: str
    user_type: str
    
    def add_roles(self, *roles: str) -> None: ...

class EmployeeMaster(Document):
    # Document fields
    name: str
    employee_name: str
    employee_code: str
    employee_type: str
    designation: str
    contact_number: str
    email: str
    user: Optional[str]
    role: Optional[str]
    is_active: bool
    employee_roles: List[EmployeeRole]
    
    def validate(self) -> None:
        if self.user and not self.email:
            frappe.throw(_("Email is required for user creation"))
        
        if self.email and not frappe.utils.validate_email_address(self.email):
            frappe.throw(_("Invalid email address"))
            
    def before_save(self):
        if not self.user and self.email:
            self.create_user()
            
    def create_user(self):
        try:
            # Check if user exists
            existing_user = frappe.db.exists("User", self.email)
            if existing_user:
                # Reactivate and reset existing user
                user = frappe.get_doc("User", self.email)
                user.enabled = 1
                
                # Clear existing password reset key
                user.db_set('reset_password_key', '')
                frappe.db.commit()
                
                user.save(ignore_permissions=True)
            else:
                # Create new user
                user = frappe.get_doc({
                    "doctype": "User",
                    "email": self.email,
                    "first_name": self.employee_name,
                    "username": self.employee_code,
                    "enabled": 1,
                    "send_welcome_email": 0,
                    "user_type": "System User",
                })
                user.insert(ignore_permissions=True)
        
            # Generate new reset key
            reset_key = user.reset_password()
            url = frappe.utils.get_url()
            reset_url = f"{url}/update-password?key={reset_key}"
            
            # Send welcome email with reset link
            frappe.sendmail(
                recipients=[self.email],
                subject="Welcome to Vigility Technologies (Demo)",
                message=f"""
                Hello {self.employee_name},
                
                Your account has been {['created', 'reactivated'][bool(existing_user)]} at {url}.
                Your login id is: {self.email}
                
                Click on the link below to set your password (valid for 24 hours):
                {reset_url}
                
                Note: This password reset link can only be used once.
                
                Best regards,
                Team Vigility
                """,
                now=True,
                reference_doctype="User",
                reference_name=user.name
            )
            
            # Update employee document and assign role
            self.user = user.name
            self.assign_default_role(user.name)
            
            frappe.msgprint(_(
                "User {0} {1} successfully. Welcome email sent with password reset link."
            ).format(user.name, ['created', 'reactivated'][bool(existing_user)]))
            
        except Exception as e:
            frappe.log_error(f"User setup failed: {str(e)}")
            frappe.throw(_("Could not setup user: {0}").format(str(e)))

    def assign_default_role(self, user_name):
        try:
            # First check if a specific role is assigned
            if self.role:
                role_name = self.role
            else:
                # Use default role mapping if no specific role
                role_mapping = {
                    "Officer": "PPDC Officer",
                    "Ad-hoc": "PPDC Staff",
                    "Contract": "PPDC Staff",
                    "OJT": "PPDC Trainee",
                    "Temp": "PPDC Staff",
                    "Retired": "PPDC Consultant"
                }
                
                if self.employee_type in role_mapping:
                    role_name = role_mapping[self.employee_type]
                else:
                    role_name = "PPDC Staff"  # Default fallback role
            
            # Create role if it doesn't exist
            if not frappe.db.exists("Role", role_name):
                new_role = frappe.get_doc({
                    "doctype": "Role",
                    "role_name": role_name,
                    "desk_access": 1
                })
                new_role.insert(ignore_permissions=True)
            
            # Assign role to user
            user = frappe.get_doc("User", user_name)
            user.add_roles(role_name)
            
            # Apply any role permissions from Role Permission Master
            role_permissions = frappe.get_all(
                "Role Permission Master",
                filters={"permission_name": role_name},
                fields=["name"]
            )
            
            if role_permissions:
                for rp in role_permissions:
                    perm_doc = frappe.get_doc("Role Permission Master", rp.name)
                    perm_doc.apply_permissions_to_role(role_name)
            
            # Handle additional role assignments from employee_roles
            if self.employee_roles:
                for role_row in self.employee_roles:
                    if role_row.role != role_name:  # Avoid duplicate assignment
                        user.add_roles(role_row.role)
                        # Apply role permissions for additional roles
                        add_role_perms = frappe.get_all(
                            "Role Permission Master",
                            filters={"permission_name": role_row.role},
                            fields=["name"]
                        )
                        for rp in add_role_perms:
                            perm_doc = frappe.get_doc("Role Permission Master", rp.name)
                            perm_doc.apply_permissions_to_role(role_row.role)
            
            user.save(ignore_permissions=True)
            frappe.db.commit()
            
            msg = f"Role {role_name} assigned to user {user_name}"
            if self.employee_roles:
                additional_roles = ", ".join([r.role for r in self.employee_roles if r.role != role_name])
                if additional_roles:
                    msg += f" with additional roles: {additional_roles}"
            
            frappe.msgprint(msg)
                
        except Exception as e:
            frappe.log_error(f"Role assignment failed: {str(e)}")
            frappe.throw(f"Could not assign role: {str(e)}")

    def assign_role_with_permissions(self, user_name, role_name):
        try:
            # Ensure role exists
            if not frappe.db.exists("Role", role_name):
                role = frappe.get_doc({
                    "doctype": "Role",
                    "role_name": role_name,
                    "desk_access": 1
                }).insert()
            
            # Assign role to user
            user = frappe.get_doc("User", user_name)
            user.add_roles(role_name)
            
            # Sync permissions from Role Permission Master
            self.sync_role_permissions(role_name)
            
        except Exception as e:
            frappe.log_error(f"Role assignment failed: {str(e)}")

    def sync_role_permissions(self, role_name):
        permissions = frappe.get_all("Role Permission Assignment",
            filters={"role": role_name},
            fields=["permission"]
        )
        
        for perm in permissions:
            permission_doc = frappe.get_doc("Role Permission Master", perm.permission)
            permission_doc.apply_permissions_to_role(role_name)
            
    def on_trash(self):
        """Handle employee deletion"""
        if self.user:
            try:
                # Don't delete user, just disable
                user = frappe.get_doc("User", self.user)
                user.enabled = 0
                user.save(ignore_permissions=True)
                frappe.msgprint(_("User {0} has been disabled").format(self.user))
            except Exception as e:
                frappe.log_error(f"Failed to disable user: {str(e)}")


import frappe

def after_save(self, method):
    # Create User if not linked
    if not self.user:
        user_email = self.email or f"{self.employee_code}@dummy.localdomain"
        username = self.employee_code or self.employee_name.replace(" ", "").lower()
        if not frappe.db.exists("User", user_email):
            user_doc = frappe.get_doc({
                "doctype": "User",
                "email": user_email,
                "first_name": self.employee_name,
                "username": username,
                "enabled": 1
            })
            user_doc.insert(ignore_permissions=True)
            self.user = user_doc.name
            frappe.db.set_value(self.doctype, self.name, "user", self.user)
            pass

    # Sync roles assigned to user from Employee Role
    if self.user and self.employee_roles:
        assign_roles_to_user(self.user, self.employee_roles)

def assign_roles_to_user(user: str, employee_roles: Union[str, List[EmployeeRole], None]) -> None:
    user_doc = cast(User, frappe.get_doc("User", user))
    
    # Retain 'System Manager' role and override others
    existing_roles = [r for r in user_doc.roles if r.get("role") == "System Manager"]
    user_doc.set("roles", existing_roles)
    
    # Handle role assignments
    if employee_roles:
        if isinstance(employee_roles, str):
            user_doc.append("roles", {"role": employee_roles, "parenttype": "User"})
        elif isinstance(employee_roles, list):
            for role_row in employee_roles:
                user_doc.append("roles", {"role": role_row["role"], "parenttype": "User"})
    
    user_doc.save(ignore_permissions=True)