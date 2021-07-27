# 前面的效果都是一对一发，如果做一个广播效果可不可以，这时候需要用到exchange了。
# exchange必须明确的知道，收到的消息要发送给谁。
# exchange的类型决定了怎么处理。类型有以下几种
# 1.fanout：exchange将消息发送给和该exchange连接的所有queue；也就是所谓的广播模式；此模式下忽略routing_key
# 2.direct：通过routingKey和exchange决定的那个唯一的queue可以接收消息，只有routing_key为"black"时才可以将其发送到队列queue_name；
# 3.topic：所有符合routingKey(此时可以是一个表达式)的routingKey所bind的queue可以接收消息
#
# exchange type 过滤类型
# 　　　　fanout = 广播
# 　　　　direct = 组播
# 　　　　topic = 规则播
# 　　　　header = 略过。。。


# 注意：广播是实时的，没有客户端接收，消息就没有了，不会保存下来，不会等待客户端启动时接受消息。类似收音机。
# 所以在发送消息前，要先启动客户端，准备接受消息，然后启动服务端发送消息。

# 广播
# 需要queue和exchange绑定，因为消费者不是和exchange直连的，消费者连接在queue上，queue绑定在exchange上，消费者只会在queue里读取消息。


import pika
# 创建凭证，使用rabbitmq用户名/密码登录
credentials = pika.PlainCredentials("guest", "guest")
# 创建连接
connection = pika.BlockingConnection(pika.ConnectionParameters("127.0.0.1", credentials=credentials))
# 创建频道
channel = connection.channel()
# 这里是广播，不需要声明queue
channel.exchange_declare(exchange="log",  # 声明广播管道
                         exchange_type="fanout")
# delivery_mode=2代表消息持久化
channel.basic_publish(exchange="log",
                      routing_key="",  # 此处为空，必须有
                      body="fanout 持久化 来啦来啦！")
print("消息发送完成")
connection.close()