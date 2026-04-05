# Cricket Predictor Pro (ODI + T20)

Cricket Predictor Pro is a Flask web app for cricket match simulation and analysis.
It focuses on practical match inputs and visual outputs for project/demo use.

## What this project does

- Team selection (top teams)
- 15-player squad loading and Playing XI selection
- Score prediction with `Low / Average / High`
- Chase win probability
- Run trajectory chart
- Team comparison charts
- DLS target calculator (with interruption inputs)
- Live match ingestion from **Cricbuzz links**

## Tech Stack

- Backend: Python + Flask
- Frontend: HTML, CSS, JavaScript, Chart.js
- Data/model logic: `api/data.py` and `api/engine.py`
- Server: Gunicorn

## Project Structure

```text
.
├── api/
│   ├── app.py                # Flask routes
│   ├── engine.py             # Prediction logic
│   ├── data.py               # Teams/squads/venues/rules
│   ├── templates/
│   │   └── index.html
│   └── static/
│       ├── app.js
│       ├── style.css
│       └── flags/
├── requirements.txt
├── Procfile
├── railway.json
└── README.md
```

## Prerequisites

- Python 3.10+
- pip

## Setup

Run from project root (folder containing `api/`):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Run Locally

### Recommended

```bash
gunicorn api.app:app --bind 0.0.0.0:5000
```

Open:
- `http://localhost:5000`

### Alternative (Flask dev server)

```bash
python3 -m flask --app api.app run --host 0.0.0.0 --port 5000
```

## Start/Stop Commands (Quick)

### Start (foreground)

```bash
gunicorn api.app:app --bind 0.0.0.0:5000
```

### Stop (foreground)

Press `Ctrl + C`

### Start (background)

```bash
nohup gunicorn api.app:app --bind 0.0.0.0:5000 > server.log 2>&1 & echo $!
```

### Stop (background by PID)

```bash
kill <PID>
```

### Stop by port

```bash
fuser -k 5000/tcp
```

## Health Check

```bash
curl http://localhost:5000/api/status
```

## API Routes

- `GET /api/status`
- `GET /api/meta?format=odi|t20`
- `GET /api/squad?team=<TEAM>&format=odi|t20`
- `POST /api/predict_score`
- `POST /api/win_probability`
- `POST /api/dls`
- `POST /api/compare`
- `POST /api/trajectory`

## Deployment

### Railway (if using paid/active plan)

This repo is already prepared with:
- `Procfile`
- `railway.json`
- `requirements.txt`

Start command:

```bash
gunicorn api.app:app --bind 0.0.0.0:$PORT
```

### Free alternatives

- Render free web service (if available in your region/plan)
- Fly.io free allowances (depends on current policy)
- Self-host on a VM/VPS
- Cloudflare tunnel to expose your local app for demos

## Common Issues

### 1) `No module named 'api'`

Run from correct folder:

```bash
pwd
ls
```

Make sure `api/` is visible.

### 2) Port 5000 already in use

```bash
fuser -k 5000/tcp
```

### 3) Live ingest not working

- Use a valid full Cricbuzz match URL.
- Retry with another live match link.
- Check internet connection and provider restrictions.

## Disclaimer

This is a model-based educational predictor. It is not an official ICC scoring tool and should not be treated as an official result system.
