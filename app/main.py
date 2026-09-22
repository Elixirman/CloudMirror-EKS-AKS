import os
from datetime import datetime
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from sqlalchemy import create_engine, text

app = FastAPI(title="O&G Multicloud App")

DB_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/appdb")
CLOUD = os.getenv("CLOUD_PROVIDER", "unknown")
engine = create_engine(DB_URL, pool_pre_ping=True)

@app.get("/health")
def health():
    return {"status": "ok", "time": datetime.utcnow().isoformat()}

@app.get("/readings")
def readings():
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT id, sensor_id, value, unit, recorded_at FROM readings ORDER BY recorded_at DESC LIMIT 20")).mappings().all()
        return {"count": len(rows), "readings": [dict(r) for r in rows]}

@app.get("/")
def root():
    return {"app": "O&G Multicloud Platform", "cloud": CLOUD}

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT sensor_id, value, unit, recorded_at FROM readings ORDER BY recorded_at DESC LIMIT 20")).mappings().all()

    rows_html = "".join(
        f"<tr><td>{r['sensor_id']}</td><td>{r['value']}</td><td>{r['unit']}</td><td>{r['recorded_at']}</td></tr>"
        for r in rows
    ) or "<tr><td colspan='4'>No data yet</td></tr>"

    badge_class = "aws" if CLOUD == "aws" else "azure" if CLOUD == "azure" else "unknown"

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>O&G Multicloud Platform</title>
        <style>
            body {{
                font-family: 'Segoe UI', Arial, sans-serif;
                background: #0f172a;
                color: #e2e8f0;
                margin: 0;
                padding: 40px;
            }}
            .container {{
                max-width: 900px;
                margin: 0 auto;
            }}
            h1 {{
                font-size: 28px;
                margin-bottom: 4px;
            }}
            .subtitle {{
                color: #94a3b8;
                margin-bottom: 20px;
            }}
            .badge {{
                display: inline-block;
                padding: 4px 14px;
                border-radius: 20px;
                font-weight: bold;
                font-size: 13px;
                letter-spacing: 1px;
            }}
            .badge.aws {{ background: #ff9900; color: #1a1a1a; }}
            .badge.azure {{ background: #0078d4; color: white; }}
            .badge.unknown {{ background: #475569; color: white; }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 24px;
                background: #1e293b;
                border-radius: 8px;
                overflow: hidden;
            }}
            th, td {{
                padding: 12px 16px;
                text-align: left;
            }}
            th {{
                background: #334155;
                text-transform: uppercase;
                font-size: 12px;
                letter-spacing: 1px;
                color: #94a3b8;
            }}
            tr:nth-child(even) {{ background: #24324a; }}
            .footer {{
                margin-top: 24px;
                color: #64748b;
                font-size: 13px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Oil & Gas Sensor Platform</h1>
            <p class="subtitle">Real-time sensor readings &middot; <span class="badge {badge_class}">{CLOUD.upper()}</span></p>
            <table>
                <tr><th>Sensor ID</th><th>Value</th><th>Unit</th><th>Recorded At</th></tr>
                {rows_html}
            </table>
            <p class="footer">Deployed via Terraform + Kubernetes ({CLOUD})</p>
        </div>
    </body>
    </html>
    """
