# Grafana & Prometheus Monitoring Demo

A comprehensive monitoring solution using Grafana and Prometheus with a sample Python Flask application for metrics collection and visualization.

## 📋 Overview

This project demonstrates how to set up a complete monitoring stack using:
- **Prometheus** - For metrics collection and storage
- **Grafana** - For metrics visualization and dashboards
- **Flask Application** - Sample Python app exposing custom metrics

## 🚀 Features

- Real-time metrics collection
- Custom application metrics
- Pre-configured Prometheus scraping
- Docker Compose setup for easy deployment
- Scalable monitoring infrastructure

## 📦 Prerequisites

- Docker & Docker Compose
- Python 3.8+ (for local development)
- Git

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/pm0049/grafana-prometheus.git
cd grafana-prometheus
```

### 2. Start the Stack
```bash
docker-compose up -d
```

This will start:
- Prometheus on `http://localhost:9090`
- Grafana on `http://localhost:3000`
- Flask app on `http://localhost:5000`

### 3. Access Grafana

1. Open your browser and navigate to `http://localhost:3000`
2. Default credentials:
   - Username: `admin`
   - Password: `admin`
3. Add Prometheus as a data source:
   - URL: `http://prometheus:9090`

## 📊 Available Metrics

The Flask application exposes the following metrics at `/metrics`:

- Request counters
- Response times
- Custom application metrics
- System metrics

## 🐳 Docker Services

### Prometheus
- **Port**: 9090
- **Config**: `prometheus.yml`
- Scrapes metrics from the Flask application every 15 seconds

### Grafana
- **Port**: 3000
- Pre-configured to work with Prometheus

### Flask App
- **Port**: 5000
- Exposes `/metrics` endpoint for Prometheus scraping

## 📁 Project Structure
```
grafana-prometheus-demo/
├── app.py                  # Flask application with metrics
├── docker-compose.yml      # Docker Compose configuration
├── prometheus.yml          # Prometheus configuration
├── requirements.txt        # Python dependencies
└── README.md              # This file



```
<img width="1918" height="1026" alt="Image" src="https://github.com/user-attachments/assets/6f2810ce-4620-4d37-b75a-e5e4f033b1b7" />

## 🔧 Configuration

### Prometheus Configuration

Edit `prometheus.yml` to add more scrape targets:
```yaml
scrape_configs:
  - job_name: 'flask-app'
    scrape_interval: 15s
    static_configs:
      - targets: ['flask-app:5000']
```

### Adding Custom Metrics

In `app.py`, you can add custom metrics using the Prometheus client library:
```python
from prometheus_client import Counter, Histogram

custom_counter = Counter('my_custom_counter', 'Description')
custom_counter.inc()
```

## 📈 Creating Dashboards

1. Log into Grafana
2. Click on "+" → "Dashboard"
3. Add a new panel
4. Select Prometheus as the data source
5. Write PromQL queries to visualize your metrics

## 🛑 Stopping the Stack
```bash
docker-compose down
```

To remove volumes as well:
```bash
docker-compose down -v
```

## 📚 Useful Commands
```bash
# View logs
docker-compose logs -f

# Restart a specific service
docker-compose restart prometheus

# Check running containers
docker-compose ps

# Execute commands in container
docker-compose exec prometheus sh
```

## 🔍 Troubleshooting

### Prometheus not scraping metrics
- Check if the Flask app is running: `curl http://localhost:5000/metrics`
- Verify Prometheus targets: `http://localhost:9090/targets`

### Grafana can't connect to Prometheus
- Ensure both containers are on the same network
- Use container name instead of localhost: `http://prometheus:9090`

### Port conflicts
- Modify ports in `docker-compose.yml` if 3000, 5000, or 9090 are already in use

## 📖 Resources

- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [Prometheus Python Client](https://github.com/prometheus/client_python)
- [PromQL Basics](https://prometheus.io/docs/prometheus/latest/querying/basics/)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 👤 Author

**Pratik Mulik**
- GitHub: [@pm0049](https://github.com/pm0049)

## 🎯 Next Steps

- [ ] Add alerting rules
- [ ] Create custom Grafana dashboards
- [ ] Implement service discovery
- [ ] Add more application metrics
- [ ] Set up persistent storage for metrics

---

⭐ If you find this project helpful, please give it a star!
