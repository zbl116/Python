import time, sys, queue
from multiprocessing.managers import BaseManager
import traceback
import threading

# 创建类似的QueueManager:
class QueueManager(BaseManager):
    pass

def get_task_handle(task, result):
    while not task.empty():
        num = task.get(True, timeout=1)
        print(num)
        ret = '%d * %d = %d' % (num, num, num * num)
        time.sleep(1)
        result.put('agent1----%s' % str(ret))

def connect_server():
    # 由于这个QueueManager只从网络上获取Queue，所以注册时只提供名字:
    QueueManager.register('get_task_queue')
    QueueManager.register('get_result_queue')
    # 连接到服务器，也就是运行task_master.py的机器:
    server_addr = '127.0.0.1' # 当处于不同的服务器上时，需要关闭server的防火墙或者设置端口例外，不然连接不上
    print('Connect to server %s...' % server_addr)
    # 端口和验证码注意保持与task_master.py设置的完全一致:
    m = QueueManager(address=(server_addr, 5000), authkey=b'abc')
    m.connect()
    task = m.get_task_queue()
    result = m.get_result_queue()
    return task, result

def main():
    task, result = connect_server()
    get_task_handle(task, result)
    print('worker1 exit.')

if __name__ == '__main__':
    main()
