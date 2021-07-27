# 上面我们看到，我重启后，队列全部没有了。
# 为了保证RabbitMQ在退出或者异常情况下数据没有丢失，需要将queue，exechange和Message都持久化。
# 持久化步骤：
# 1.队列持久化
# 每次声明队列的时候，都加上durable，注意每个队列都要写，客户端和服务端声明的时候都要写。
#
# #在管道里声明
# queue channel.queue_declare(queue=‘hello2‘, durable=True)
#
# 2.消息持久化
# 发送端发送消息时，加上properties
# properties=pika.BasicProperties(
# delivery_mode=2, # 消息持久化
# )

import pika
# 创建凭证，使用rabbitmq用户名/密码登录
credentials = pika.PlainCredentials("guest", "guest")
# 创建连接
connection = pika.BlockingConnection(pika.ConnectionParameters("127.0.0.1", credentials=credentials))
# 创建频道
channel = connection.channel()
# 新建一个队列，用于接收消息
# 默认情况下，此队列不支持持久化，如果服务挂掉，数据丢失
# durable=True开启持久化，必须新开启一个队列，原本的队列已经不支持持久化了
channel.queue_declare(queue="SH3", durable=True)

# delivery_mode=2代表消息持久化
channel.basic_publish(exchange="",
                      routing_key="SH3",
                      body="SH3 持久化 来啦来啦！",
                      # 数据持久化
                      properties=pika.BasicProperties(delivery_mode=2))
print("消息发送完成")