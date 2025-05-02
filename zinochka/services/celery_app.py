from celery import Celery

# Create the Celery app with RabbitMQ as broker
celery_app = Celery(
    "zinochka",
    broker="amqp://guest:guest@rabbitmq:5672//",
    include=["zinochka.services.tasks"]
)

# Optional configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

if __name__ == "__main__":
    celery_app.start()