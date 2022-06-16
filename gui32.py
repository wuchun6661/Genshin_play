# -*- coding=utf-8 -*-
"""
作者：55450
日期：2022年06月13日
时间：16：57：03
"""
import time
import cv2
import numpy as np
import win32api
import win32con
import win32gui
import win32ui

PIC_CAP_FORMAT = '.jpg'
PIC_SELECT_FORMAT = '.png'


class My_gui32:

    def __init__(self):

        self._hwndMain = -1  # 主窗口
        self.imgx = -1
        self.imgy = -1
        self.timeBegin = time.time()
        self.timeEnd = time.time()

        self.get_YuanShen_Hwnd()


    # 等待图片消失
    def ImgWait(self, _Tname, _Mname):
        while True:
            # 截图
            self.CaptureOne(_Mname)
            if self.SearchImage(_Tname, _Mname) == False:
                time.sleep(1.0)
                return

            print("waiting page finished .... sleep 1.0s >> ")
            time.sleep(1.0)

    def getPicPath(self):
        return './resource/image/'

    def getFindPath(self):
        return './resource/imagefind/'

    # 查找一个图，返回位置  isCap决定是否再截个图
    def SearchImage(self, _timgFileName, _mainImgFileName, isCap=False):

        if isCap == True:
            self.CaptureOne(_mainImgFileName)

        _timgFileName = _timgFileName + PIC_SELECT_FORMAT  # home.png
        _mainImgFileName = _mainImgFileName + PIC_CAP_FORMAT  # tmp.jpg

        timgpath = self.getFindPath() + _timgFileName  # ./resource/imagefind/home.png
        template = cv2.imread(timgpath)

        # template = cv2.resize(template, (0, 0), fx=scale, fy=scale)
        template_size = template.shape[:2]  # 尺寸:(高，宽)

        mFilePathName = self.getPicPath() + _mainImgFileName  # ./resource/image/tmp.jpg
        img = cv2.imread(mFilePathName)
        cv2.imshow("img", img)
        cv2.waitKey(1)

        res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)  # 模板匹配
        threshold = 0.60
        loc = np.where(res >= threshold)

        for pt in zip(*loc[::-1]):
            self.imgx = int(pt[0] + template_size[1] / 2)
            self.imgy = int(pt[1] + template_size[0] / 2) - 20  # 返回图片中心供点击  原神上边界高20，需要减去
            if self.imgx > 10 and self.imgy > 10:
                print(self.imgx, self.imgy)
                return True
        return False

    # 鼠标不点击，最后换实现方法
    def WinLeftClick(self, _hwnd, _x, _y):
        client_pos = win32gui.ClientToScreen(_hwnd, (_x, _y))  # 将客户端的相对位置，转换成屏幕位置
        print(client_pos)
        win32api.SetCursorPos([client_pos[0], client_pos[1]])
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        time.sleep(0.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

    # 右
    def winRightClick(self, _hwnd, _x, _y):
        client_pos = win32gui.ClientToScreen(_hwnd, (_x, _y))
        win32api.SetCursorPos([client_pos[0], client_pos[1]])
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
        time.sleep(0.5)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)

    # 搜索图片，并窗口点击
    def ImgLeftClick(self, _Tname, _Mname, _Iscap=True):

        if _Iscap == True:
            self.CaptureOne(_Mname)

        if self.SearchImage(_Tname, _Mname) == True:
            # client_pos = [self.imgx, self.imgy]
            self.WinLeftClick(self._hwndMain, self.imgx, self.imgy)
            return True
        return False

    def CaptureOne(self, _filename, _hwnd=0):

        try:
            self.CaptureOneNotry(_filename, _hwnd)
        except:
            print('截图出错！')

    # 抓图一个
    def CaptureOneNotry(self, _filename, _hwnd=0):
        # _hwnd=0 为桌面窗口

        time.sleep(0.5)

        _filename = _filename + PIC_CAP_FORMAT  # temp.jpg

        if _hwnd == 0:
            _hwnd = self._hwndMain  # 逍遥模拟器的句柄传递给_hwnd

        # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
        hwndDC = win32gui.GetWindowDC(_hwnd)
        # 根据窗口的DC获取mfcDC
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        # mfcDC创建可兼容的DC
        saveDC = mfcDC.CreateCompatibleDC()
        # 创建bigmap准备保存图片
        saveBitMap = win32ui.CreateBitmap()

        # 获取窗口大小
        left, top, right, bottom = win32gui.GetWindowRect(_hwnd)
        w = right - left
        h = bottom - top

        # 为bitmap开辟空间
        saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)  # w,h可以改
        # 高度saveDC，将截图保存到saveBitmap中
        saveDC.SelectObject(saveBitMap)  # 将截图存到saveBitMap中
        # 截取从左上角（0，0）长宽为（w，h）的图片
        saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)  # 从左上角截取w,h范围的区域

        saveBitMap.SaveBitmapFile(saveDC, self.getPicPath() + _filename)  # ./resource/image/tmp.jpg

        signedIntsArray = saveBitMap.GetBitmapBits(True)  # 提取数据成buffer
        im_opencv = np.frombuffer(signedIntsArray, dtype = 'uint8')  # 从deffer转numpy数组
        im_opencv.shape = (h, w, 4)

        # cv2.imshow("im_opencv", im_opencv)  # 显示
        # if (cv2.waitKey(1) & 0xFF) == ord('1'):  # 其实有无0xFF都可，加上防止返回值超过255，和‘1’的ascii码比较
        #     break

    # 得到原神窗口句柄 title = 原神
    def get_YuanShen_Hwnd(self):

        self._hwndMain = -1
        Thwnd = -1
        hwndList = self.get_child_windows(0)
        for hwnd in hwndList:
            try:
                className = win32gui.GetClassName(hwnd)
                title = win32gui.GetWindowText(hwnd)
                # print(className, title)
                if className == 'UnityWndClass':
                    if title == '原神':
                        print(hwnd, className, title)
                        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
                        h = bottom - top
                        if h > 400:
                            # print(title)
                            Thwnd = hwnd
                            break
            except:
                pass

        if Thwnd != -1:
            left, top, right, bottom = win32gui.GetWindowRect(Thwnd)
            print('发现安卓窗口，hwnd:', Thwnd, ' 窗口：', str(left) + " " +
                  str(top) + " " + str(right) + " " + str(bottom) + ' w= ' + str(right - left)
                  + " h= " + str(bottom - top))
            self._hwndMain = Thwnd
            # self.get_child_windows(self._hwndMain)
            # print(self.get_child_windows(self._hwndMain),666)
        else:
            print("未发现原神窗口")

    def get_child_windows(self, parent):
        '''
        获得parent的所有子窗口句柄
        返回子窗口句柄列表
        '''
        # if not parent:
        #    return
        hwndChildList = []
        win32gui.EnumChildWindows(parent, lambda hwnd, param: param.append(hwnd), hwndChildList)
        return hwndChildList

    @property
    # 将方法变成属性来调用
    def hwndMain(self):
        return self._hwndMain
