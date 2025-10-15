app_name = "ppdc_super_admin"
app_title = "PPDC Super Admin"
app_publisher = "Digiice Development Team"
app_description = "Super Admin module for PPDC Agra with Master Data Management"
app_email = "dev@digiice.in"
app_license = "agpl-3.0"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "ppdc_super_admin",
# 		"logo": "/assets/ppdc_super_admin/logo.png",
# 		"title": "PPDC Super Admin",
# 		"route": "/ppdc_super_admin",
# 		"has_permission": "ppdc_super_admin.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/ppdc_super_admin/css/ppdc_super_admin.css"
# app_include_js = "/assets/ppdc_super_admin/js/ppdc_super_admin.js"

# include js, css files in header of web template
# web_include_css = "/assets/ppdc_super_admin/css/ppdc_super_admin.css"
# web_include_js = "/assets/ppdc_super_admin/js/ppdc_super_admin.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "ppdc_super_admin/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "ppdc_super_admin/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# automatically load and sync documents of this doctype from downstream apps
# importable_doctypes = [doctype_1]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "ppdc_super_admin.utils.jinja_methods",
# 	"filters": "ppdc_super_admin.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "ppdc_super_admin.install.before_install"
# after_install = "ppdc_super_admin.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "ppdc_super_admin.uninstall.before_uninstall"
# after_uninstall = "ppdc_super_admin.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "ppdc_super_admin.utils.before_app_install"
# after_app_install = "ppdc_super_admin.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "ppdc_super_admin.utils.before_app_uninstall"
# after_app_uninstall = "ppdc_super_admin.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "ppdc_super_admin.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"ppdc_super_admin.tasks.all"
# 	],
# 	"daily": [
# 		"ppdc_super_admin.tasks.daily"
# 	],
# 	"hourly": [
# 		"ppdc_super_admin.tasks.hourly"
# 	],
# 	"weekly": [
# 		"ppdc_super_admin.tasks.weekly"
# 	],
# 	"monthly": [
# 		"ppdc_super_admin.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "ppdc_super_admin.install.before_tests"

# Extend DocType Class
# ------------------------------
#
# Specify custom mixins to extend the standard doctype controller.
# extend_doctype_class = {
# 	"Task": "ppdc_super_admin.custom.task.CustomTaskMixin"
# }

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "ppdc_super_admin.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "ppdc_super_admin.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["ppdc_super_admin.utils.before_request"]
# after_request = ["ppdc_super_admin.utils.after_request"]

# Job Events
# ----------
# before_job = ["ppdc_super_admin.utils.before_job"]
# after_job = ["ppdc_super_admin.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"ppdc_super_admin.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

