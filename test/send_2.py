import pika
# 创建凭证，使用rabbitmq用户名/密码登录
credentials = pika.PlainCredentials("guest", "guest")
# 创建连接
connection = pika.BlockingConnection(pika.ConnectionParameters("127.0.0.1", credentials=credentials))
# 创建频道
channel = connection.channel()
# 新建一个队列，用于接收消息
channel.queue_declare(queue="SH2")
# 注意，在rabbitmq中，消息要发送给队列，必须经过交换(exchange)
# 可以使用空字符串交换(exchange="")
# 精确的指定发送给哪个队列(routing_key=""),参数body值发送的数据
channel.basic_publish(exchange="",
                      routing_key="SH2",
                      body="SH2 来啦来啦！")
print("消息发送完成")
connection.close()