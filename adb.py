# -- coding: utf-8 --

import os
from time import sleep

import cv2

adb_path = r'C:\tool\platform-tools\adb.exe'


def image_to_position(screen, template):
    image_x, image_y = template.shape[:2]
    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    print("prob:", max_val)
    if max_val > 0.98:
        global center
        center = (max_loc[0] + image_y / 2, max_loc[1] + image_x / 2)
        return center
    else:
        return False


def connect_adb():
    os.system(f"{adb_path} connect 127.0.0.1:21503")
    os.system(f"{adb_path} root")


def screenshot():
    os.system(f"{adb_path} shell screencap -p /data/screenshot.png")
    os.system(f"{adb_path} pull /data/screenshot.png asset\\tmp.png")


def adb_click(center, offset=(0, 0)):
    (x, y) = center
    x += offset[0]
    y += offset[1]
    os.system(f"{adb_path} shell input tap {x} {y}")


def find_button_and_click(img):
    position = find_button(img)
    if position:
        print(f'click {img}')
        adb_click(position)
        sleep(1)
        return True
    else:
        print(f'{img} not find')
        return False


def find_button(img):
    screenshot()
    screen = cv2.imread('asset/tmp.png')
    template = cv2.imread(f'asset/{img}')
    return image_to_position(screen, template)


def await_task_over():
    while 1:
        # 检测体力恢复
        find_button_and_click('power_max.png')
        # 检测任务结束
        if find_button_and_click('task_over.jpg'):
            break
        sleep(10)


if __name__ == "__main__":
    connect_adb()
    i = 0
    while i < 6:
        find_button_and_click('task_home.jpg')
        # 判断是否无体力
        # if find_button('no_tili.png'):
        if find_button('no_power_shiji.jpg'):
            # find_button_and_click('by_tili_for_yuanshi.png') #是否碎石
            sleep(1)
            find_button_and_click('by_tili.png')
            sleep(1)
            find_button_and_click('task_home.jpg')

        sleep(3)
        find_button_and_click('task_start.jpg')

        await_task_over()
        find_button_and_click('power_max.png')
        sleep(10)
        i += 1
        print(f'第{i}次执行任务')

# if __name__ == '__main__':
#     # connect_adb()
#     # screenshot()
#     find_button_and_click('task_home.jpg')
