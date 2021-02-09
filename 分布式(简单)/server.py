import random, time, queue
from multiprocessing.managers import BaseManager
import threading
import time
import traceback
# 发送任务的队列:
task_queue = queue.Queue()
# 接收结果的队列:
result_queue = queue.Queue()

# 从BaseManager继承的QueueManager:
class QueueManager(BaseManager):
    pass

def get_result(result):
    print('Try get results...')
    for i in range(50):
        r = result.get(timeout=30)
        print('Result: %s' % r)

def put_task(task):
    for i in range(50):
        n = random.randint(0, 50)
        print('Put task %d...' % n)
        task.put(n)
        time.sleep(0.5)

def create_server():
    # 把两个Queue都注册到网络上, callable参数关联了Queue对象:
    task = None
    result = None
    manager = None
    try:
        QueueManager.register('get_task_queue', callable=lambda: task_queue)
        QueueManager.register('get_result_queue', callable=lambda: result_queue)
        # 绑定端口5000, 设置验证码'abc':
        manager = QueueManager(address=('', 5000), authkey=b'abc') #需要设定特定的ip
        # 启动Queue:
        manager.start()
        # 获得通过网络访问的Queue对象:
        task = manager.get_task_queue()
        result = manager.get_result_queue()
    except Exception as e:
        traceback.print_exc()
    return task, result, manager

def main():
    task, result, manager = create_server()
    if task is None or result is None or manager is None:
        print('Error happened when create server.')
        return

    t_result = threading.Thread(target=get_result, args=(result, ))
    t_result.start()
    t_task = threading.Thread(target=put_task, args=(task, ))
    t_task.start()
    t_task.join()
    t_result.join()
    # 关闭
    manager.shutdown()
    print('master exit.')

if __name__ == '__main__':
    main()
