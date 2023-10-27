import queue
import threading

class queue_handler_class:
    def queue_handler(work_list):
        # 작업 큐 생성
        work_list = queue.Queue()

        while True:
            # 작업 큐에서 작업 가져오기
            work = work_list.get()

            # 작업 수행
            work()