# Self-Healing Infrastructure

An automated infrastructure monitoring and recovery project using Prometheus, Alertmanager, Flask, Ansible, and NGINX.

## Architecture

NGINX → Blackbox Exporter → Prometheus → Alertmanager → Flask Webhook → Ansible → NGINX Recovery

## Components

- **NGINX:** Web server monitored for availability.
- **Blackbox Exporter:** Performs HTTP health checks.
- **Prometheus:** Collects monitoring metrics and evaluates alert rules.
- **Alertmanager:** Routes alerts to the webhook and email receiver.
- **Flask:** Receives and validates alerts.
- **Ansible:** Executes the automated NGINX recovery playbook.
- **Node Exporter:** Provides system metrics, including CPU utilization.

## Automated Recovery Workflow

1. Prometheus detects that NGINX is unavailable.
2. The `NginxDown` alert fires.
3. Alertmanager sends a webhook to the Flask application.
4. Flask validates the alert.
5. Flask invokes the fixed Ansible recovery wrapper.
6. Ansible ensures NGINX is running.
7. An HTTP health check verifies recovery.

## Monitoring and Alerts

- NGINX availability monitoring.
- CPU utilization monitoring.
- Email notifications through Gmail SMTP.
- Automated NGINX recovery for the `NginxDown` alert.

## Technologies

- Ubuntu on WSL2
- NGINX
- Prometheus
- Alertmanager
- Blackbox Exporter
- Node Exporter
- Python and Flask
- Ansible
- Git and GitHub

## Repository Structure

```text
self-healing-infrastructure/
├── ansible/
│   └── recover_nginx.yml
├── webhook/
│   └── app.py
├── .gitignore
└── README.md


```

## Security Notes

- Do not commit passwords, SMTP credentials, API keys, or private keys.
- Keep credentials in protected files outside the repository.
- Review configuration files before publishing.

## Validation

The NGINX recovery workflow was tested by stopping NGINX and verifying that the monitoring and alerting pipeline triggered automated recovery.

The CPU alert rule was loaded and verified in Prometheus. Actual high-CPU email delivery has not yet been demonstrated.
