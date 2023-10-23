# -*- encoding=utf8 -*-
__author__ = "PC"

import json

from airtest.core.api import *
from airtest.core.settings import Settings as ST
import logging
from airtest.aircv import *
auto_setup(__file__)


logger = logging.getLogger("airtest")
logger.setLevel(logging.ERROR)
ST.OPDELAY= 0.3
# 720 1280  1080 1920
#0.66 0.66
niudan_banner_aren = (0, 570, 720, 918)
niudan_retry_aren = (0, 570, 724, 1280)
skip_aren = (528, 990, 720, 1280)
niudan_left_point = (674,778)
menu_point = (698,57)
menu_bottom = (698,1086)
niudan_banner_template = Template(r"tpl1696407721990.png", record_pos=(0.036, 0.183), resolution=(720, 1280))
#ST.THRESHOLD = 0.7
ST.CVSTRATEGY = ["tpl","sift"]
ST.FIND_TIMEOUT_TMP = 0
#卡池映射表
card_table = {"美妙姿势": Template(r"tpl1693394750722.png", resolution=(1080, 1920)) , "北部玄驹": Template(r"tpl1696407824860.png", resolution=(720, 1280))}

#=====================================用户配置=====================

reg_username = "shiroito"
target_count = 4
lottery_times = 1
target_card = []
def init_config():
    params = globals()
    config_path = params.get("config_path")
    if config_path is None:
        return
    json_config = {}
    with open(config_path, 'r', encoding='utf-8') as file:
        json_config = json.load(file)

    global reg_username
    global target_count
    global lottery_times
    global target_card
    reg_username = str(json_config["reg_username"])
    target_count = int(json_config["target_count"])
    target_card = json.loads(str(json_config["target_card"]).strip())
    lottery_times = int(json_config["lottery_times"])

def start_reflush():
    while True:
        touch((481,995))
        if(exists(Template(r"tpl1693374403682.png", record_pos=(0.423, 0.767), resolution=(1080, 1920)))):
            break
    touch((481,995))
    wait(Template(r"tpl1693374457979.png", record_pos=(-0.006, 0.007), resolution=(1080, 1920)), timeout = 100)
    sleep(1)
    touch(Template(r"tpl1693374470146.png", record_pos=(0.228, 0.266), resolution=(1080, 1920)))
    
def print_name():
    touch(Template(r"tpl1693374495496.png", threshold=0.95, record_pos=(0.099, -0.076), resolution=(1080, 1920)))
    text(reg_username)
    wait(Template(r"tpl1693375033942.png", record_pos=(-0.249, -0.091), resolution=(1080, 1920)))
    touch(Template(r"tpl1693375088130.png", record_pos=(0.367, 0.816), resolution=(1080, 1920)))
    wait(Template(r"tpl1693375180286.png", threshold=0.95, record_pos=(0.016, 0.272), resolution=(1080, 1920)))
    touch(Template(r"tpl1693375224837.png", record_pos=(-0.004, 0.267), resolution=(1080, 1920)))
    wait(Template(r"tpl1693375250502.png", threshold=0.95, record_pos=(0.225, 0.265), resolution=(1080, 1920)))
    sleep(1)
    touch(Template(r"tpl1693375261855.png", threshold=0.95, record_pos=(0.226, 0.268), resolution=(1080, 1920)))
    while True:
        
        if(exists(Template(r"tpl1693375353076.png", threshold=0.8, record_pos=(0.409, 0.8), resolution=(1080, 1920)))):
            try:
                touch(Template(r"tpl1693380624499.png", threshold=0.95, record_pos=(0.409, 0.79), resolution=(1080, 1920)))

            except Exception as e:
                print(e)
                
            continue
        if(exists(Template(r"tpl1693375427000.png", record_pos=(0.011, -0.799), resolution=(1080, 1920)))):
            break

