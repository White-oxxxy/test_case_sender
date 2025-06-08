from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

from core.settings.dev import get_settings


settings = get_settings()

otlp_trace_exporter = OTLPSpanExporter(endpoint=settings.otlp.otlp_url, insecure=True)

span_processor = BatchSpanProcessor(otlp_trace_exporter)

current_trace_provider = trace.get_tracer_provider()

resource = Resource(
    attributes={
        "service.name": "sender_service",
    }
)

if not isinstance(current_trace_provider, TracerProvider):
    trace_provider = TracerProvider(resource=resource)
    trace_provider.add_span_processor(span_processor)
    trace.set_tracer_provider(trace_provider)

else:
    trace_provider = current_trace_provider

tracer = trace.get_tracer("app")