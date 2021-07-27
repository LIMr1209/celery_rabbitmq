# 上面的所有例子中，队列都是单向的，一端发送，一端接收。
# 如果发送端想接收消费端处理的数据，怎么办呢，这就需要RPC（remote procedure call）远程过程调用了。

# 1.生产端 生成rpc_queue队列，这个队列负责把消息发给消费端。
# 2.生产端 生成另外一个随机队列callback_queue，这个队列是发给消费端，消费者用这个队列把处理好的数据发送给生产端。
# 3.生产端 生成一组唯一字符串UUID，发送给消费者，消费者会把这串字符作为验证在发给生产者。
# 4.当消费端处理完数据，发给生产端，会把处理数据与UUID一起通过随机生产的队列callback_queue发回给生产端。
# 5.生产端，会使用while循环 不断检测是否有数据，并以这种形式来实现阻塞等待数据，来监听消费端。
# 6.生产端获取数据调用回调函数，回调函数判断本机的UUID与消费端发回UID是否匹配，由于消费端，可能有多个，且处理时间不等所以需要判断，判断成功赋值数据，while循环就会捕获到，完成交互。

import pika
import uuid
import time


class FibRpcClient(object):
    def __init__(self):
        credentials = pika.PlainCredentials("guest", "guest")
        # 1.创建连接
        self.connection = pika.BlockingConnection(pika.ConnectionParameters("127.0.0.1", credentials=credentials))
        self.channel = self.connection.channel()
        # 2.生成随机queue
        # exclusive = True,消费者端断开连接，队列删除
        result = self.channel.queue_declare(queue="", exclusive=True)
        # 随机获取queue名字，发送数据给消费端
        self.callback_queue = result.method.queue
        # self.on_response回调函数:只要收到消息就调用这个函数
        # 声明收到消息后，收queue=self.callback_queue内的消息
        self.channel.basic_consume(self.callback_queue, self.on_response, True)

    def on_response(self, ch, method, properties, body):
        """
        收到消息就调用该函数
        :param ch: 管道内存对象
        :param method: 消息发送给哪个queue
        :param props:
        :param body: 数据对象
        :return:
        """
        # 判断随机生成的ID与消费者端发过来的ID是否相同，
        if self.corr_id == properties.correlation_id:
            # 将body值给self.response
            print("接收到客户端发送的信息：", body)
            self.response = body

    def call(self, n):
        # 赋值变量，一个循环值
        self.response = None
        # 随机生成唯一的字符串
        self.corr_id = str(uuid.uuid4())

        self.channel.basic_publish(exchange="",
                                   routing_key="rpc_queue",
                                   properties=pika.BasicProperties(
                                       # 告诉消费端，执行命令成功后把结果返回给该队列
                                       reply_to=self.callback_queue,
                                       # 生成UUID，发送给消费端
                                       correlation_id=self.corr_id,
                                   ),
                                   # 发的消息，必须传入字符串，不能传数字
                                   body=str(n))
        # 没有数据就循环接收数据
        while self.response is None:
            # 非阻塞版的start_consuming()
            # 注意，在这里不使用start_consuming去获取数据，因为这样会堵塞再这里，我们使用了另一种方法self.connection.process_data_events()
            # 没有消息不会阻塞
            self.connection.process_data_events()
            print("client does not send data")
            time.sleep(1)
        # 接收到了消费端的结果，返回
        return int(self.response)


fib_rpc = FibRpcClient()
print("[x] Requesting fib(6)")
response = fib_rpc.call(6)
print(" [.] Got %r" % response)
time.sleep(1000)