def notice_close():
    sleep(0.5)
    touch(Template(r"tpl1694219399540.png", rgb=True, record_pos=(0.0, 0.752), resolution=(1080, 1920)))

    wait(Template(r"tpl1693370154060.png", record_pos=(0.003, -0.321), resolution=(1080, 1920)))
    sleep(0.5)
    touch(Template(r"tpl1694219399540.png", rgb=True, record_pos=(0.0, 0.752), resolution=(1080, 1920)))
    wait(Template(r"tpl1694219555334.png", record_pos=(-0.31, -0.566), resolution=(1080, 1920)))
    sleep(0.5)
    touch(Template(r"tpl1694219399540.png", rgb=True, record_pos=(0.0, 0.752), resolution=(1080, 1920)))

def gift_get():
    #wait(Template(r"tpl1693370226313.png", record_pos=(0.415, 0.37), resolution=(1080, 1920)))
    touch(Template(r"tpl1693370240204.png", threshold=0.85, record_pos=(0.412, 0.376), resolution=(1080, 1920)))
    wait(Template(r"tpl1693964537594.png", record_pos=(0.019, 0.635), resolution=(1080, 1920)))
    sleep(0.5)
    touch(Template(r"tpl1694394709078.png", record_pos=(0.22, 0.755), resolution=(1080, 1920)))

    wait(Template(r"tpl1693370295374.png", record_pos=(0.0, 0.644), resolution=(1080, 1920)))
    sleep(0.5)
    touch(Template(r"tpl1694394727921.png", record_pos=(0.004, 0.754), resolution=(1080, 1920)))
    wait(Template(r"tpl1694422812019.png", record_pos=(-0.002, -0.704), resolution=(1080, 1920)))
    sleep(0.5)
    touch(Template(r"tpl1694394727921.png", record_pos=(0.004, 0.754), resolution=(1080, 1920)))


def niudan():
    ssr_count = 0;
    touch(Template(r"tpl1693370515971.png", record_pos=(0.399, 0.806), resolution=(1080, 1920)))
    while True:
        sleep(1)
        full_screen = G.DEVICE.snapshot()
        search_aren = aircv.crop_image(full_screen, niudan_banner_aren)
        pos = niudan_banner_template.match_in(search_aren)
        if(pos is not None):
            break
        touch(niudan_left_point)
    sleep(0.5)
    touch(Template(r"tpl1693370582898.png", record_pos=(0.306, 0.504), resolution=(1080, 1920)))
    sleep(0.5)
    touch(Template(r"tpl1694394792754.png", record_pos=(0.219, 0.267), resolution=(1080, 1920)))

    for i in range(lottery_times):
        if i == 0:
            ssr_count = niudan_pick(ssr_count, True)
        else:
            ssr_count = niudan_pick(ssr_count)
            
    if ssr_count >= target_count and len(target_card) == 0:
        print("ssr的数目超过{}结束运行，获得ssr数目{}".format(target_count, ssr_count))
        return True
    print("此轮重生获得ssr数目{}".format(ssr_count))
    sleep(0.5)
    touch(Template(r"tpl1693371074647.png", record_pos=(-0.202, 0.777), resolution=(1080, 1920)))
    wait(Template(r"tpl1693371113140.png", threshold=0.75, record_pos=(0.001, 0.8), resolution=(1080, 1920)))
    sleep(1)
    touch(Template(r"tpl1693371113140.png", threshold=0.75, record_pos=(0.001, 0.8), resolution=(1080, 1920)))



def niudan_pick(ssr_count, isFirst = False):
    if not isFirst :
        touch(Template(r"tpl1693370859821.png", record_pos=(0.219, 0.776), resolution=(1080, 1920)))
        sleep(1)
        touch(Template(r"tpl1693370883389.png", record_pos=(0.204, 0.27), resolution=(1080, 1920)))
    sleep(1)
    while True:
        full_screen = G.DEVICE.snapshot()
        search_aren = aircv.crop_image(full_screen, skip_aren)
        pos = Template(r"tpl1693964732005.png").match_in(search_aren)

        if(pos is not None):
            touch((pos[0]+skip_aren[0], pos[1] + skip_aren[1]))
            continue
        
        full_screen = G.DEVICE.snapshot()
        search_aren = aircv.crop_image(full_screen, niudan_retry_aren)
        pos = Template(r"tpl1693370840928.png").match_in(search_aren)
        if(pos is not None):
            break
    sleep(0.5)
    size = find_all(Template(r"tpl1694442424737.png", threshold=0.62, resolution=(720, 1280)))
    
    if size is not None:
        ssr_count = ssr_count + len(size)
        target_card_remove()
    return ssr_count

