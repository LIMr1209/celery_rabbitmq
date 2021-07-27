import pika
# 建立与rabbitmq的连接
credentials = pika.PlainCredentials("guest","guest")
connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1',credentials=credentials))
channel = connection.channel()
channel.queue_declare(queue="SH")

def callback(ch,method,properties,body):
    print("消费者接收到了任务：%r"%body.decode("utf8"))
    # 有消息来临，立即执行callback，没有消息则夯住，等待消息
    # 老百姓开始去邮箱取邮件啦，队列名字是水许传
# 第一个参数是队列
# 第二个是回调函数
# 第三个这是auto_ack=True
channel.basic_consume("SH",callback,True)
# 开始消费，接收消息
channel.start_consuming()