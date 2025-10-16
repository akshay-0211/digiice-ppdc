# Copyright (c) 2025, Digiice Development Team and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _

class EmployeeMaster(Document):
    def validate(self):
        if self.user and not self.email:
            frappe.throw(_("Email is required for user creation"))
        
        if self.email and not frappe.utils.validate_email_address(self.email):
            frappe.throw(_("Invalid email address"))
            
    def before_save(self):
        if not self.user and self.email:
            self.create_user()
            
    def create_user(self):
        if not frappe.db.exists("User", self.email):
            try:
                # Check email configuration
                email_settings = frappe.get_doc('Email Account')
                if not (email_settings.smtp_server and email_settings.smtp_port):
                    # If email not configured, create user without welcome email
                    user = frappe.get_doc({
                        "doctype": "User",
                        "email": self.email,
                        "first_name": self.employee_name,
                        "username": self.employee_code,
                        "enabled": 1,
                        "send_welcome_email": 0,  # Disable welcome email
                        "user_type": "System User",
                    })
                    user.insert(ignore_permissions=True)
                    
                    # Set a default password
                    user.new_password = "Welcome@123"
                    user.save(ignore_permissions=True)
                    
                    # Update employee document
                    self.user = user.name
                    
                    # Assign default role based on employee type
                    self.assign_default_role(user.name)
                    
                    frappe.msgprint(_("""User {0} created successfully. 
                        Email configuration not found. 
                        Default password set to: Welcome@123""").format(user.name))
                else:
                    # Create user with welcome email if email is configured
                    user = frappe.get_doc({
                        "doctype": "User",
                        "email": self.email,
                        "first_name": self.employee_name,
                        "username": self.employee_code,
                        "enabled": 1,
                        "send_welcome_email": 1,
                        "user_type": "System User",
                    })
                    user.insert(ignore_permissions=True)
                    
                    # Update employee document
                    self.user = user.name
                    
                    # Assign default role based on employee type
                    self.assign_default_role(user.name)
                    
                    frappe.msgprint(_("User {0} created successfully. Welcome email sent.").format(user.name))
                    
            except Exception as e:
                frappe.log_error(f"User creation failed: {str(e)}")
                frappe.throw(_("Could not create user: {0}").format(str(e)))

    def assign_default_role(self, user_name):
        role_mapping = {
            "Officer": "PPDC Officer",
            "Ad-hoc": "PPDC Staff",
            "Contract": "PPDC Staff",
            "OJT": "PPDC Trainee",
            "Temp": "PPDC Staff",
            "Retired": "PPDC Consultant"
        }
        
        if self.employee_type in role_mapping:
            role = role_mapping[self.employee_type]
            self.assign_role_with_permissions(user_name, role)

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
        # Handle user deletion or deactivation when employee is deleted
        if self.user:
            try:
                user = frappe.get_doc("User", self.user)
                user.enabled = 0
                user.save(ignore_permissions=True)
            except Exception as e:
                frappe.log_error(f"User deactivation failed: {str(e)}")


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

def assign_roles_to_user(user, employee_roles):
    user_doc = frappe.get_doc("User", user)
    # Retain 'System Manager' role and override others
    user_doc.set("roles", [r for r in user_doc.roles if r.role == "System Manager"])
    
    # Handle role assignments
    if employee_roles:
        if isinstance(employee_roles, str):
            user_doc.append("roles", {"role": employee_roles})
        elif isinstance(employee_roles, list):
            for role_row in employee_roles:
                user_doc.append("roles", {"role": role_row.role})
    
    user_doc.save(ignore_permissions=True)