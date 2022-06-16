# pynput参考资料 https://blog.csdn.net/forward_huan/article/details/107991355

import time
import win32api
import win32con
import pydirectinput
import fish3
from gui32 import My_gui32
from threading import Thread


def test():
    time.sleep(3)
    mouse_move(200, 500)
    mouse_click()
    time.sleep(3)
    key_click("m")


def key_click(key_str):
    pydirectinput.keyDown(key_str)
    pydirectinput.keyUp(key_str)


def mouse_click():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def mouse_move(x, y):
    # (左-右+，上-下+)
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x, y)


if __name__ == "__main__":
    # char_list = [[228, 691], [398, 759], [579, 797], [866, 795], [1046, 759], [1217, 691]]
    # char_list_2 = [[228, 697], [398, 765], [579, 803], [866, 801], [1046, 765], [1217, 697]]
    # [+32, -83] [+32, -83] [+18, -83] [-18, -83] [-32, -83] [-32, -83]
    my = My_gui32()

    # list1 = fish3.SearchImage(my.hwndMain)
    # print(list1)
    thread1 = Thread(target=fish3.window_capture, daemon=True, args=(my.hwndMain, "1", [260, 614]))  # 创建一个子线程，用于接收数据
    thread1.start()  # 启动子线程

    thread2 = Thread(target=fish3.window_capture, daemon=True, args=(my.hwndMain, "2", [430, 682]))  # 创建一个子线程，用于接收数据
    thread2.start()  # 启动子线程

    thread3 = Thread(target=fish3.window_capture, daemon=True, args=(my.hwndMain, "3", [597, 720]))  # 创建一个子线程，用于接收数据
    thread3.start()  # 启动子线程

    thread4 = Thread(target=fish3.window_capture, daemon=True, args=(my.hwndMain, "4", [848, 718]))  # 创建一个子线程，用于接收数据
    thread4.start()  # 启动子线程

    thread5 = Thread(target=fish3.window_capture, daemon=True, args=(my.hwndMain, "5", [1014, 682]))  # 创建一个子线程，用于接收数据
    thread5.start()  # 启动子线程
    #
    thread6 = Thread(target=fish3.window_capture, daemon=True, args=(my.hwndMain, "6", [1185, 614]))  # 创建一个子线程，用于接收数据
    thread6.start()  # 启动子线程

    while True:
        if win32api.GetKeyState(ord('Q')) < 0:  # [-127 1 -128 0]循环，其中负数是按下，非负数是抬起，且有些类似于Ctrl的按键是全局的
            break
        time.sleep(0.1)

    print("程序结束")
    exit(0)

