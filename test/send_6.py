# topic模式类似于direct模式，只是其中的routing_key变成了一个有“.”分隔的字符串，“.”将字符串分割成几个单词，
# 每个单词代表一个条件；
#
# 话题类型，可以根据正则进行更精确的匹配，按照规则过滤。
# exchange_type="topic"。
# 在topic类型下，可以让队列绑定几个模糊的关键字，之后发送者将数据发送到exchange,exchange将传入"路由值"和"关键字"进行匹配，匹配成功，将数据发送到指定队列。
# #表示可以匹配0个或多个单词
# *表示只能匹配一个单词

# 之前事例，发送消息时明确指定某个队列并向其中发送消息，RabbitMQ还支持根据关键字发送，
# 即：队列绑定关键字，发送者将数据根据关键字发送到消息exchange，exchange根据 关键字 判定应该将数据发送至指定队列。


import pika
import sys
# 创建凭证，使用rabbitmq用户名/密码登录
credentials = pika.PlainCredentials("guest", "guest")
# 创建连接
connection = pika.BlockingConnection(pika.ConnectionParameters("127.0.0.1", credentials=credentials))
# 创建频道
channel = connection.channel()
# 这里是topic，不需要声明queue
channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

#这里关键字必须为点号隔开的单词，以便于消费者进行匹配。
routing_key = '[warn].info'
channel.basic_publish(exchange="topic_logs",
                      routing_key=routing_key,
                      body="vita send message")
print("消息发送完成")
connection.close()