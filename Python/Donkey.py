# -*- coding: UTF-8 -*-

import os
import time
import random
import pytest
import threading
import numpy as np
from time import sleep
from appium import webdriver
import matplotlib.pyplot as plt
from selenium.webdriver.support.ui import WebDriverWait
from appium.webdriver.common.touch_action import TouchAction

'''
@author xinzhen


基于appium制造iOS端，类Monkey工具：Donkey。

优点：

①基于appium，实现方便。
②结合pytest，轻松实现多机并发。
③屏蔽状态栏不可点击区域。

缺点：

①基于appium，速度上不如略逊于Monkey。

'''


@pytest.mark.parametrize("device_name, udid, wdalocal_port, appium",
                         [
                             ("测试机iPhone X", "a1bef8664467b9146b9bc7b511049d951dcce327", 5680, '4766'),

                             # ("测试机iPhone6S", "4a7fe6672c148956640cfdaff70da48e49f6945c", 5682, '4766'),

                             # ("测试机iPhone5s", "ed50fe2a082cd8ea8d1ee7bb11ccc017250da180", 5680, '4766'),


                         ])
def test_donkey(device_name, udid, wdalocal_port, appium):

    capabilities = {

                    'platformName': 'iOS',
                    'platformVersion': "12.1",
                    'deviceName': device_name,
                    'bundleId': 'com.tent',
                    'udid': udid,
                    'wdaLocalPort': wdalocal_port,
                    'automationName': 'appium',
                    # 'unicodeKeyboard': True,
                    'noReset': True

                }

    url = 'http://localhost:' + appium + '/wd/hub'

    global driver
    driver = webdriver.Remote(url, capabilities)
    driver.implicitly_wait(5)

    global w
    w = driver.get_window_size()['width']
    global h
    h = driver.get_window_size()['height']
    print("屏幕宽：%s" % w)
    print("屏幕高：%s \n" % h)

    '''
        在此设置事件比例：
            
            滑动：35%
            点击：55%
            防止遍历过深：5%
            长按触发3D-touch: 2%
            点击页面独立返回按钮：2%
            
            定时timer守护Donkey进程，如果Donkey跳出app后，可再次回到app（如果app崩溃了，则可重新启动app）。   
            
        update：
        
        2019.1.9
        
        ①限制守护进程执行次数。
        
        ②优化输出结果。
        
        2019.1.10
        
        ①尝试另外一种事件分配方法：以滑动事件为核心，一个滑动事件后伴随着其他事件。
        
    '''

    events_num = 100000  # 在此设置事件数
    events_space = 0.3  # 事件间隔时间，单位是s

    # 初始化计数
    click_num = 0
    swipe_num = 0
    fix_deep_num = 0
    back_num = 0
    long_press_num = 0
    defend_num = 0

    start_time = time.time()  # Donkey 开始表演

    for i in range(events_num):

        percent = random.randint(1, 100)

        try:
            if 65 <= percent <= 100:
                random_swipe()
                swipe_num = swipe_num + 1
                print("🚀 第 %s 次执行 swipe 成功！\n" % (i + 1))

            elif 10 <= percent < 65:
                random_click()
                click_num = click_num + 1
                print("🚀 第 %s 次执行 click 成功！\n" % (i + 1))

            elif 5 <= percent < 10:
                fix_deep_path()
                fix_deep_num = fix_deep_num + 1
                print("🚀 第 %s 次执行 fix_deep_path 成功！\n" % (i + 1))

            elif percent == 4 or percent == 3:
                back()
                back_num = back_num + 1
                print("🚀 第 %s 次执行 back 成功！\n" % (i + 1))

            else:
                random_long_press()
                long_press_num = long_press_num + 1
                print("🚀 第 %s 次执行 long_press 成功！\n" % (i+1))

            sleep(events_space)  # 事件之间的间隔事件

            '''
            每循环5次执行一次守护进程。
            '''
            if i != 0 and (i % 20) == 0:
                timer = threading.Timer(1, defend_thread)  # 1s 后启动守护进程，设置等待时间越大，可成功执行守护进程越少
                timer.start()
                defend_num = defend_num + 1
            else:
                pass

        except Exception as e:
            print("💣 第 %s 次执行Event失败! \n%s" % ((i+1), e))

    print("\n✨【Events】总执行时间为: %s s" % int(time.time() - start_time))
    print("\n✨swipe 执行: %s 次" % swipe_num)
    print("\n✨click 执行: %s 次" % click_num)
    print("\n✨fix_deep_path 执行: %s 次" % fix_deep_num)
    print("\n✨back 执行: %s 次" % back_num)
    print("\n✨long_press 执行: %s 次" % long_press_num)
    print("\n⚔ 守护进程执行: %s 次" % defend_num)


