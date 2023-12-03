from concurrent.futures import ThreadPoolExecutor

pool = ThreadPoolExecutor(max_workers=10)

def task(arg):
    print(f"Processing task: {arg}")

for i in range(10):
    pool.submit(task, i)

pool.shutdown()