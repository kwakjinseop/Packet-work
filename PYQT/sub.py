import threading


def calculate(partial_works):
    for work in partial_works:
        result = work * 1000
        results.append(work)


works = [x for x in range(1000)]
results = []

# 스레드 개수와 스레드 리스트
thread_count = 10
threads = []

# 새로운 스레드 생성/실행 후 스레드 리스트에 추가
for i in range(thread_count):
    thread = threading.Thread(target=calculate, args=(works[i * 100: (i + 1) * 100],), )
    thread.start()
    threads.append(thread)

# 메인 스레드는 각 스레드의 작업이 모두 끝날 때까지 대기
for thread in threads:
    thread.join()

print("Finished")