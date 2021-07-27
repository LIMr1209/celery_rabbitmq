import pika
# 建立与rabbitmq的连接
credentials = pika.PlainCredentials("guest","guest")
connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1',credentials=credentials))
channel = connection.channel()
channel.exchange_declare(exchange="log", exchange_type="fanout")
# 不指定queue名字，rabbit会随机分配一个名字
# exclusive=True会在使用此queue的消费者断开后，自动将queue删除
result = channel.queue_declare(queue="", exclusive=True)
# 获取随机的queue名字
queue_name = result.method.queue
print("random queuename", queue_name)
channel.queue_bind(exchange="log",  # queue绑定到转发器上
                   queue=queue_name)
print("Waiting for log!")

def callback(ch,method,properties,body):
    print("消费者接收到了任务：%r"%body.decode("utf8"))

# auto_ack设置为False
channel.basic_consume(queue_name,callback,True)
# 开始消费，接收消息
channel.start_consuming()