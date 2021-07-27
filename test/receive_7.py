import pika

# 创建凭证，使用rabbitmq用户名/密码登录
credentials = pika.PlainCredentials("guest", "guest")
# 创建连接
connection = pika.BlockingConnection(pika.ConnectionParameters("127.0.0.1", credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue="rpc_queue")

def fib(n):
    """
    斐波那契数列
    :param n:
    :return:
    """
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)

def on_request(ch, method, props, body):
    n = int(body)
    print(" [.] fib(%s)" % n)
    response = fib(n)
    ch.basic_publish(exchange="",
                     # 数据发送到生产端随机生成的queue
                     routing_key=props.reply_to,
                     # 同时把correlation_id值设置为生产端传过来的值。
                     properties=pika.BasicProperties(
                         correlation_id=props.correlation_id,
                     ),
                     # 把fib()的结果返回给生产端
                     body=str(response))
    # 确保任务完成
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume("rpc_queue", on_request, False)
print(" [x] Awaiting RPC requests")
channel.start_consuming()