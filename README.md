# DevSecOps Alerting Platform 🔐

A production-grade monitoring and alerting platform built with OpenTelemetry, Prometheus, and Grafana — integrated into a secure CI/CD pipeline (DevSecOps).

---

## 🏗️ Architecture

```
Flask App → OpenTelemetry Collector → Prometheus → Alertmanager
                                           ↓
                                       Grafana (Dashboards)

GitHub Push → GitHub Actions → Bandit + Trivy + Safety → Build
```

---

## 🧰 Tech Stack

| Tool | Role |
|---|---|
| Flask | Sample application to monitor |
| OpenTelemetry | Collect and export metrics and traces |
| Prometheus | Store and query metrics |
| Alertmanager | Route and send alerts |
| Grafana | Visualize metrics and alerts |
| Docker Compose | Run all services locally |
| GitHub Actions | CI/CD pipeline automation |
| Bandit | Python SAST security scanner |
| Trivy | Docker image vulnerability scanner |
| Safety | Python dependency CVE scanner |

---

## 🚀 How to Run

### Prerequisites
- Docker Desktop (running)
- Git

### Start the full platform

```bash
git clone https://github.com/YOUR_USERNAME/devsecops-alerting-platform.git
cd devsecops-alerting-platform
docker compose up --build
```

### Access the services

| Service | URL | Credentials |
|---|---|---|
| Flask App | http://localhost:5000 | — |
| Flask Metrics | http://localhost:5000/metrics | — |
| Prometheus | http://localhost:9090 | — |
| Alertmanager | http://localhost:9093 | — |
| Grafana | http://localhost:3000 | admin / admin |

---

## 🔐 Security Alert Rules

| Alert | Trigger | Severity |
|---|---|---|
| BruteForceDetected | >5 failed logins in 2 minutes | 🔴 Critical |
| UnauthorizedAccessSpike | >10 HTTP 401s in 2 minutes | 🟡 Warning |
| HighErrorRate | >20% HTTP 500 error rate | 🟡 Warning |
| SlowResponseTime | p90 response time > 2 seconds | 🟡 Warning |
| AppDown | App unreachable for 30 seconds | 🔴 Critical |
| HighRequestRate | >10 req/sec for 2 minutes | 🟡 Warning |
| PrometheusTargetDown | Any monitored target is down | 🔴 Critical |

---

## 🧪 How to Simulate Alerts (Demo)

### Simulate a Brute Force Attack
```bash
for i in {1..20}; do
  curl -s -X POST http://localhost:5000/login \
    -H "Content-Type: application/json" \
    -d '{"username":"hacker","password":"wrong"}'
done
```

### Simulate High Error Rate
```bash
for i in {1..15}; do
  curl -s http://localhost:5000/error
done
```

### Simulate Slow Requests
```bash
for i in {1..5}; do
  curl -s http://localhost:5000/slow
done
```

After running any simulation, wait **1-2 minutes** then check:
- Prometheus Alerts → http://localhost:9090/alerts
- Alertmanager → http://localhost:9093

---

## 🔄 CI/CD Pipeline

Every push to `main` automatically triggers:

```
Push to GitHub
      ↓
✅ Run Tests (pytest)
      ↓
┌──────────────────────────────────────────┐
│  ✅ Bandit   ✅ Trivy    ✅ Safety       │
│  (SAST)     (Container)  (Dependencies)  │
└──────────────────────────────────────────┘
      ↓
✅ Build Final Docker Image
```

Security reports are saved as **downloadable artifacts** on every run.

---

## 📁 Project Structure

```
devsecops-alerting-platform/
├── app/
│   ├── app.py                      # Flask app with OTel instrumentation
│   ├── requirements.txt            # Python dependencies
│   ├── Dockerfile                  # Container definition
│   └── tests/
│       └── test_app.py             # Unit tests
├── prometheus/
│   ├── prometheus.yml              # Scrape configuration
│   └── alert_rules.yml            # 7 alerting rules
├── alertmanager/
│   └── alertmanager.yml           # Alert routing by severity
├── otel-collector/
│   └── otel-collector-config.yml  # OTel pipeline config
├── grafana/
│   └── provisioning/
│       ├── datasources/           # Prometheus datasource
│       └── dashboards/            # Auto-loaded dashboard JSON
├── .github/
│   └── workflows/
│       └── devsecops-pipeline.yml # Full CI/CD pipeline
└── docker-compose.yml             # Full stack definition
```

---

## 📊 Grafana Dashboard Panels

| Panel | Type | What it shows |
|---|---|---|
| Failed Login Attempts | Stat | Total failed logins counter |
| Failed Logins Rate | Time series | Logins/min over time |
| HTTP Request Rate by Status | Time series | Traffic breakdown by status code |
| Active Users | Gauge | Current active user count |
| App Health | Stat | UP / DOWN status |
| Response Time p90 | Time series | 90th percentile latency |
| 401 Unauthorized Requests | Time series | Unauthorized access over time |

---

## 👨‍💻 Author

Built as a final year project (PFA) demonstrating DevSecOps practices using open source observability tools.