import pika
import sys
# 建立与rabbitmq的连接
credentials = pika.PlainCredentials("guest","guest")
connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1',credentials=credentials))
channel = connection.channel()
# 生产者和消费者端都要声明队列，以排除生成者未启动，消费者获取报错的问题
channel.exchange_declare(exchange="topic_logs", exchange_type="topic")
# 不指定queue名字，rabbit会随机分配一个名字
# exclusive=True会在使用此queue的消费者断开后，自动将queue删除
result = channel.queue_declare(queue="", exclusive=True)
# 获取随机的queue名字
queue_name = result.method.queue
print("random queuename", queue_name)

#绑定键。‘#’匹配所有字符，‘*’匹配一个单词
binding_keys = ['[warn].*', 'info.*']

if not binding_keys:
    sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
    sys.exit(1)

for binding_key in binding_keys:
    channel.queue_bind(exchange='topic_logs', queue=queue_name, routing_key=binding_key)

print("Waiting for log!")

def callback(ch,method,properties,body):
    print(" [x] %r:%r" % (method.routing_key, body))

channel.basic_consume(queue_name,callback,True)
# 开始消费，接收消息
channel.start_consuming()