def random_swipe():

        random_num = random.randint(1, 100)
        random_w_1 = random.randint(1, w)
        random_h_1 = random.randint(1, h)
        random_w_2 = random.randint(1, w)
        random_h_2 = random.randint(1, h)

        '''
            滑动事件占比：

                向上滑动：40%
                向下滑动：20%
                向右滑动：20%
                向左滑动：10%
                随机滑动：10%


                update：

                2019.1.9  

                ①优化拖动范围，屏蔽顶部状态栏不可拖动区域：

                随机拖动的h坐标+20，用于屏蔽h轴0-20区域，以h-20为界，<=h-20可直接点击，<h-20<也可直接点击，超出h则不做任何操作。
        '''

        if random_num < 100:

            random_sw = random.randint(1, 10)

            # 滑动事件：随机滑动占比0.1，向shang滑动占比0.4，向xia滑动占比0.2，向右滑动占比0.2，向左滑动占比0.1
            if random_sw == 10:

                if 0 < random_h_1 + 25 <= h - 25 and 0 < random_h_2 + 25 <= h - 25:

                    driver.swipe(random_w_1, random_h_1 + 25, random_w_2, random_h_2 + 25, 200)  # 随机滑动

                elif random_h_1 + 25 < h and random_h_2 + 25 < h:

                    driver.swipe(random_w_1, random_h_1 + 25, random_w_2, random_h_2 + 25, 200)  # 随机滑动
                else:
                    pass

            elif 5 <= random_sw < 10:
                driver.swipe(w * 0.5, h * 0.8, w * 0.5, h * 0.2, 300)

            elif 4 <= random_sw < 5:
                driver.swipe(w * 0.5, h * 0.4, w * 0.5, h * 0.8, 300)

            elif random_sw == 2 or random_sw == 3:
                driver.swipe(w * 0.1, h * 0.5, w * 0.8, h * 0.5, 300)

            else:
                driver.swipe(w * 0.8, h * 0.5, w * 0.1, h * 0.5, 300)
        else:

            driver.swipe(w * 0.2, h * 0.5, w * 0.8, h * 0.5, 300)


def random_click():

        random_num = random.randint(1, 100)
        random_w = random.randint(1, w)
        random_h = random.randint(1, h)
        random_key = random.randint(h - 25, h)

        '''
            update：

            2019.1.9  
            
            ①优化点击范围，屏蔽顶部状态栏不可点击区域：

            随机点击的h坐标+25，用于屏蔽h轴0-25区域，以h-25为界，<=h-25可直接点击，<h-25<也可直接点击，超出h则不做任何操作。
            
            ②增加重点点击区域：
            
            屏幕底部区域设置为重点点击区域，重点区域大小可根据情况设置 random_key 。
            
            ③增加重点区域点击比例

        '''

        if 30 <= random_num <= 100:

            if 0 < random_h + 25 <= h - 25:

                driver.tap([(random_w, random_h + 25)])

            elif h - 25 < random_h + 25 < h:

                driver.tap([(random_w, random_h + 25)])

            else:
                pass

        elif 1 < random_num < 30:  # 重点点击区域，占比30%

            driver.tap([(random_w, random_key)])
        else:
            driver.swipe(w * 0.2, h * 0.5, w * 0.8, h * 0.5, 300)


def random_long_press():

        random_num = random.randint(1, 100)
        random_w = random.randint(1, w)
        random_h = random.randint(1, h)

        '''
            update：

            2019.1.9  

            优化长按范围，屏蔽顶部状态栏不可长按区域：

            随机长按的h坐标+25，用于屏蔽h轴0-25区域，以h-25为界，<=h-25可直接点击，<h-25<也可直接点击，超出h则不做任何操作。

        '''

        if random_num < 100:

                if 0 < random_h + 25 <= h - 25:

                    TouchAction(driver).long_press(x=random_w, y=random_h, duration=2000).perform()

                elif h - 25 < random_h + 25 < h:

                    TouchAction(driver).long_press(x=random_w, y=random_h, duration=2000).perform()
                else:
                    pass

        else:
            driver.swipe(w * 0.2, h * 0.5, w * 0.8, h * 0.5, 300)


def fix_deep_path():

        for i in range(3):
            driver.swipe(w * 0.2, h * 0.5, w * 0.8, h * 0.5, 300)
            sleep(1)


def back():

        '''
        用途：

        避免长时间在一个特殊页面出不来。此处可根据APP情况设定。

        '''

        try:
            driver.find_element_by_ios_predicate('name="toolbar back"').click()  # 左下角返回
            # driver.swipe(w*0.1, h*0.9, w*0.1, h*0.9, 500)  # 左下角返回
        except:
            pass

        try:
            driver.find_element_by_ios_predicate('name="toolbar_back"').click()  # 左上角返回
        except:
            pass

        try:
            driver.find_element_by_ios_predicate('name="icon menu guanbi"').click()  # 广告左上角返回
        except:
            pass

        # try:
        #     # driver.find_element_by_xpath('//*[@type="XCUIElementTypeButton"]').click()  # 解决未登录状态下，关闭登录弹窗
        #     driver.find_element_by_ios_predicate("type == 'XCUIElementTypeButton'").click()
        # except:
        #     pass


def defend_thread():

        try:
            driver.activate_app('com.huxiu')  # 调起后台app，或者当app崩溃时会启动app
            print("\n   【Donkey】守卫进程启动成功... \n")

        except :
            print("\n   【☠️Donkey】守卫进程启动失败... \n")


