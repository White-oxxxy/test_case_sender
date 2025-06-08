from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry import metrics

from core.settings.dev import get_settings


settings = get_settings()

otlp_exporter = OTLPMetricExporter(endpoint=settings.otlp.otlp_url, insecure=True)

otlp_metric_reader = PeriodicExportingMetricReader(exporter=otlp_exporter)

prometheus_reader = PrometheusMetricReader()

current_metrics_provider = metrics.get_meter_provider()

resource = Resource(
    attributes={
        "service.name": "sender_service",
    }
)

if not isinstance(current_metrics_provider, MeterProvider):
    metrics_provider = MeterProvider(
        metric_readers=[prometheus_reader, otlp_metric_reader],
        resource=resource,
    )
    metrics.set_meter_provider(metrics_provider)

else:
    metrics_provider = current_metrics_provider

meter = metrics.get_meter("app")