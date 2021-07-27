import pika
import sys
# 建立与rabbitmq的连接
credentials = pika.PlainCredentials("guest","guest")
connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1',credentials=credentials))
channel = connection.channel()
# 生产者和消费者端都要声明队列，以排除生成者未启动，消费者获取报错的问题
channel.exchange_declare(exchange="direct_logs", exchange_type="direct")
# 不指定queue名字，rabbit会随机分配一个名字
# exclusive=True会在使用此queue的消费者断开后，自动将queue删除
result = channel.queue_declare(queue="", exclusive=True)
# 获取随机的queue名字
queue_name = result.method.queue
print("random queuename", queue_name)
severities = sys.argv[1:]
if not severities:
    sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
    sys.exit(1)
# 循环列表去绑定
for severity in severities:
    print(severity)
    channel.queue_bind(exchange='direct_logs', queue=queue_name, routing_key=severity)
print("Waiting for log!")

def callback(ch,method,properties,body):
    print(" [x] %r:%r" % (method.routing_key, body))

# auto_ack设置为False
channel.basic_consume(queue_name,callback,True)
# 开始消费，接收消息
channel.start_consuming()