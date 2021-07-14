#스레드 개요

import _thread
import time
import random


def DoItThread(str):
    cnt = 0
    while(cnt<10):
        time.sleep(random.randint(0,100)/300.0)
        print(str,cnt)
        cnt+=1

_thread.start_new_thread(DoItThread,("홍길동",))
_thread.start_new_thread(DoItThread,("강감찬",))
print("멈추고 싶으면 아무키나 누르세요.")
input()