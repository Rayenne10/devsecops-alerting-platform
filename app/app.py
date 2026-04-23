import random
import time
from flask import Flask, jsonify, request
from prometheus_flask_exporter import PrometheusMetrics
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.resources import Resource

# ── OpenTelemetry setup ──────────────────────────────────────────────
resource = Resource.create({"service.name": "flask-app"})
provider = TracerProvider(resource=resource)
otlp_exporter = OTLPSpanExporter(endpoint="http://otel-collector:4317", insecure=True)
provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

# ── Flask setup ──────────────────────────────────────────────────────
app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)
metrics = PrometheusMetrics(app)

# Custom metrics
failed_logins = metrics.counter(
    'failed_logins_total',
    'Total number of failed login attempts'
)
active_users = metrics.gauge(
    'active_users',
    'Number of active users'
)

# ── Routes ───────────────────────────────────────────────────────────
@app.route("/")
def home():
    return jsonify({"status": "ok", "message": "App is running"})

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    username = data.get("username", "")
    password = data.get("password", "")

    # Simulate failed login
    if username != "admin" or password != "secret":
        failed_logins.inc()
        return jsonify({"error": "Invalid credentials"}), 401

    active_users.set(random.randint(1, 100))
    return jsonify({"message": "Login successful"})

@app.route("/slow")
def slow():
    # Simulate a slow endpoint
    with tracer.start_as_current_span("slow-operation"):
        time.sleep(random.uniform(1, 3))
    return jsonify({"message": "Slow response done"})

@app.route("/error")
def error():
    # Simulate random errors
    if random.random() < 0.7:
        return jsonify({"error": "Internal Server Error"}), 500
    return jsonify({"message": "Lucky, no error this time"})

@app.route("/health")
def health():
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
