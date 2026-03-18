# Certificate Lifecycle Management Portal

A Flask web application for monitoring and managing SSL/TLS certificate lifecycles across network infrastructure.

## Project Structure

```
certificate_management_portal/
├── app/
│   ├── __init__.py              # Flask application factory (create_app)
│   ├── models/
│   │   ├── __init__.py          # Exports Certificate, CertificateService
│   │   └── certificate.py       # Certificate dataclass + CertificateService
│   ├── routes/
│   │   ├── __init__.py          # Exports dashboard_bp, inventory_bp
│   │   ├── dashboard.py         # Blueprint: /, /dashboard — charts & stats
│   │   └── inventory.py         # Blueprint: /inventory, /api/certificates
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/                  # Client-side scripts (empty, tracked via .gitkeep)
│   └── templates/
│       ├── base.html
│       ├── dashboard.html
│       └── inventory.html
├── data/
│   └── mock_certificates.json   # Mock certificate records for development
├── config.py                    # DevelopmentConfig / ProductionConfig
├── requirements.txt
├── run.py                       # Entrypoint — runs on 0.0.0.0:5000
└── CLAUDE.md
```

## Running the App

```bash
pip install -r requirements.txt
python run.py
```

The app starts in development mode by default (`FLASK_ENV=development`). Visit `http://localhost:5000`.

To run in production mode:

```bash
FLASK_ENV=production python run.py
```

## Configuration (`config.py`)

| Key | Default | Description |
|-----|---------|-------------|
| `SECRET_KEY` | `dev-secret-key-...` | Override via `SECRET_KEY` env var in production |
| `MOCK_DATA_PATH` | `data/mock_certificates.json` | Path to certificate data |
| `ITEMS_PER_PAGE` | `50` | Pagination page size |
| `ALERT_CRITICAL` | `7` | Days-until-expiry threshold for critical status |
| `ALERT_WARNING` | `30` | Days-until-expiry threshold for warning status |
| `ALERT_ATTENTION` | `60` | Days-until-expiry threshold for attention status |
| `ALERT_INFO` | `90` | Days-until-expiry threshold for healthy/info status |

## Key Components

### `Certificate` (dataclass)
Represents a single certificate record. Key computed properties:
- `status` — `healthy | attention | warning | critical | expired` derived from `days_until_expiry`
- `status_color` — Bootstrap color class mapped from status

### `CertificateService`
Loads and queries certificates from JSON. Methods:
- `get_all()` — all certificates
- `get_by_id(cert_id)` — single certificate
- `get_by_status(status)` — filtered by status string
- `get_by_site(site_code)` — filtered by site
- `get_statistics()` — aggregate counts + site/device-type breakdowns

### Routes
| Blueprint | Prefix | Endpoints |
|-----------|--------|-----------|
| `dashboard_bp` | `/` | `GET /`, `GET /dashboard` |
| `inventory_bp` | `/inventory` | `GET /inventory`, `GET /api/certificates`, `GET /api/certificate/<id>` |

## Known Gaps / TODO

The application factory (`app/__init__.py`) registers two blueprints that do not yet have corresponding route files:
- `app/routes/discovery.py` — `discovery_bp`
- `app/routes/reports.py` — `reports_bp`

These must be created before the app can start without import errors.

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| Flask | 3.0.2 | Web framework |
| Flask-CORS | 4.0.0 | Cross-origin requests |
| plotly | 5.20.0 | Interactive charts on dashboard |
| pandas | 2.2.1 | Data manipulation for reports |
| openpyxl | 3.1.2 | Excel export |
| jinja2 | 3.1.3 | HTML templating |
| python-dateutil | 2.9.0 | Date parsing |
