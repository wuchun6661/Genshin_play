# Genshin_play

## 简介

原神AI全自动打鼓（python实现）

目前仅支持分辨率1440x900

不管哪种启动，都可以通过按“q”结束

## 下载
#### 1、直接下载
https://github.com/wuchun6661/Genshin_play/archive/refs/heads/master.zip
#### 2、git clone下载（新手勿试）
git clone https://github.com/wuchun6661/Genshin_play.git

## 运行

#### 1、直接启动（不依赖代码环境）

**注意：最起码需要保证main.exe和resource文件夹在同级目录下！！！！**

①启动原神，调节原神分辨率到1440x900

②右键main.exe，以管理员身份启动

③按“q”结束程序

#### 2、通过源码启动（新手不推荐）

①启动原神，调节原神分辨率到1440x900

②安装依赖项（pip install xxx）

③以管理员身份启动main.py

④按“q”结束程序

## 可能出现的问题

#### 1、通过代码运行不成功，各种报错

答：建议新手通过第一种方式启动，这样不依赖任何python环境，甚至不需要装python

2、能运行，但是不敲击

答：检查是否以管理员身份启动，检查是否调节原神分辨率至1440x900

3、能敲击，但成功率不是100%

答：本代码是通过监控屏幕，然后模板匹配的方法进行识别并按下按键，若电脑性能不佳，可能会导致卡顿致使识别率不高，可以通过换一台性能更好的电脑解决此问题

4、电脑性能已经足够高了，弹大佬谱还是不能100%

答：经本人测试，本代码在官方的谱子上均能100%完成，在网友上传的谱子上普遍能100%，但在极其苛刻的大佬谱上，可能存在漏检。本人时间有限，如有需要，可根据代码自行优化。

