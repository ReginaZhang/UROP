# adding 'test_modules' directory to the path
import os
path = os.getcwd()
import sys
sys.path.append(path+"\\test_modules")

from loginGS import LoginGS
from threading import Thread

def make_threadlist():
    '''
    make_threadlist()

    Description:
        making a list of threads to run simultaniously
    Return:
        a list of threads
    '''
    firefox = LoginGS("firefox")
    chrome = LoginGS("chrome")
    t1 = Thread(target = firefox.login)
    t2 = Thread(target = chrome.login)
    threads = []
    threads.append(t1)
    threads.append(t2)
    return threads

def threading_test(threads_list):
    '''
    threading_test(threads_list)

    Description:
        to start and join the threads
    Param:
        threads_list - a list of threads
    '''
    for thread in threads_list:
        thread.start()
    for thread in threads_list:
        thread.join()

def main():
    '''
    do the testing
    '''
    threads = make_threadlist()
    threading_test(threads)

if __name__ == "__main__":
    main()
