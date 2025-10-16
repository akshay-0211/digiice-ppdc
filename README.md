# PPDC Super Admin

Super Admin module for PPDC Agra with Master Data Management and RBAC

## Setup

### Prerequisites
- Python 3.12+
- Node.js 16+
- Redis
- MariaDB

### Installation Steps

1. Create new bench:
```bash
bench init frappe-bench
cd frappe-bench
```

2. Get the app:
```bash
bench get-app https://github.com/akshay-0211/digiice-ppdc.git
```

3. Create new site:
```bash
bench new-site erpnext.localhost
bench --site erpnext.localhost install-app ppdc_super_admin
```

4. Build and Start:
```bash
bench build
bench start
```

### Email Configuration (Optional)
```bash
bench --site erpnext.localhost set-config -g mail_server "smtp.gmail.com"
bench --site erpnext.localhost set-config -g mail_port 587
bench --site erpnext.localhost set-config -g mail_use_tls 1
```

### Troubleshooting
- Clear cache: `bench clear-cache`
- Rebuild database: `bench --site erpnext.localhost migrate`
- Check logs: `bench --site erpnext.localhost show-logs`

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench install-app ppdc_super_admin
```

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/ppdc_super_admin
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade
### CI

This app can use GitHub Actions for CI. The following workflows are configured:

- CI: Installs this app and runs unit tests on every push to `develop` branch.
- Linters: Runs [Frappe Semgrep Rules](https://github.com/frappe/semgrep-rules) and [pip-audit](https://pypi.org/project/pip-audit/) on every pull request.


### License

agpl-3.0
