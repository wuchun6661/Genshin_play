import win32gui, win32ui, win32con, win32api
import time
import cv2
import numpy as np
from threading import Thread


def mouse_click():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def mouse_move(x, y):
    # (左-右+，上-下+)
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x, y)


def key_loop(num, short_list, long_list, flag):
    while True:
        time.sleep(0.01)
        if short_list[0]:
            # print('*********')
            short_list[0] = 0
            time.sleep(0.05)
            if num == "1":
                win32api.keybd_event(65, 0, 0, 0)
                win32api.keybd_event(65, 0, win32con.KEYEVENTF_KEYUP, 0)

            if num == "2":
                win32api.keybd_event(83, 0, 0, 0)
                win32api.keybd_event(83, 0, win32con.KEYEVENTF_KEYUP, 0)

            if num == "3":
                win32api.keybd_event(68, 0, 0, 0)
                win32api.keybd_event(68, 0, win32con.KEYEVENTF_KEYUP, 0)

            if num == "4":
                win32api.keybd_event(74, 0, 0, 0)
                win32api.keybd_event(74, 0, win32con.KEYEVENTF_KEYUP, 0)

            if num == "5":
                win32api.keybd_event(75, 0, 0, 0)
                win32api.keybd_event(75, 0, win32con.KEYEVENTF_KEYUP, 0)

            if num == "6":
                win32api.keybd_event(76, 0, 0, 0)
                win32api.keybd_event(76, 0, win32con.KEYEVENTF_KEYUP, 0)

        if long_list[0]:
            long_list[0] = 0
            time.sleep(0.05)

            if num == "1":
                if flag[0] < 0:
                    win32api.keybd_event(65, 0, 0, 0)
                else:
                    win32api.keybd_event(65, 0, win32con.KEYEVENTF_KEYUP, 0)

            if num == "2":
                if flag[0] < 0:
                    win32api.keybd_event(83, 0, 0, 0)
                else:
                    win32api.keybd_event(83, 0, win32con.KEYEVENTF_KEYUP, 0)

            if num == "3":
                if flag[0] < 0:
                    win32api.keybd_event(68, 0, 0, 0)
                else:
                    win32api.keybd_event(68, 0, win32con.KEYEVENTF_KEYUP, 0)

            if num == "4":
                if flag[0] < 0:
                    win32api.keybd_event(74, 0, 0, 0)
                else:
                    win32api.keybd_event(74, 0, win32con.KEYEVENTF_KEYUP, 0)

            if num == "5":
                if flag[0] < 0:
                    win32api.keybd_event(75, 0, 0, 0)
                else:
                    win32api.keybd_event(75, 0, win32con.KEYEVENTF_KEYUP, 0)

            if num == "6":
                if flag[0] < 0:
                    win32api.keybd_event(76, 0, 0, 0)
                else:
                    win32api.keybd_event(76, 0, win32con.KEYEVENTF_KEYUP, 0)
            flag[0] = -flag[0]


