from abc import ABCMeta, abstractmethod
from queue import Queue

class GetUserPwd(metaclass=ABCMeta):
    def __init__(self,q_size=50,min_count=5):
        self.__user_pwd_pool = Queue(maxsize=q_size)
        self.__min_count = 5



    @abstractmethod
    def getUserPwd(self):
        """
        必须实现的获取用户名和密码的方法
        :return: [{"User":"Pwd"},...]
        """
        pass

