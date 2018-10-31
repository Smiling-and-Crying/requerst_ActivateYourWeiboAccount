import time

from lib.GetUserPwd import GetUserPwd

class GetUserPwdTest(GetUserPwd):
    def __init__(self):
        super(GetUserPwdTest, self).__init__(get_count_once=2)

    def getUserPwdInterface(self):
        return [{"152xxxxx": "xxxxxxx"}, {"138xxxxxxx": "xxxxxxxx"}]



def main():
    print("start..........")
    o = GetUserPwdTest()
    o.run(o.getUserPwdInterface)
    while True:
        ret = o.getUPfromQ()
        print(ret)
        time.sleep(1)

if __name__ == '__main__':
    main()