def window_capture(hwnd=0, num="2", pos_char=[398, 759]):
    short_list = [0]
    long_list = [0]
    flag = [-1]
    yellow_interval = 0.15
    purple_interval = 0.15
    last_time = time.time()
    thread = Thread(target=key_loop, daemon=True, args=(num, short_list, long_list, flag))  # 创建一个子线程，用于接收数据
    thread.start()  # 启动子线程
    ###########尺寸###########
    d = 130  # 监测区域边长
    pos_circle = [pos_char[0], pos_char[1] - 44]  # 圆心位置
    start_wh = (pos_circle[0] - d//2, pos_circle[1] - d//2)  # 检测框左上角坐标
    end_wh = (start_wh[0] + d, start_wh[1] + d)  # 检测框右下角坐标
    size_wh = (end_wh[0] - start_wh[0], end_wh[1] - start_wh[1])  # 检测区域的宽高
    w = size_wh[0]
    h = size_wh[1]

    # hwnd = 0  # 窗口的编号，0号表示当前活跃窗口
    hwndDC = win32gui.GetWindowDC(hwnd)  # 根据窗口句柄获取窗口的设备上下文DC(Divice Context)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)  # 根据窗口的DC获取mfcDC
    saveDC = mfcDC.CreateCompatibleDC()  # mfcDC创建可兼容的DC
    saveBitMap = win32ui.CreateBitmap()  # 创建bigmap准备保存图片
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)  # 为bitmap开辟空间

    print("线程"+num+"已启动")
    ###################################################
    while True:
        saveDC.SelectObject(saveBitMap)  # 高度saveDC，将截图保存到saveBitmap中
        saveDC.BitBlt((0, 0), size_wh, mfcDC, start_wh, win32con.SRCCOPY)  # 截取从(100，100)长宽为(w，h)的图片

        signedIntsArray = saveBitMap.GetBitmapBits(True)
        im_opencv = np.frombuffer(signedIntsArray, dtype='uint8')
        im_opencv.shape = (h, w, 4)
        im_opencv = cv2.cvtColor(im_opencv, cv2.COLOR_BGRA2BGR)
        ###############################检测################################
        Filename_yellow = "yellow_ball" + num + ".png"  # home.png
        Filepath_yellow = "./resource/imagefind/" + Filename_yellow  # ./resource/imagefind/home.png
        yellow = cv2.imread(Filepath_yellow)

        Filename_purple = "purple_ball" + num + ".png"  # home.png
        Filepath_purple = "./resource/imagefind/" + Filename_purple  # ./resource/imagefind/home.png
        purple = cv2.imread(Filepath_purple)

        res1 = cv2.matchTemplate(im_opencv, yellow, cv2.TM_CCOEFF_NORMED)  # 模板匹配
        threshold1 = 0.5
        loc1 = np.where(res1 >= threshold1)

        res2 = cv2.matchTemplate(im_opencv, purple, cv2.TM_CCOEFF_NORMED)  # 模板匹配
        threshold2 = 0.5
        loc2 = np.where(res2 >= threshold2)

        # print(loc)
        for pt in zip(*loc1[::-1]):
            flag[0] = -1
            now = time.time()
            if now - last_time < yellow_interval:
                break
            # print(flag[0])
            short_list[0] = 1
            last_time = now
            break

        for pt in zip(*loc2[::-1]):
            now = time.time()
            time.sleep(0.02)
            if now - last_time < purple_interval:
                break
            long_list[0] = 1
            last_time = now
            break

        #################################################################
        # cv2.imshow(num, im_opencv)  # 显示
        #
        # if (cv2.waitKey(1) & 0xFF) == ord('q'):  # 其实有无0xFF都可，加上防止返回值超过255，和‘1’的ascii码比较
        #     break
    #######################################################
    #####释放内存    
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)
    #####关闭all窗口
    cv2.destroyAllWindows()
    print("线程"+num+"已结束")


def SearchImage(_hwnd):
    list_char = []
    img_find_list = ["A", "S", "D", "J", "K", "L", ]
    hwndDC = win32gui.GetWindowDC(_hwnd)  # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)  # 根据窗口的DC获取mfcDC
    saveDC = mfcDC.CreateCompatibleDC()  # mfcDC创建可兼容的DC
    saveBitMap = win32ui.CreateBitmap()  # 创建bigmap准备保存图片

    left, top, right, bottom = win32gui.GetWindowRect(_hwnd)  # 获取窗口大小
    w = right - left
    h = bottom - top

    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)  # 为bitmap开辟空间
    saveDC.SelectObject(saveBitMap)  # 将截图存到saveBitMap中
    saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)  # 从左上角截取w,h范围的区域

    signedIntsArray = saveBitMap.GetBitmapBits(True)  # 提取数据成buffer
    im_opencv = np.frombuffer(signedIntsArray, dtype='uint8')  # 从deffer转numpy数组

    im_opencv.shape = (h, w, 4)  # 指定图像shape
    im_opencv = cv2.cvtColor(im_opencv, cv2.COLOR_BGRA2BGR)

    # cv2.imshow("123", im_opencv)
    # cv2.waitKey(0)
    for img_find in img_find_list:
        _timgFileName = img_find + ".png"  # home.png
        timgpath = "./resource/imagefind/" + _timgFileName  # ./resource/imagefind/home.png
        template = cv2.imread(timgpath)
        template_size = template.shape[:2]  # 尺寸:(高，宽)

        res = cv2.matchTemplate(im_opencv, template, cv2.TM_CCOEFF_NORMED)  # 模板匹配
        threshold = 0.90
        loc = np.where(res >= threshold)

        for pt in zip(*loc[::-1]):
            imgx = int(pt[0] + template_size[1] / 2)
            imgy = int(pt[1] + template_size[0] / 2)  # 返回图片中心供点击  原神上边界高20，需要减去
            list_char.append([imgx, imgy])
            print(imgx, imgy)
            break

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(_hwnd, hwndDC)

    return list_char


if __name__ == "__main__":
    window_capture()
