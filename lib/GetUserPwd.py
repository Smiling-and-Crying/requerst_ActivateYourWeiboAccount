from abc import ABCMeta, abstractmethod
from queue import Queue
import queue
import threading
import time

class GetUserPwd(metaclass=ABCMeta):
    def __init__(self,get_count_once=1,q_size=50,min_count=15,max_try_count=5):
        self.__q_size = q_size
        self.__min_count = min_count
        self.__max_try_count = max_try_count
        self.__get_count_once = get_count_once


        self.__background_thread_switch = True
        self.__thLock = threading.Condition()  #声明通知锁
        self.__user_pwd_pool = Queue(maxsize=self.__q_size)  #保存用户名密码的列表


    def set_background_thread_switch_close(self):
        """关闭后台获取用户名密码自动填充的程序"""
        self.__background_thread_switch = False

    def autoGetUser(self,fun):
        """后台获取用户名密码，等待通知，自动获取并填充用户名队列"""
        self.__thLock.acquire() #枷锁
        try:
            while self.__background_thread_switch:
                self.__thLock.wait() #进入等待池
                print("填充开始....当前Q数量:[%s]"%str(self.__user_pwd_pool.qsize()))
                while True:
                    try:
                        try:
                            need_count = self.__q_size - self.__user_pwd_pool.qsize()
                            co = int(need_count / self.__get_count_once)
                        except Exception as e:
                            co = 1
                        result = []
                        for i in range(co):
                            result+=fun()
                        if result:
                            self.__user_pwd_pool.not_full.acquire()
                            try:
                                for item in result:
                                    self.__user_pwd_pool._put(item)
                                    self.__user_pwd_pool.unfinished_tasks += 1
                            finally:
                                self.__user_pwd_pool.not_empty.notify()
                                self.__user_pwd_pool.not_full.release()
                                self.__thLock.notify()
                                print("填充结束,当前Q数量:[%s]"%str(self.__user_pwd_pool.qsize()))
                        else:
                            print("Interface 未获取到内容...")
                            time.sleep(2)
                            continue
                        break
                    except Exception as e:
                        print("Interface 定义错误,err:",e)
        finally:
            self.__thLock.release()

    def getUPfromQ(self):
        """
        从Q中获取一条用户名密码组合
        :return:{"User":"Pwd"}
        """
        self.__thLock.acquire()
        try:
            for i in range(self.__max_try_count):
                try:
                    user_item = self.__user_pwd_pool.get_nowait()
                    if self.__user_pwd_pool.qsize() <= self.__min_count:
                        self.__thLock.notify()
                    return user_item

                except queue.Empty:
                    self.__thLock.notify()
                    self.__thLock.wait(None)
                except Exception as e:
                    pass
        finally:
            self.__thLock.release()


    def run(self,fun):
        threading.Thread(target=self.autoGetUser,args=(fun,)).start()


    @abstractmethod
    def getUserPwdInterface(self):
        """
        必须实现的获取用户名和密码的方法
        :return: [{"User":"Pwd"},...]
        """
        return [{"User":"Pwd"},]

