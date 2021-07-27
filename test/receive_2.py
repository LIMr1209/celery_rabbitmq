# 默认情况下，auto_ack=True，
# 生产者发送数据给队列，消费者取出消息后，数据将会被删除。
# 特殊情况，如果消费者处理过程中，出现错误，数据处理没有完成，那么该数据将从队列中丢失。
# ACK机制用于保证消费者如果拿了队列的消息，客户端处理时出错了，那么队列中仍然存在这个消息，提供下一位消费者继续取
#
# 不确认机制：
# 即每次消费者接收到数据后，不管是否处理完成，rabbitmq-server都会把这个消息标记完成，从队列中删除。

# 当设置 auto_ack=False 拿到消息必须给rabbitmq服务端回复ack，否则消息不会被删除。防止客户端出错，数据丢失
import pika
# 建立与rabbitmq的连接
credentials = pika.PlainCredentials("guest","guest")
connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1',credentials=credentials))
channel = connection.channel()
channel.queue_declare(queue="SH2")

# auto_ack 为true 只要接受消息就会清除
# auto_ack 为Flase 消息不清除
# 回调使用 ch.basic_ack(delivery_tag=method.delivery_tag) 清除消息
def callback(ch,method,properties,body):
    print("消费者接收到了任务：%r"%body.decode("utf8"))
    # 演示报错，消息仍然存在,取消下面的int注释。
    # int("qwqwqwq")
    # 有消息来临，立即执行callback，没有消息则夯住，等待消息
    ch.basic_ack(delivery_tag=method.delivery_tag)
channel.basic_consume("SH2",callback,False)
# 开始消费，接收消息
channel.start_consuming()