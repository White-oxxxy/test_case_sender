from .metrics_exporter import meter

# --- Taskiq ---

task_duration = meter.create_histogram(
    name="task_duration_seconds",
    unit="s",
    description="Время выполнения таски",
)

task_counter = meter.create_counter(
    name="task_invocations_total",
    description="Количество вызовов таски"
)

task_success_counter = meter.create_counter(
    name="task_success_total",
    description="Количество успешных выполнений задач",
)

task_error_counter = meter.create_counter(
    name="task_errors_total",
    description="Количество ошибочных выполнений задач",
)