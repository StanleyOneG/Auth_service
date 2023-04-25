from flask import request
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from functools import wraps


def trace_this(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        tracer = trace.get_tracer(__name__)
        request_id = request.headers.get('X-Request-Id')
        with tracer.start_as_current_span(func.__name__) as span:
            span.set_attribute('http.request_id', request_id)
            return func(*args, **kwargs)

    return wrapper


def configure_tracer() -> None:
    trace.set_tracer_provider(
        TracerProvider(resource=Resource.create({SERVICE_NAME: "Auth API"}))
    )
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(
            JaegerExporter(
                agent_host_name='jaeger',
                agent_port=6831,
            )
        )
    )
    # Чтобы видеть трейсы в консоли
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(ConsoleSpanExporter())
    )
