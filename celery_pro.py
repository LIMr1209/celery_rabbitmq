from celery import Celery

# 为了提高性能，官方推荐使用librabbitmq，这是一个连接rabbitmq的C++的库；
# pip install celery[librabbitmq]
app = Celery('celery', include=['tasks'])

app.config_from_object('celeryconfig')
