// public/js/super_admin_workspace.js
frappe.provide("frappe.workspaces");

frappe.workspaces.SuperAdmin = class SuperAdmin {
    constructor(wrapper) {
        this.wrapper = $(wrapper);
        this.page = frappe.ui.make_app_page({
            parent: wrapper,
            title: 'Super Admin Dashboard',
            single_column: true
        });
        this.setup_page();
    }

    setup_page() {
        // Your dashboard setup code
    }
};

frappe.provide("ppdc_super_admin.pages");
ppdc_super_admin.pages.super_admin_dashboard = class SuperAdminDashboard {
    constructor(wrapper) {
        this.page = frappe.ui.make_app_page({
            parent: wrapper,
            title: 'Super Admin Dashboard',
            single_column: true
        });
        this.setup_page();
    }
};