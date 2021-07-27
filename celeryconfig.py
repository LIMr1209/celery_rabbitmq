BROKER_URL = 'amqp://guest:guest@localhost:5672'  # 使用RabbitMQ作为消息代理

CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'  # 把任务结果存在了Redis
