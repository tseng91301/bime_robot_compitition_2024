import threading
import time

def worker(name):
    print(f'{name} 开始工作')
    time.sleep(2)  # 模拟工作耗时
    print(f'{name} 完成工作')

# 创建两个线程
thread1 = threading.Thread(target=worker, args=('线程1',))
thread2 = threading.Thread(target=worker, args=('线程2',))

# 启动线程
thread1.start()
thread2.start()

# # 等待线程完成
# thread1.join()
# thread2.join()

print('所有线程已完成')