def target_card_remove():
    global target_card
    if len(target_card) == 0:
        return
    while True:
        for i in range(len(target_card)):
            template = card_table.get(target_card[i])
            if template is not None:
                if exists(template):
                    target_card.remove(target_card[i])
                    break
        break

def delete_data():
    try:
    
        wait(Template(r"tpl1693378114026.png", record_pos=(0.408, 0.102), resolution=(1080, 1920)))
    
    except Exception as e:
        touch(Template(r"tpl1693371113140.png", threshold=0.9, record_pos=(0.001, 0.8), resolution=(1080, 1920)))
        wait(Template(r"tpl1693378114026.png", record_pos=(0.408, 0.102), resolution=(1080, 1920)))

    while True:
        touch(menu_point)
        #touch((1125,241))
        sleep(1)
        if(exists(Template(r"tpl1693398849078.png", record_pos=(0.225, -0.295), resolution=(1152, 2376)))):
            break
    touch(Template(r"tpl1693398877776.png", record_pos=(0.232, -0.297), resolution=(1152, 2376)))

    wait(Template(r"tpl1693373323297.png", record_pos=(0.01, -0.711), resolution=(1080, 1920)))
    while True:
        touch(menu_bottom)
        #touch((1112,1967))
        if(exists(Template(r"tpl1694520019315.png", threshold=0.75, rgb=True, resolution=(720, 1280)))):
            break
    
    while True:
        
        touch(Template(r"tpl1694520019315.png", threshold=0.75, rgb=True, resolution=(720, 1280)))
        sleep(1)
        wait(Template(r"tpl1693374216164.png", threshold=0.7, rgb=True, record_pos=(0.225, 0.269), resolution=(1080, 1920)))
        sleep(1)
        touch(Template(r"tpl1693374228585.png", threshold=0.7, rgb=True, record_pos=(0.224, 0.269), resolution=(1080, 1920)))
        wait(Template(r"tpl1693374241180.png", threshold=0.7, rgb=True, record_pos=(0.002, -0.323), resolution=(1080, 1920)))
        sleep(1)
        touch(Template(r"tpl1693374257944.png", rgb=True, record_pos=(0.222, 0.267), resolution=(1080, 1920)))
        wait(Template(r"tpl1694521242898.png", record_pos=(-0.01, -0.318), resolution=(720, 1280)))
        sleep(1)
        touch(Template(r"tpl1693374280809.png", threshold=0.85, rgb=True, record_pos=(-0.001, 0.265), resolution=(1080, 1920)))
        sleep(1)
        if(not exists(Template(r"tpl1694519362731.png", threshold=0.8, rgb=True, target_pos=2, record_pos=(0.0, 0.689), resolution=(720, 1280)))):
            break
    

def main_d():
    while True:
        delete_data()
        start_reflush()
        try:
            print_name()
        except Exception as e:
            print_name()
        notice_close()
        gift_get()
        result = niudan()
        if result:
            return
        
def main_p():
    while True:
        try:
            print_name()
        except Exception as e:
            print_name()
        notice_close()
        gift_get()
        result = niudan()
        if result:
            return
        delete_data()
        start_reflush()


def do_task():
    if exists(Template(r"tpl1693378114026.png", record_pos=(0.408, 0.102), resolution=(1080, 1920))):
        main_d()
        return
    elif exists(Template(r"tpl1693374495496.png", threshold=0.95, record_pos=(0.099, -0.076), resolution=(1080, 1920))):
        main_p()
        return

init_config()
do_task()







