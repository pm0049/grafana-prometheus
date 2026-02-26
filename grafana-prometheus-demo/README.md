# Grafana + Prometheus Monitoring Dashboard Project

A hands-on monitoring project demonstrating the fundamentals of Grafana and Prometheus by monitoring a Flask web application with real-time metrics visualization.

![Project Banner](screenshots/ss1.png)

---

## 📋 Table of Contents
- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Technologies Used](#technologies-used)
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Complete Setup Guide](#complete-setup-guide)
- [Running the Project](#running-the-project)
- [Dashboard Configuration](#dashboard-configuration)
- [Metrics Explained](#metrics-explained)
- [Troubleshooting](#troubleshooting)
- [Screenshots](#screenshots)
- [What I Learned](#what-i-learned)
- [Future Enhancements](#future-enhancements)
- [Resources](#resources)

---

## 🎯 Project Overview

This project is a complete monitoring solution built to understand observability concepts. It includes:

- **Flask Web Application** instrumented with Prometheus metrics
- **Prometheus** server for scraping and storing time-series data
- **Grafana** dashboards for real-time visualization
- **Custom metrics** tracking requests, errors, and business events

**Key Features:**
- Real-time request rate monitoring
- Error rate tracking
- Custom business metrics (user signups)
- Request duration histograms
- Interactive Grafana dashboards

---

## 🏗️ Architecture
```
┌──────────────────┐         ┌────────────────┐         ┌─────────────────┐
│                  │         │                │         │                 │
│   Flask App      │ ─────▶  │  Prometheus    │ ─────▶  │    Grafana      │
│   (Port 8000)    │ metrics │  (Port 9090)   │  query  │  (Port 3000)    │
│                  │  /15s   │                │         │                 │
│  • Endpoints     │         │  • Scraping    │         │  • Dashboards   │
│  • Metrics       │         │  • Storage     │         │  • Alerts       │
│  • Counters      │         │  • PromQL      │         │  • Graphs       │
└──────────────────┘         └────────────────┘         └─────────────────┘
        │                                                         │
        │                                                         │
        └─────────────────── User Traffic ───────────────────────┘
```

**Data Flow:**
1. Flask application exposes `/metrics` endpoint with Prometheus format
2. Prometheus scrapes metrics every 15 seconds
3. Grafana queries Prometheus for dashboard visualization
4. Users access Grafana to view real-time monitoring data

---

## 🛠️ Technologies Used

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.13+ | Application runtime |
| Flask | 3.1.2 | Web framework |
| Prometheus | 3.9.1 | Metrics collection |
| Grafana | Latest | Data visualization |
| Docker | Latest | Container runtime |
| prometheus-client | 0.24.1 | Python metrics library |

---

## ✅ Prerequisites

Before starting, ensure you have:

- [x] **Python 3.x** installed ([Download](https://www.python.org/downloads/))
- [x] **Docker Desktop** installed and running ([Download](https://www.docker.com/products/docker-desktop))
- [x] **Windows PowerShell** or Terminal access
- [x] **Text Editor** (Notepad, VS Code, etc.)
- [x] Basic understanding of:
  - Command line operations
  - Python basics
  - Docker concepts

**System Requirements:**
- OS: Windows 10/11, macOS, or Linux
- RAM: 4GB minimum
- Disk Space: 2GB free space

---

## 📁 Project Structure
```
grafana-prometheus-demo/
│
├── app.py                      # Flask application with Prometheus metrics
├── prometheus.yml              # Prometheus scrape configuration
├── requirements.txt            # Python dependencies
├── generate_traffic.py         # Traffic generator script (optional)
├── README.md                   # Project documentation
│
└── screenshots/                # Project screenshots
    ├── flask-app.png
    ├── prometheus-targets.png
    ├── grafana-dashboard.png
    ├── request-rate.png
    └── metrics-endpoint.png
```

---

## 🚀 Complete Setup Guide

### Step 1: Create Project Directory
```powershell
# Create project folder
mkdir grafana-prometheus-demo
cd grafana-prometheus-demo
```

---

### Step 2: Create Python Requirements File

Create `requirements.txt`:
```txt
flask
prometheus-client
```

Install dependencies:
```powershell
pip install -r requirements.txt
```

---

### Step 3: Create Flask Application

Create `app.py` with the following content:
```python
from flask import Flask
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time
import random

app = Flask(__name__)

# Define Prometheus metrics
REQUEST_COUNT = Counter(
    'app_requests_total', 
    'Total HTTP requests', 
    ['method', 'endpoint', 'status']
)

REQUEST_DURATION = Histogram(
    'app_request_duration_seconds', 
    'HTTP request duration in seconds'
)

USER_SIGNUPS = Counter(
    'app_user_signups_total', 
    'Total number of user signups'
)

@app.route('/')
def home():
    """Home endpoint - simulates work and tracks metrics"""
    start = time.time()
    REQUEST_COUNT.labels(method='GET', endpoint='/', status=200).inc()
    
    # Simulate some work
    time.sleep(random.uniform(0.1, 0.5))
    
    REQUEST_DURATION.observe(time.time() - start)
    return 'Hello, Monitoring World!'

@app.route('/signup', methods=['POST'])
def signup():
    """Signup endpoint - tracks user signups"""
    USER_SIGNUPS.inc()
    REQUEST_COUNT.labels(method='POST', endpoint='/signup', status=201).inc()
    return 'User signed up!', 201

@app.route('/error')
def error():
    """Error endpoint - simulates failures"""
    REQUEST_COUNT.labels(method='GET', endpoint='/error', status=500).inc()
    return 'Error!', 500

@app.route('/metrics')
def metrics():
    """Prometheus metrics endpoint"""
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
```

**Key Points:**
- `Counter`: Tracks cumulative values (requests, signups)
- `Histogram`: Tracks distributions (request durations)
- `/metrics`: Exposes data in Prometheus format
- `CONTENT_TYPE_LATEST`: Correct content type for Prometheus

---

### Step 4: Create Prometheus Configuration

Create `prometheus.yml`:
```yaml
global:
  scrape_interval: 15s          # How often to scrape targets
  evaluation_interval: 15s      # How often to evaluate rules

scrape_configs:
  # Prometheus monitoring itself
  - job_name: prometheus
    static_configs:
      - targets: [localhost:9090]

  # Flask application
  - job_name: flask-app
    static_configs:
      - targets: [host.docker.internal:8000]
    metrics_path: /metrics
```

**Configuration Explained:**
- `scrape_interval`: Prometheus scrapes metrics every 15 seconds
- `job_name`: Logical name for the target
- `targets`: Where to scrape from
- `host.docker.internal`: Docker's way to access host machine

---

### Step 5: Start Docker Containers

#### Create Docker Network
```powershell
docker network create monitoring
```

#### Start Prometheus
```powershell
docker run -d \
  --name my-prometheus \
  -p 9090:9090 \
  -v ${PWD}/prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus \
  --config.file=/etc/prometheus/prometheus.yml

docker network connect monitoring my-prometheus
```

#### Start Grafana
```powershell
docker run -d \
  --name my-grafana \
  -p 3000:3000 \
  -e GF_SECURITY_ADMIN_PASSWORD=admin \
  grafana/grafana

docker network connect monitoring my-grafana
```

#### Verify Containers are Running
```powershell
docker ps
```

**Expected output:**
```
CONTAINER ID   IMAGE             PORTS                    NAMES
xxxxxxxx       grafana/grafana   0.0.0.0:3000->3000/tcp   my-grafana
xxxxxxxx       prom/prometheus   0.0.0.0:9090->9090/tcp   my-prometheus
```

---

### Step 6: Start Flask Application
```powershell
python app.py
```

**Expected output:**
```
 * Serving Flask app 'app'
 * Running on http://127.0.0.1:8000
 * Running on http://0.0.0.0:8000
```

**Keep this terminal window open!**

---

## 🎮 Running the Project

### Access the Services

| Service | URL | Credentials |
|---------|-----|-------------|
| Flask App | http://localhost:8000 | None |
| Prometheus | http://localhost:9090 | None |
| Grafana | http://localhost:3000 | admin / admin |

---

### Verify Prometheus is Scraping

1. Open **http://localhost:9090/targets**
2. Look for `flask-app` target
3. Ensure **State** shows **UP** (green)

![Prometheus Targets](screenshots/prometheus-targets.png)

**If DOWN (red):**
- Check Flask is running
- Verify http://localhost:8000/metrics is accessible
- Check prometheus.yml configuration

---

### Generate Test Traffic

Create `generate_traffic.py`:
```python
import requests
import time
import random

print('Generating traffic... Press Ctrl+C to stop')

while True:
    try:
        # Random requests to different endpoints
        endpoints = [
            'http://localhost:8000/', 
            'http://localhost:8000/error'
        ]
        requests.get(random.choice(endpoints))
        
        # Occasional signup requests
        if random.random() > 0.8:
            requests.post('http://localhost:8000/signup')
        
        time.sleep(random.uniform(0.5, 2))
        print('.', end='', flush=True)
    except Exception as e:
        print(f'\nError: {e}')
        time.sleep(1)
```

Run it:
```powershell
python generate_traffic.py
```

---

## 📊 Dashboard Configuration

### Step 1: Login to Grafana

1. Open **http://localhost:3000**
2. Login with:
   - **Username**: `admin`
   - **Password**: `admin`
3. Skip password change or set a new one

---

### Step 2: Add Prometheus Data Source

1. Click **☰ menu** (top left)
2. Go to: **Connections** → **Data sources**
3. Click **"Add data source"**
4. Select **"Prometheus"**
5. Configure:
   - **Name**: `Prometheus`
   - **URL**: `http://my-prometheus:9090`
   - Leave other settings as default
6. Click **"Save & test"**
7. You should see: ✅ **"Successfully queried the Prometheus API"**

---

### Step 3: Create Dashboard

1. Click **☰ menu** → **Dashboards**
2. Click **"New"** → **"New Dashboard"**
3. Click **"+ Add visualization"**
4. Select **"Prometheus"** data source

---

### Step 4: Create Panels

#### Panel 1: Total Requests (Big Number)

**Configuration:**
- **Query**: `sum(app_requests_total)`
- **Visualization**: Stat
- **Title**: Total Requests
- **Description**: Total number of HTTP requests received

**Steps:**
1. In query box, enter: `sum(app_requests_total)`
2. Click "Run queries"
3. On right side, set **Title**: `Total Requests`
4. Change **Visualization** to: **Stat**
5. Click **"Apply"**

---

#### Panel 2: Request Rate Over Time

**Configuration:**
- **Query**: `rate(app_requests_total[1m])`
- **Visualization**: Time series
- **Title**: Request Rate per Second
- **Description**: Shows requests/second over time

**Steps:**
1. Click "Add" → "Visualization"
2. Query: `rate(app_requests_total[1m])`
3. Title: `Request Rate per Second`
4. Keep as **Time series**
5. Click **"Apply"**

---

#### Panel 3: Error Rate

**Configuration:**
- **Query**: `rate(app_requests_total{status="500"}[1m])`
- **Visualization**: Time series (with red color)
- **Title**: Error Rate
- **Description**: Tracks /error endpoint hits

**Steps:**
1. Click "Add" → "Visualization"
2. Query: `rate(app_requests_total{status="500"}[1m])`
3. Title: `Error Rate`
4. Under **Standard options** → **Color scheme**: Red
5. Click **"Apply"**

---

#### Panel 4: Total User Signups

**Configuration:**
- **Query**: `app_user_signups_total`
- **Visualization**: Stat
- **Title**: Total User Signups
- **Description**: Custom business metric

**Steps:**
1. Click "Add" → "Visualization"
2. Query: `app_user_signups_total`
3. Title: `Total User Signups`
4. Visualization: **Stat**
5. Click **"Apply"**

---

#### Panel 5: Request Duration (95th Percentile)

**Configuration:**
- **Query**: `histogram_quantile(0.95, rate(app_request_duration_seconds_bucket[5m]))`
- **Visualization**: Time series
- **Title**: 95th Percentile Response Time
- **Description**: 95% of requests complete within this time

**Steps:**
1. Click "Add" → "Visualization"
2. Query: `histogram_quantile(0.95, rate(app_request_duration_seconds_bucket[5m]))`
3. Title: `95th Percentile Response Time`
4. Unit: `seconds (s)`
5. Click **"Apply"**

---

### Step 5: Save Dashboard

1. Click the **💾 Save** icon (top right)
2. **Dashboard name**: `My Monitoring Dashboard`
3. **Folder**: General
4. Click **"Save"**

---

## 📈 Metrics Explained

### Counter: `app_requests_total`

**Type**: Counter (monotonically increasing)

**Purpose**: Tracks total number of HTTP requests

**Labels**:
- `method`: HTTP method (GET, POST)
- `endpoint`: URL path (/, /signup, /error)
- `status`: HTTP status code (200, 201, 500)

**Example PromQL Queries**:
```promql
# Total requests
sum(app_requests_total)

# Request rate per second
rate(app_requests_total[1m])

# Error rate
rate(app_requests_total{status="500"}[1m])

# Requests by endpoint
sum by (endpoint) (app_requests_total)
```

---

### Histogram: `app_request_duration_seconds`

**Type**: Histogram (distribution of values)

**Purpose**: Tracks HTTP request durations

**Use Cases**:
- Calculate average response time
- Find 95th percentile (most requests complete within X seconds)
- Identify slow requests

**Example PromQL Queries**:
```promql
# Average response time
rate(app_request_duration_seconds_sum[5m]) 
/ 
rate(app_request_duration_seconds_count[5m])

# 95th percentile
histogram_quantile(0.95, rate(app_request_duration_seconds_bucket[5m]))

# 50th percentile (median)
histogram_quantile(0.50, rate(app_request_duration_seconds_bucket[5m]))
```

---

### Counter: `app_user_signups_total`

**Type**: Counter

**Purpose**: Custom business metric tracking user signups

**Use Cases**:
- Track total signups
- Calculate signup rate
- Alert on signup anomalies

**Example PromQL Queries**:
```promql
# Total signups
app_user_signups_total

# Signup rate per minute
rate(app_user_signups_total[1m])

# Signups in last hour
increase(app_user_signups_total[1h])
```

---

## 🔧 Troubleshooting

### Issue 1: flask-app shows DOWN in Prometheus

**Symptoms**: Red status in http://localhost:9090/targets

**Solutions**:

1. **Verify Flask is running**:
```powershell
   curl http://localhost:8000
```

2. **Check metrics endpoint**:
```powershell
   curl http://localhost:8000/metrics
```
   Should return Prometheus format metrics, not HTML

3. **Verify Content-Type**:
```python
   # In app.py, ensure metrics function has:
   return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}
```

4. **Check prometheus.yml**:
   - Ensure target is `host.docker.internal:8000`
   - Verify `metrics_path: /metrics`

5. **Restart Prometheus**:
```powershell
   docker restart my-prometheus
```

---

### Issue 2: Grafana shows "No data"

**Solutions**:

1. **Verify data source connection**:
   - Go to: Connections → Data sources → Prometheus
   - Click "Save & test"
   - Should show green success message

2. **Check Prometheus is collecting data**:
   - Open: http://localhost:9090
   - Search: `app_requests_total`
   - Click "Execute"
   - Should see data in table

3. **Generate traffic**:
```powershell
   # Make some requests
   for ($i=1; $i -le 50; $i++) { 
       curl http://localhost:8000/ 
   }
```

4. **Check time range**:
   - In Grafana panel, check time range (top right)
   - Set to "Last 5 minutes" or "Last 15 minutes"

---

### Issue 3: Docker containers won't start

**Solutions**:

1. **Check Docker is running**:
   - Open Docker Desktop
   - Ensure Docker icon in system tray is active

2. **Check port conflicts**:
```powershell
   # Check if ports are already in use
   netstat -ano | findstr :9090
   netstat -ano | findstr :3000
```

3. **Remove old containers**:
```powershell
   docker rm -f my-prometheus my-grafana
   docker network rm monitoring
```
   Then recreate them

4. **Check logs**:
```powershell
   docker logs my-prometheus
   docker logs my-grafana
```

---

### Issue 4: "Connection refused" error

**Solutions**:

1. **Allow Python through Windows Firewall**:
   - Windows Defender Firewall → Allow an app
   - Add: `python.exe`
   - Check both Private and Public

2. **Use localhost instead of host.docker.internal**:
   - In prometheus.yml, try: `targets: [YOUR_IP:8000]`
   - Find your IP: `ipconfig` (look for IPv4 Address)

3. **Use Docker host network** (Linux only):
```yaml
   # In docker-compose.yml
   network_mode: host
```

---

### Issue 5: Metrics show wrong Content-Type

**Error**: "received unsupported Content-Type 'text/html'"

**Solution**:

Ensure `app.py` metrics endpoint uses correct content type:
```python
from prometheus_client import CONTENT_TYPE_LATEST

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}
```

**NOT**:
```python
return generate_latest()  # Wrong - defaults to text/html
```

---

## 📸 Screenshots

### 1. Flask Application Home Page
![Flask App Running](screenshots/ss1.png)
*The Flask application responding at localhost:8000*

---

### 2. Prometheus Metrics Endpoint
![Metrics Endpoint](screenshots/ss4.png)
*Raw Prometheus metrics exposed at /metrics endpoint*

---

### 3. Prometheus Targets Status
![Prometheus Targets](screenshots/ss6.png)
*Prometheus showing flask-app target as UP (green) - successfully scraping metrics*

---

### 4. Complete Grafana Dashboard
![Grafana Dashboard](screenshots/ss2.png)
*Full monitoring dashboard with all panels showing real-time data*

---

### 5. Request Rate Time Series
![Request Rate Graph](screenshots/ss6.png)
*Request rate per second over time - shows traffic patterns*

---

## 🎓 What I Learned

### Prometheus Skills Acquired

✅ **Metric Types**:
- Counters for cumulative values
- Histograms for distributions
- Gauges for point-in-time values

✅ **PromQL Query Language**:
- `rate()` for per-second rates
- `sum()` for aggregation
- `histogram_quantile()` for percentiles
- Label filtering with `{}`

✅ **Configuration**:
- Writing prometheus.yml
- Configuring scrape targets
- Setting scrape intervals
- Understanding metrics_path

✅ **Architecture**:
- Pull-based monitoring model
- Time-series data storage
- Target discovery concepts

---

### Grafana Skills Acquired

✅ **Data Source Management**:
- Connecting to Prometheus
- Configuring authentication
- Testing connections

✅ **Dashboard Creation**:
- Building panels from scratch
- Choosing appropriate visualizations
- Using variables and templates

✅ **Visualization Types**:
- Time series for trends
- Stats for single values
- Gauges for current state
- Tables for detailed data

✅ **Query Editor**:
- Writing PromQL in Grafana
- Using query builder
- Setting refresh intervals

---

### Application Instrumentation

✅ **Metrics Integration**:
- Adding prometheus_client to Python
- Creating custom metrics
- Exposing /metrics endpoint
- Setting correct content types

✅ **Best Practices**:
- Using descriptive metric names
- Adding useful labels
- Avoiding high cardinality
- Documentation in metric help text

✅ **Performance Considerations**:
- Minimal overhead from metrics
- Efficient metric collection
- Appropriate scrape intervals

---

### Docker & DevOps

✅ **Container Management**:
- Running services in Docker
- Container networking
- Volume mounting
- Port mapping

✅ **Networking**:
- Docker networks
- host.docker.internal usage
- Container DNS resolution

✅ **Troubleshooting**:
- Reading container logs
- Debugging connectivity
- Port conflict resolution

---

### Observability Concepts

✅ **The Three Pillars**:
- Metrics (this project)
- Logs (future enhancement)
- Traces (future enhancement)

✅ **Monitoring Strategy**:
- What to measure
- When to alert
- SLI/SLO concepts

✅ **Practical Skills**:
- Real-time monitoring
- Performance analysis
- Issue detection
- Data-driven decisions

---

---

## 📚 Resources

### Official Documentation

- [Prometheus Documentation](https://prometheus.io/docs/introduction/overview/)
- [Grafana Documentation](https://grafana.com/docs/)
- [prometheus_client Python Library](https://github.com/prometheus/client_python)
- [Flask Documentation](https://flask.palletsprojects.com/)

### Tutorials & Guides

- [Prometheus Best Practices](https://prometheus.io/docs/practices/)
- [PromQL Basics](https://prometheus.io/docs/prometheus/latest/querying/basics/)
- [Grafana Dashboard Best Practices](https://grafana.com/docs/grafana/latest/best-practices/)

### Community

- [Prometheus GitHub](https://github.com/prometheus/prometheus)
- [Grafana GitHub](https://github.com/grafana/grafana)
- [CNCF Slack - #prometheus](https://slack.cncf.io/)

### Learning Resources

- [Prometheus Up & Running (Book)](https://www.oreilly.com/library/view/prometheus-up/9781492034131/)
- [Grafana Fundamentals Course](https://grafana.com/tutorials/)

---

## 🤝 Contributing

This is a learning project, but contributions are welcome!

**How to contribute:**
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

**Ideas for contributions:**
- Additional metric types
- New dashboard panels
- Better traffic generators
- Documentation improvements
- Bug fixes

---

## 📝 License

This project is open source and available for educational purposes.

Feel free to use, modify, and distribute for learning.

---

## 🙏 Acknowledgments

- **Prometheus Community** for excellent documentation
- **Grafana Labs** for powerful visualization tools
- **Flask Team** for simple web framework
- **Docker** for containerization

---

## 📧 Contact

**Created by:** Pratik Mulik  
**Date:** February 2026  
**Purpose:** Learning Grafana & Prometheus fundamentals  
**Location:** Mumbai, Maharashtra, India

---

## ⭐ Project Status

**Status**: ✅ **Complete and Working**

**Last Updated**: February 25, 2026

**Version**: 1.0.0

---

## 🎯 Project Goals Achieved

- [x] Set up Prometheus monitoring
- [x] Create instrumented Flask application
- [x] Configure Grafana dashboards
- [x] Understand metric types
- [x] Learn PromQL queries
- [x] Practice Docker operations
- [x] Build real-time monitoring system

---

**Thank you for checking out this project! Happy monitoring! 📊🚀**
