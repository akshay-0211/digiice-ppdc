frappe.provide('ppdc_super_admin.workspace');

ppdc_super_admin.workspace.SuperAdmin = class SuperAdminWorkspace {
    constructor(wrapper) {
        this.wrapper = $(wrapper);
        this.page = frappe.ui.make_app_page({
            parent: wrapper,
            title: 'Super Admin - Master Data',
            single_column: true
        });
        this.setup_page();
    }

    setup_page() {
        this.setup_dashboard();
    }

    setup_dashboard() {

    $(wrapper).find('.layout-main-section').html(`
        <div class="ppdc-dashboard">
            <h3 style="margin-bottom: 30px;">Master Data Management</h3>
            <p class="text-muted" style="margin-bottom: 40px;">
                Centralized management of all master data for PPDC Agra
            </p>
            
            <div class="row">
                <div class="col-md-4 col-sm-6 dashboard-card-wrapper">
                    <a href="/app/head-office" class="card-link">
                        <div class="master-data-card blue-border">
                            <div class="card-icon blue-text"><i class="fa fa-building fa-3x"></i></div>
                            <h4 class="card-title">Head Office</h4>
                            <p class="card-desc">Manage headquarters details</p>
                        </div>
                    </a>
                </div>
                
                <div class="col-md-4 col-sm-6 dashboard-card-wrapper">
                    <a href="/app/extension-center" class="card-link">
                        <div class="master-data-card green-border">
                            <div class="card-icon green-text"><i class="fa fa-map-marker fa-3x"></i></div>
                            <h4 class="card-title">Extension Center</h4>
                            <p class="card-desc">18+ field centers</p>
                        </div>
                    </a>
                </div>
                
                <div class="col-md-4 col-sm-6 dashboard-card-wrapper">
                    <a href="/app/efc-master" class="card-link">
                        <div class="master-data-card purple-border">
                            <div class="card-icon purple-text"><i class="fa fa-home fa-3x"></i></div>
                            <h4 class="card-title">EFC Master</h4>
                            <p class="card-desc">Enterprise Facilitation Centers</p>
                        </div>
                    </a>
                </div>
                
                <div class="col-md-4 col-sm-6 dashboard-card-wrapper">
                    <a href="/app/scheme" class="card-link">
                        <div class="master-data-card orange-border">
                            <div class="card-icon orange-text"><i class="fa fa-file-text fa-3x"></i></div>
                            <h4 class="card-title">Scheme</h4>
                            <p class="card-desc">Government schemes</p>
                        </div>
                    </a>
                </div>
                
                <div class="col-md-4 col-sm-6 dashboard-card-wrapper">
                    <a href="/app/employee-master" class="card-link">
                        <div class="master-data-card red-border">
                            <div class="card-icon red-text"><i class="fa fa-users fa-3x"></i></div>
                            <h4 class="card-title">Employee Master</h4>
                            <p class="card-desc">Staff with RBAC</p>
                        </div>
                    </a>
                </div>
                
                <div class="col-md-4 col-sm-6 dashboard-card-wrapper">
                    <a href="/app/faculty" class="card-link">
                        <div class="master-data-card cyan-border">
                            <div class="card-icon cyan-text"><i class="fa fa-user fa-3x"></i></div>
                            <h4 class="card-title">Faculty</h4>
                            <p class="card-desc">Trainers & instructors</p>
                        </div>
                    </a>
                </div>
            </div>
        </div>
        
        <style>
            .ppdc-dashboard { padding: 20px; }
            .dashboard-card-wrapper { margin-bottom: 25px; }
            .card-link { text-decoration: none; color: inherit; display: block; }
            .master-data-card {
                padding: 35px 20px;
                text-align: center;
                border-radius: 8px;
                background: #fff;
                border: 3px solid;
                transition: all 0.3s ease;
                height: 100%;
                box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            }
            .master-data-card:hover {
                transform: translateY(-8px);
                box-shadow: 0 12px 24px rgba(0,0,0,0.2);
            }
            .card-icon { margin-bottom: 15px; }
            .card-title { margin: 15px 0 10px 0; font-weight: 600; font-size: 18px; }
            .card-desc { margin: 0; color: #666; font-size: 13px; }
            
            .blue-border { border-color: #3498db; }
            .blue-text { color: #3498db; }
            .green-border { border-color: #2ecc71; }
            .green-text { color: #2ecc71; }
            .purple-border { border-color: #9b59b6; }
            .purple-text { color: #9b59b6; }
            .orange-border { border-color: #e67e22; }
            .orange-text { color: #e67e22; }
            .red-border { border-color: #e74c3c; }
            .red-text { color: #e74c3c; }
            .cyan-border { border-color: #1abc9c; }
            .cyan-text { color: #1abc9c; }
        </style>
    `)    }
};

frappe.pages['super-admin'].on_page_load = function(wrapper) {
    frappe.super_admin_workspace = new ppdc_super_admin.workspace.SuperAdmin(wrapper);
};
