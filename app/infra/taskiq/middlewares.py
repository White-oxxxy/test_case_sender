import contextvars
import time
from typing import (
    Any,
    Coroutine,
)

from opentelemetry.context import (
    attach,
    detach,
)
from opentelemetry.propagate import extract
from opentelemetry import trace
from taskiq import (
    TaskiqMiddleware,
    TaskiqMessage,
    TaskiqResult,
)

from infra.monitoring.metrics.custom_metrics import (
    task_duration,
    task_counter,
    task_error_counter,
    task_success_counter,
)
from infra.monitoring.trace_exporter import tracer


otel_span_var = contextvars.ContextVar("otel_span")
start_time_var = contextvars.ContextVar("start_time")
otel_ctx_token_var = contextvars.ContextVar("otel_ctx_token")


class MetricsMiddleWares(TaskiqMiddleware):
    def pre_execute(self, message: TaskiqMessage):
        span = tracer.start_span(
            name=f"task:{message.task_name}",
            kind=trace.SpanKind.INTERNAL,
        )

        token = attach(trace.set_span_in_context(span))

        otel_span_var.set(span)
        otel_ctx_token_var.set(token)
        start_time_var.set(time.perf_counter())

        return message

    def post_execute(
        self,
        message: TaskiqMessage,
        result: TaskiqResult[Any],
    ) -> None | Coroutine[Any, Any, None]:
        self._finish_span(result)

        return None

    def on_error(
        self,
        message: TaskiqMessage,
        result: TaskiqResult[Any],
        exception: BaseException,
    ) -> None | Coroutine[Any, Any, None]:
        self._finish_span(result, is_error=True)

        return None

    def _finish_span(
        self,
        result: TaskiqResult[Any],
        is_error: bool = False
    ):
        if hasattr(result, "task_name"):
            task_name: str = result.task_name
        else:
            task_name: str = "unknown"

        labels = {"task_name": task_name}

        try:
            span = otel_span_var.get()
            token = otel_ctx_token_var.get()
            start_time = start_time_var.get()

        except LookupError:
            return

        duration = time.perf_counter() - start_time

        task_duration.record(duration, labels)
        task_counter.add(1, labels)

        if is_error or (getattr(result, "is_err", False)):
            task_error_counter.add(1, labels)

            span.record_exception(result.exception if hasattr(result, "exception") else None)
            span.set_status(trace.Status(trace.StatusCode.ERROR))

        else:
            task_success_counter.add(1, labels)

        span.end()

        detach(token)

