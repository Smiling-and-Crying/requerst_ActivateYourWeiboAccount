import os
import sys
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,BASE_PATH)


def main():
    print("程序开始执行....")

if __name__ == '__main__':
    print("Hello Git")
