# 路由模式，通过routing_key将消息发送给对应的queue;
# 如下面这句话，可以设置exchange为direct模式，只有routing_key为"black"时才将其发送到队列queue_name;
# channel.queue_bind(exchange=exchange_name,queue=queue_name,routing_key='black')

import pika
import sys
# 创建凭证，使用rabbitmq用户名/密码登录
credentials = pika.PlainCredentials("guest", "guest")
# 创建连接
connection = pika.BlockingConnection(pika.ConnectionParameters("127.0.0.1", credentials=credentials))
# 创建频道
channel = connection.channel()
# 这里是组播，不需要声明queue
channel.exchange_declare(exchange="direct_logs",  # 声明组播管道
                         exchange_type="direct")
# 重要程度级别，这里默认定义为 info
severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
message = ' '.join(sys.argv[2:]) or 'Hello World!'

channel.basic_publish(exchange="direct_logs",
                      routing_key=severity,
                      body=message)
print(" [x] Sent %r:%r" % (severity, message))
connection.close()