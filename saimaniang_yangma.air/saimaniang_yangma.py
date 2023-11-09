# -*- encoding=utf8 -*-
__author__ = "PC"

import json

import numpy as np
from airtest.core.api import *
from airtest.core.settings import Settings as ST
import logging
from airtest.aircv import *
from cnocr import CnOcr

auto_setup(__file__)

logging.disable(level=logging.ERROR)

ST.CVSTRATEGY = ["tpl","sift"]
ST.OPDELAY= 0.3
ST.FIND_TIMEOUT_TMP = 0
#文本识别工具
en_ocr = CnOcr(rec_model_name = "en_PP-OCRv3", rec_root="./ocr-models", rec_model_backend='pytorch',
               det_root="./cnstd-models", det_more_configs={'rotated_bbox': False}, cand_alphabet="0123456789+")
cn_ocr = CnOcr(rec_model_name="densenet_lite_136-gru", rec_model_backend='pytorch', rec_root="./ocr-models",
                det_model_name="db_shufflenet_v2",det_root="./cnstd-models", det_more_configs={'rotated_bbox': False})
#当前使用闹钟
c_clock = 0
#当前回合
c_round = 0
#是否结束
is_end = False
#是否已经修改过跑法
running_is_edit = False
#外出是否需要双重确认
go_out_recheck = False
#当前技能阈
c_skill_limit = 250
#是否养成剧情结束
#story_is_end = False
task_area_point = (0, 898, 720, 1175)
top_area_point = (0, 0, 720, 317)
center_area_point = (0, 317, 720, 985)
bottom_area_poin = (0, 904, 720, 1280)
#属性位置
speed_area_point = (68, 855, 132, 880)
endurance_area_point = (185, 855, 250, 880)
power_area_point = (295, 855, 360, 880)
perseverance_area_point = (412, 855, 474, 880)
intelligence_area_point = (520, 855, 585, 880)
#主页标志识别区域
home_mark_area_point = (550, 670, 720, 900)
#事件标签位置
event_title_area_point = (107, 233, 547, 285)
#技能位置
skill_point = (600, 855, 690, 895)
#技能学习界面点数位置
skill_point2 = (500, 400, 680, 440)
#心情位置
mood_point = (574, 142, 670, 180)
#友情头像区域
friendship_area_point = (508, 165, 720, 765)
#训练属性位置
train_speed_area_point = (13, 888, 178, 1188)
train_endurance_area_point = (178, 888, 297, 1188)
train_power_area_point = (297, 888, 429, 1188)
train_perseverance_area_point = (429, 888, 561, 1188)
train_intelligence_area_point = (561, 888, 693, 1188)
#误识别文本修复
ocr_fix_table = {"(康丽莎电女树":"伊丽莎白女王杯"}
#=====================================用户配置=====================
#技能字典
skill_table = ["蓝玫瑰猎人", "汝等,瞻仰皇帝的神威吧", "直线能手", 
               "最后冲刺", "登山家","弯道加速","曲线行家","领跑弯道", 
               "领跑直线", "弯道能手", "雨天", "路况不佳", "京都赛道", 
               "钉牢后方", "对抗意识", "为了完成高贵的使命", "顺时针", 
               "逆时针", "共鸣", "束缚", "场地良", "非标准距离"]
#角色使用的战术 0 = 后追, 1 = 居中，2 = 前跟，3 - 领跑
running = 3
#回合策略 -1 = 获取友情为主, -2 = 根据训练策略为主, -3 = 剧情比赛, -4 = 夏日集训,  比赛名称为自定义比赛
round_strategies = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -3,
                    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
                   -2, -2, "女王杯", -2 , -3, -2, -3, -2, -2, -3, -2, -2,
                   -4, -4, -4, -4, -2, -2, -2, -3, -3, -2, -2, -2,
                   -2, -2, -2, -2, -2, -3, -2, -2, -2, -2, -2, -2,
                   -4, -4, -4, -4, -2, -2, -2, -3, -2, -2, -2, -3,
                   -2, -3, -2, -3, -2, -3]
#事件选择列表*号开头为体力选项需要判断是否体力溢出
event_list = ["*2-追加的自主训练"]
#最多允许闹钟使用数目
max_clock = 1
#技能学习步长
skill_limit_step = 80
#技能点大于此值学习技能-初始值
skill_limit = 250
skill_end_mark = 150
#训练方向 速 耐 力 毅 智
strategy = [1, 0.75, 0, 0, 0]
#其实回合
start_round = 0
#是否使用体力药水
is_charge = 0
#持有闹钟数
total_clock = 1
#养成次数
cultivate_times = 1
#支援卡位置
support_name = "Reina"
def init_config():
    params = globals()
    config_path = params.get("config_path")
    if config_path is None:
        return
    json_config = {}
    with open(config_path, 'r', encoding='utf-8') as file:
        json_config = json.load(file)

    global max_clock
    global skill_limit
    global c_skill_limit
    global skill_end_mark
    global running
    global start_round
    global round_strategies
    global skill_table
    global strategy
    global is_charge
    global total_clock
    global cultivate_times
    global support_name
    global event_list
    max_clock = int(json_config["clock_times"])
    skill_limit = int(json_config["skill_start_limit"])
    c_skill_limit = skill_limit
    skill_end_mark = int(json_config["skill_stop_limit"])
    running = int(json_config["running"])
    start_round = int(json_config["start_round"])
    strategy = json.loads(str(json_config["strategy"]).strip())
    round_strategies = json.loads(str(json_config["schedule"]).strip())
    skill_table = json.loads(str(json_config["skill_list"]).strip())
    is_charge = int(json_config["is_charge"])
    total_clock = int(json_config["total_clock"])
    support_name = str(json_config["support_name"])
    cultivate_times = int(json_config["cultivate_times"])
    event_list = json.loads(str(json_config["event_list"]).strip())
    
def do_task():
    #检测页面
    if is_in_home():
        for i in range(cultivate_times):
            start_cultivate(start_round)
            cultivate_global_init()
            if i == (cultivate_times - 1):
                return
            res = pre_cultivate()
            if not res:
                return          
    else:
        for i in range(cultivate_times):
            res = pre_cultivate()
            if not res:
                return
            start_cultivate(0)
            cultivate_global_init()

def pre_cultivate():

    while True:
        next_p = exists(Template(r"tpl1695803925584.png", record_pos=(0.257, 0.646), resolution=(720, 1280)))
        if next_p:
            touch(next_p)
            sleep(1)
        next_p = exists(Template(r"tpl1695803969756.png", record_pos=(0.003, 0.607), resolution=(720, 1280)))
        if next_p:
            touch(next_p)
            sleep(1)
        if exists(Template(r"tpl1697557884999.png", threshold=0.95, record_pos=(0.361, 0.608), resolution=(720, 1280))):
            sleep(1)
            break
    next_p = exists(Template(r"tpl1695805922498.png", threshold=0.9, record_pos=(0.294, 0.057), resolution=(720, 1280)))
    if next_p:
        sleep(1)
        touch(next_p)
        wait(Template(r"tpl1695804741013.png", record_pos=(-0.003, -0.79), resolution=(720, 1280)))
        support_pos = find_support(support_name)
        touch(support_pos)
        sleep(1)
    
    while True:
        next_p = exists(Template(r"tpl1695812451877.png", record_pos=(0.065, 0.606), resolution=(720, 1280)))
        
        if next_p:
            try:
                touch(next_p)
            except Exception as e:
                continue
            sleep(1.5)
        
        next_p = exists(Template(r"tpl1695815097712.png", threshold=0.85, record_pos=(0.219, 0.267), resolution=(720, 1280)))
        if next_p:
            if is_charge == 0:
                return False
            else:
                try:
                    touch(next_p)
                    next_p = wait(Template(r"tpl1695815505184.png", record_pos=(-0.376, -0.44), resolution=(720, 1280)))
                except Exception as e:
                    continue
                    
                sleep(1.5)
                touch((next_p[0] + 500, next_p[1]))
                next_p = wait(Template(r"tpl1695815600247.png", record_pos=(0.219, 0.385), resolution=(720, 1280)))
                sleep(1)
                touch(next_p)
                next_p = wait(Template(r"tpl1695815654922.png", record_pos=(0.001, 0.269), resolution=(720, 1280)))
                sleep(1)
                touch(next_p) 
        if exists(Template(r"tpl1693915070619.png", record_pos=(0.409, 0.795), resolution=(1080, 1920))):
            return True
    
    
    
#开始培育
def start_cultivate(start_r):
    init_skip()
    global c_round
    
    for i in range(len(round_strategies)):
        if i < start_r:
            c_round = i + 1
            continue
        status = get_status()
        run_round(status[0], status[1], status[2], status[3], status[4], status[5])
        c_round = c_round + 1
        if is_end:
            break
    end_strategy()
       
    
def init_skip():
    while True:
        
        next_p = exists(Template(r"tpl1693915070619.png", threshold=0.85, record_pos=(0.409, 0.795), resolution=(1080, 1920)))
        if next_p:
            
            touch(next_p)
            sleep(1)
        
        if exists(Template(r"tpl1693915147663.png", threshold=0.9, record_pos=(-0.001, -0.432), resolution=(1080, 1920))):
            sleep(1)
            touch(Template(r"tpl1693915185150.png", record_pos=(-0.103, -0.018), resolution=(1080, 1920)))
            touch(Template(r"tpl1693915218427.png", record_pos=(0.002, 0.383), resolution=(1080, 1920)))
            
        if not exists(Template(r"tpl1695816751831.png", threshold=0.9, record_pos=(-0.146, 0.844), resolution=(720, 1280))):
            
            try:
                next_p = exists(Template(r"tpl1693915266857.png", record_pos=(-0.142, 0.844), resolution=(1080, 1920)))
                if next_p:
                    sleep(1)
                    touch(next_p)

                next_p = exists(Template(r"tpl1693915367114.png", threshold=0.9, record_pos=(-0.141, 0.845), resolution=(1080, 1920)))
                if next_p:
                    sleep(1)
                    touch(next_p)
                    
            except Exception as e:
                continue        
                
        else:
            if is_in_home():
                return
    


def get_status():
    full_screen = G.DEVICE.snapshot()
    top_area = get_top_screen(full_screen)
    task_area = get_task_screen(full_screen)
    while True:
        if is_in_home(full_screen):
            sleep(0.5)
            is_in_home()
            break

        full_screen = G.DEVICE.snapshot()
        top_area = get_top_screen(full_screen)
        task_area = get_task_screen(full_screen)
    
    
    #判断页面 0-普通页面 1-剧情比赛页面
    page_type = 0
    if Template(r"tpl1694613824100.png").match_in(task_area) is not None:
        page_type = 1    
    
        
    action = get_action(top_area)
    mood = get_mood(mood_point)
    health = get_health(task_area, page_type)
    attribute = get_attribute(full_screen, page_type)
    skill = get_skill(full_screen, page_type)
    score_coefficient = get_score_coefficient(attribute)
    logging.critical("===========================================================================================================================")
    logging.critical("当前回合：{}".format(c_round))
    logging.critical("当前体力为：{}".format(action))
    logging.critical("当前心情为：{}".format(mood))
    logging.critical("当前健康状态为：{}".format(health))
    logging.critical("当前技能点数为：{}".format(skill))
    logging.critical("当前属性：速度：{}, 耐力：{}, 力量：{}, 毅力：{}, 智力：{}".format(attribute[0], attribute[1], attribute[2], attribute[3], attribute[4]))
    logging.critical("训练得分：速度：{}, 耐力：{}, 力量：{}, 毅力：{}, 智力：{}".format(round(score_coefficient[0], 2), round(score_coefficient[1], 2), round(score_coefficient[2], 2), round(score_coefficient[3], 2), round(score_coefficient[4], 2)))
    logging.critical("===========================================================================================================================")
    return [action, mood, health, attribute, skill, page_type]


def run_round(action, mood, health, attribute, skill, page_type):
    
    if skill >= c_skill_limit:
        study_skill(page_type)
    #出战翻车补偿
    if c_round > 11 and c_round < 20:
        top_screen = get_top_screen()
        retry =Template(r"tpl1695992411168.png", threshold=0.9).match_in(top_screen)
        if retry is not None:
            if c_round % 2 != 0:
                custom_match("初级")
                select_after(5)
                return
        
    round_strategy = round_strategies[c_round]
    if page_type == 1:
        result = story_strategy(mood, health, attribute)
        select_after(4)
        return   
    if round_strategy == -1 :
        select_type = friendship_strategy(action, mood, health, attribute)
        select_after(select_type)
        return
    if round_strategy == -2:
        select_type = train_strategy(action, mood, health, attribute)
        select_after(select_type)
        return
    if round_strategy == -3:
        result = story_strategy(mood, health, attribute)
        select_after(4)
        return    
    if round_strategy == -4:
        select_type = train_strategy(action, mood, health, attribute, isup = True)
        select_after(select_type)
        return
    #根据比赛编号获取比赛信息，并参加
    custom_match(round_strategy)
    select_after(5)

def study_skill(page_type = 0):
    global c_skill_limit
    if page_type == 0:
        touch(Template(r"tpl1694698995089.png", record_pos=(0.332, 0.483), resolution=(720, 1280)))
    elif page_type == 1:
        touch(Template(r"tpl1694613824100.png", record_pos=(-0.206, 0.607), resolution=(720, 1280)))
    elif page_type == 2:
        touch(Template(r"tpl1694791014007.png", record_pos=(-0.219, 0.554), resolution=(720, 1280)))
    while True:
        wait(Template(r"tpl1694695726666.png", record_pos=(0.36, 0.613), resolution=(720, 1280)))
        skills = find_all(Template(r"tpl1694617619351.png", threshold=0.9, record_pos=(0.401, 0.135), resolution=(720, 1280)))
        if skills is not None:
            for i in range(len(skills)):
                mark_point = skills[i]['result']
                if skill_is_in_table(mark_point):
                    touch(mark_point)
                    sleep(0.5)
                    touch(mark_point)
        
        skill_num = 0 
        try:
            skill_num = point2text(skill_point2, 1)
        except Exception as e:
            skill_num = 0
            
        if skill_num <= skill_end_mark and page_type != 2:
            break
        if exists(Template(r"tpl1694617844205.png", threshold=0.9, record_pos=(0.475, 0.55), resolution=(720, 1280))):
            break
        swipe((355, 745), (355, 575), steps = 5, duration = 0.5)
        touch((355, 745))
        sleep(0.5)
    if exists(Template(r"tpl1694618104113.png", threshold=0.7, rgb=True, record_pos=(-0.001, 0.613), resolution=(720, 1280))):
        sleep(1)
        touch(Template(r"tpl1694618104113.png", threshold=0.7, rgb=True, record_pos=(-0.001, 0.613), resolution=(720, 1280)))
        sleep(1)
        wait(Template(r"tpl1694695645999.png", record_pos=(-0.006, -0.8), resolution=(720, 1280)))
        touch(Template(r"tpl1694695669747.png", record_pos=(0.219, 0.749), resolution=(720, 1280)))        
        wait(Template(r"tpl1694695874093.png", record_pos=(-0.004, 0.222), resolution=(720, 1280)))
        touch(Template(r"tpl1694695909066.png", record_pos=(-0.006, 0.268), resolution=(720, 1280)))
        wait(Template(r"tpl1694695726666.png", record_pos=(0.36, 0.613), resolution=(720, 1280)))
        
        c_skill_limit = skill_limit
    else:
        
        c_skill_limit = c_skill_limit + skill_limit_step
        
    touch(Template(r"tpl1694618201791.png", record_pos=(-0.388, 0.817), resolution=(720, 1280)))
    if page_type != 2:
        wait_back_home()
    
def skill_is_in_table(mark_point):
    skill_text_area = (125, mark_point[1] - 70, 400, mark_point[1] - 30)
    
    if skill_text_area[1] <= 465:
        return False
    
    skill_text = point2text(skill_text_area)
    logging.critical("技能ocr文本识别：{}".format(skill_text))
    for i in range(len(skill_table)):
        if str_compare(skill_table[i], skill_text):
            return True
    return False
    
    
def custom_match(round_strategy):
    touch(Template(r"tpl1694698924245.png", record_pos=(0.261, 0.718), resolution=(720, 1280)))
    while True:
        pos = exists(Template(r"tpl1694098144940.png", threshold=0.85, record_pos=(0.206, 0.612), resolution=(1080, 1920)))
        if pos:
            if pos[1] < 1000:
                touch(pos)
                sleep(1)
            else:
                break
    
    match_p = find_match(round_strategy)
    if match_p is not None:
        touch(match_p)
        
    touch(Template(r"tpl1694013298278.png", rgb=True))
    wait(Template(r"tpl1694013350813.png"))
    touch(Template(r"tpl1694013673749.png", rgb=True))
    
    match()

def find_match(name):
    while True:
        matchs = find_all(Template(r"tpl1694699183605.png", record_pos=(-0.108, 0.217), resolution=(720, 1280)))
        if matchs is not None:
            full_screen = G.DEVICE.snapshot()
            for i in range(len(matchs)):
                match_point = (35, matchs[i]['result'][1] - 80, 250, matchs[i]['result'][1] + 30)
                if match_point[1] <= 680:
                    continue
                
                mark = point2text(match_point, 0, full_screen)
                logging.critical("赛事ocr文本识别：{}".format(mark))
                if str_compare(name, mark):
                    return matchs[i]['result']
        
        if exists(Template(r"tpl1694699430851.png", rgb=True, record_pos=(0.471, 0.521), resolution=(720, 1280))):
            break
    
        swipe((375, 930), (375, 741), steps = 15, duration = 1)
        touch((375, 741))
        sleep(0.5)        

def find_support(name):
    
    while True:
        supports = find_all(Template(r"tpl1695807488198.png", record_pos=(-0.178, -0.404), resolution=(720, 1280)))
        for i in range(len(supports)):
            mark_point = supports[i]['result']
            point = (mark_point[0] - 88, mark_point[1] - 120, mark_point[0] + 247, mark_point[1] + 25)
            if name is None or name == "":
                return mark_point
            support_name = point2text(point)
            logging.critical("好友ocr文本识别：{}".format(support_name))
            if str_compare(name, support_name):
                return mark_point
        
        if exists(Template(r"tpl1695809878085.png", rgb=True, record_pos=(0.471, 0.649), resolution=(720, 1280))):
            touch(Template(r"tpl1697769678659.png", threshold=0.85, record_pos=(0.406, 0.507), resolution=(720, 1280)))
            sleep(1)
            continue
        swipe((350, 1000), (350, 300), steps = 15, duration = 2)
        sleep(1.5)
        
def end_strategy():
    wait(Template(r"tpl1694790924855.png", threshold=0.85, record_pos=(0.225, -0.465), resolution=(720, 1280)), timeout = 50)
    
    #技能学习
    study_skill(2)
    sleep(1)
    touch(Template(r"tpl1694791057053.png", record_pos=(0.211, 0.618), resolution=(720, 1280)))
    while True:
        touch((325, 274))
        try:
            next_p = exists(Template(r"tpl1694191806588.png", rgb=True, record_pos=(0.22, 0.387), resolution=(1080, 1920)))
            if next_p:
                touch(next_p)
                sleep(1)
            next_p = exists(Template(r"tpl1695803528738.png", record_pos=(-0.001, 0.747), resolution=(720, 1280)))     
            if next_p:
                touch(next_p)
                sleep(1)
            next_p = exists(Template(r"tpl1694191943555.png", rgb=True, record_pos=(-0.002, 0.752), resolution=(1080, 1920)))
            if next_p:
                touch(next_p)
                sleep(1)
            next_p = exists(Template(r"tpl1695803255375.png", record_pos=(0.001, 0.657), resolution=(720, 1280)))
            if next_p:
                touch(next_p)
                sleep(1)
        except Exception as e:
            continue                      
             
        if exists(Template(r"tpl1695803802160.png", record_pos=(-0.001, 0.806), resolution=(720, 1280))):
            break

    
def cultivate_global_init():
    global is_end
    global c_round
    global c_clock
    global go_out_recheck
    global running_is_edit
    global start_round
    global c_skill_limit
    is_end = False
    c_round = 0
    c_clock = 0
    start_round = 0
    go_out_recheck = False
    running_is_edit = False
    c_skill_limit = skill_limit

    
#剧情策略
def story_strategy(mood, health, attribute):
    global running_is_edit
    global c_clock
    global total_clock
    touch(Template(r"tpl1694613518325.png", record_pos=(0.208, 0.651), resolution=(720, 1280)))
    wait(Template(r"tpl1694013298278.png", rgb=True))
    touch(Template(r"tpl1694013298278.png", rgb=True))
    wait(Template(r"tpl1694013350813.png"))
    touch(Template(r"tpl1694013673749.png", rgb=True))
    
    result = match()
    
    #剧情失败
    while True:
        if not result:
            if c_clock < max_clock and c_clock <= 3 and total_clock > 0:
                touch(Template(r"tpl1694190427175.png", rgb=True, record_pos=(0.224, 0.389), resolution=(1080, 1920)))
                c_clock = c_clock + 1
                total_clock = total_clock - 1
                result = match()
                if result:
                    break
            else:
                touch(Template(r"tpl1694190445082.png", threshold=0.75, rgb=True, record_pos=(-0.217, 0.388), resolution=(1080, 1920)))
                sleep(1)
                next_p = wait(Template(r"tpl1694015047670.png", rgb=True, record_pos=(0.001, 0.751), resolution=(1080, 1920)))
                touch(next_p)
                while True:
                    touch((360, 700))
                    sleep(1)
                    next_p = exists(Template(r"tpl1694703952303.png", threshold=0.8, record_pos=(0.307, 0.746), resolution=(720, 1280)))
                    if next_p is not None:
                        break
                sleep(1)
                touch(next_p)                
                global is_end
                is_end = True
                return False
        else:
            break
        
    return True            
    
    
    
def match():
    wait(Template(r"tpl1694013986036.png"), timeout = 100)
    running_init()
    #如果未解锁查看结果，前往赛事    
    if exists(Template(r"tpl1694785531581.png", threshold=0.8, record_pos=(-0.269, 0.7), resolution=(720, 1280))):
        touch(Template(r"tpl1694014875113.png", rgb=True, record_pos=(0.15, 0.741), resolution=(1080, 1920)))
        next_p = wait(Template(r"tpl1694785649900.png", threshold=0.85, record_pos=(0.001, 0.736), resolution=(720, 1280)), timeout = 100)
        touch(next_p)
        while True:
            next_p = exists(Template(r"tpl1694785715536.png", threshold=0.85, record_pos=(0.279, 0.81), resolution=(720, 1280)))
            if next_p:
                touch(next_p)
                sleep(1)
            next_p = exists(Template(r"tpl1694785824037.png", record_pos=(0.001, 0.388), resolution=(720, 1280)))
            if next_p:
                sleep(1)
                touch(next_p)
                continue
            next_p = exists(Template(r"tpl1694015047670.png", rgb=True, record_pos=(0.001, 0.751), resolution=(1080, 1920)))
            if next_p:
                sleep(1)
                touch(next_p)
                break            
            
    else:
        touch(Template(r"tpl1694014904798.png", rgb=True, record_pos=(-0.146, 0.744), resolution=(1080, 1920)))
        
    while True:
        touch((360, 700))
        next_p = exists(Template(r"tpl1694785824037.png", record_pos=(0.001, 0.388), resolution=(720, 1280)))
        if next_p:
            sleep(1)
            touch(next_p)
            continue
        next_p = exists(Template(r"tpl1694015047670.png", rgb=True, record_pos=(0.001, 0.751), resolution=(1080, 1920)))
        if next_p:
            sleep(1)
            touch(next_p)
            continue
        next_p = exists(Template(r"tpl1694189892761.png", record_pos=(0.282, -0.308), resolution=(1080, 1920)))
        if next_p:
            return False
        next_p = exists(Template(r"tpl1694703952303.png", threshold=0.9, record_pos=(0.307, 0.746), resolution=(720, 1280)))
        if next_p:
            sleep(1)
            touch(next_p)
            break
    return True

    
def running_init():
    global running_is_edit
    if not running_is_edit:
        sleep(1)
        touch(Template(r"tpl1694013986036.png"))
        wait(Template(r"tpl1694014425721.png", threshold=0.9))
        if running == 0:
            touch(Template(r"tpl1694703787655.png", record_pos=(-0.364, 0.19), resolution=(720, 1280)))
        elif running == 1:
            touch(Template(r"tpl1694703796240.png", record_pos=(-0.151, 0.189), resolution=(720, 1280)))
        elif running == 2:
            touch(Template(r"tpl1694703804149.png", record_pos=(0.062, 0.192), resolution=(720, 1280)))
        elif running == 3:
            touch(Template(r"tpl1694703813249.png", record_pos=(0.278, 0.19), resolution=(720, 1280)))
        sleep(1)
        touch(Template(r"tpl1694014613458.png"))
        running_is_edit = True
        wait(Template(r"tpl1694013986036.png"))    
    
def train_strategy(action, mood, health, attribute, isup = False):
    full_screen = G.DEVICE.snapshot()
    # 如果有病优先治病
    if not health :
        treatment()
        return 3
    

    #满体力优先训练
    if action == 100:
        train(full_screen, attribute)
        return 0
    
    #如果心情不为极佳
    if (mood != "极佳" and mood != "上佳") and not isup:
        #体力小于50时外出
        go_out(full_screen)
        return 1
    
    #判断是否集训前
    if not isup and c_round + 2 < len(round_strategies):
        #集训前二天
        if round_strategies[c_round + 1] != -4 and round_strategies[c_round + 2] == -4:
            if action < 60:
                rest(full_screen)
                return 2
        #集训前一天    
        elif round_strategies[c_round + 1] == -4:
            if action <= 80:
                rest(full_screen)
                return 2
            
    if action < 50:
        if action >= 40 and isup:
            train(full_screen, attribute, 4)
            return 0
        if is_go_out_friendship_mark(full_screen) and mood != "极佳":
            go_out(full_screen)
            return 1
        rest(full_screen)
        return 2
    train(full_screen, attribute)
    return 0
    
    
def train(full_screen, attributes, appoint = None):
    task_screen = get_task_screen(full_screen)
    pos = Template(r"tpl1694531664870.png").match_in(task_screen)
    touch((pos[0] + task_area_point[0], pos[1] + task_area_point[1]))
    wait(Template(r"tpl1694005273843.png"))
    try:
        if appoint is not None:
            touch_p = select_train_attribute(appoint)
            touch(touch_p)
            return

        score_coefficient = get_score_coefficient(attributes=attributes)

        max_score = 0
        select_pos = 0
        for i in range(len(strategy)):
            if strategy[i] == 0:
                continue

            select_train_attribute(i)
            scores = get_train_score()
            total_score = 0
            for a in range(len(scores)):
                score = scores[a] * score_coefficient[a]
                total_score = total_score + score
            if total_score > max_score:
                max_score = total_score
                select_pos = i

        touch_p = select_train_attribute(select_pos)
        touch(touch_p)
    except Exception as e:
        touch(Template(r"tpl1694005273843.png"))

def get_score_coefficient(attributes):
    #总属性
    total_attribute = 0
    total_coefficient = 0
    for i in range(len(strategy)):
        if strategy[i] == 0:
            continue
        total_attribute = total_attribute + attributes[i]
        total_coefficient = total_coefficient + strategy[i]

    #得分期望
    score_coefficient = [0, 0, 0, 0, 0]
    for i in range(len(attributes)):
        if strategy[i] == 0:
            continue
        target_score = (strategy[i] / total_coefficient) * total_attribute
        score_coefficient[i] = target_score / attributes[i]
    return score_coefficient


#友情训练策略    
def friendship_strategy(action, mood, health, attribute):
    full_screen = G.DEVICE.snapshot()
    
    #满体力优先训练
    if action == 100:
        tarin_friendship(full_screen, min_count=0)
        return 0  
    # 如果有病优先治病
    if not health :
        treatment()
        return 3
    #如果心情不为极佳或者上佳
    if mood != "极佳" and mood != "上佳":
        #体力小于50时外出
        if action < 50:
            go_out(full_screen)
            return 1
        if tarin_friendship(full_screen, min_count= 3):
            return 0
        go_out(full_screen)
        return 1
    if action >= 40 and action < 50:
        if tarin_friendship(full_screen, min_count = 2, free_action= True):
            return 0
        
    if action <= 40:
        rest(full_screen)
        return 2
    tarin_friendship(full_screen, min_count =0)
    return 0
    
# 0 - 训练之后 1-外出之后 2-休息之后 3-医疗之后 4-剧情比赛之后 5-自定义比赛后    
def select_after(select_tyep = 0):
    while True:
        full_screen = G.DEVICE.snapshot()
        if is_in_home(full_screen):
            return      
        select_event(full_screen)
        parent_extend(full_screen)
        achievement_event(full_screen)
        if select_tyep == 1:
            zhua_wawa(full_screen)
        if is_end_story(full_screen):
            return

def achievement_event(full_screen = None):
    if full_screen is None:
        full_screen = G.DEVICE.snapshot()
    bottom_area_screen = get_bottom_screen(full_screen)
    select_pos = Template(r"tpl1694015236534.png", rgb=False, record_pos=(0.001, 0.659), resolution=(1080, 1920)).match_in(bottom_area_screen)
    if select_pos is not None:
        touch((select_pos[0] + bottom_area_poin[0], select_pos[1] + bottom_area_poin[1]))

#粉丝不足剧情失败
def is_end_story(full_screen = None):
    if full_screen is None:
        full_screen = G.DEVICE.snapshot()
    task_screen = get_task_screen(full_screen)
    end_flag = Template(r"tpl1694791057053.png", threshold=0.85).match_in(task_screen)
    if end_flag is not None:
        global is_end
        is_end = True
        return True
    
    return False

def treatment():
    full_screen = G.DEVICE.snapshot()
    task_screen = get_task_screen(full_screen)
    pos = Template(r"tpl1694186486060.png", rgb=True).match_in(task_screen)
    if pos is not None:
        touch((pos[0] + task_area_point[0], pos[1] + task_area_point[1]))
        wait_out_home()
        return    

def parent_extend(full_screen = None):
    if full_screen is None:
        full_screen = G.DEVICE.snapshot()
    bottom_area_screen = get_bottom_screen(full_screen)
    select_pos = Template(r"tpl1694099905885.png").match_in(bottom_area_screen)
    if select_pos is not None:
        touch((select_pos[0] + bottom_area_poin[0], select_pos[1] + bottom_area_poin[1]))
        
def zhua_wawa(full_screen = None):
    if full_screen is None:
        full_screen = G.DEVICE.snapshot()
    bottom_area_screen = get_bottom_screen(full_screen)
    select_pos = Template(r"tpl1694099462229.png", threshold=0.85).match_in(bottom_area_screen)
    if select_pos is None:
        return
    
    try_count = 0
    while True:
        full_screen = G.DEVICE.snapshot()
        bottom_area_screen = get_bottom_screen(full_screen)
        select_pos = Template(r"tpl1694099462229.png").match_in(bottom_area_screen)
        if select_pos is not None:
            if try_count == 0:
                sleep(1)
                touch((select_pos[0] + bottom_area_poin[0], select_pos[1] + bottom_area_poin[1]), duration = 2)
                try_count = try_count + 1
                continue
            elif try_count == 1:
                sleep(1)
                touch((select_pos[0] + bottom_area_poin[0], select_pos[1] + bottom_area_poin[1]), duration = 1.5)
                try_count = try_count + 1
                continue
            elif try_count == 2:
                sleep(1)
                touch((select_pos[0] + bottom_area_poin[0], select_pos[1] + bottom_area_poin[1]), duration = 1)
                try_count = try_count + 1
                continue
            else:
                sleep(1)
                touch((select_pos[0] + bottom_area_poin[0], select_pos[1] + bottom_area_poin[1]), duration = 1)
                continue
        if exists(Template(r"tpl1694875783629.png", record_pos=(0.004, 0.753), resolution=(720, 1280))):
            touch(Template(r"tpl1694875783629.png", record_pos=(0.004, 0.753), resolution=(720, 1280)))
            return
#选择项目
def select_event(full_screen = None):
    if full_screen is None:
        full_screen = G.DEVICE.snapshot()
    center_area_screen = get_center_screen(full_screen)
    all_select = Template(r"tpl1694611957715.png", threshold=0.85).match_all_in(center_area_screen)
    # select_pos = Template(r"tpl1694611957715.png", threshold=0.85).match_in(center_area_screen)
    # if select_pos is not None:
    #     touch((select_pos[0] + center_area_point[0], select_pos[1] + center_area_point[1]))
    if all_select is not None and len(all_select) > 1:
        select_pos_index = 0
        if len(event_list) > 0:
            title = point2text(event_title_area_point, 0, full_screen)
            logging.critical("事件ocr文本识别：{}".format(title))
            for target_title in event_list:
                if target_title[0] == "*":
                    re_target = target_title[3:]
                    if str_compare(re_target, title):
                        action = get_action(get_top_screen(full_screen))
                        if action <= 80:
                            select_pos_index = int(target_title[1:2]) - 1
                            break
                        else:
                            if int(target_title[1:2]) == 1:
                                select_pos_index = 1
                            break
                else:       
                    re_target = target_title[2:]
                    if str_compare(re_target, title):
                        select_pos_index = int(target_title[0:1]) - 1
                        break
                        
        
        for i in range(len(all_select)):
            for j in range(len(all_select)):
                 if all_select[i]['result'][1] < all_select[j]['result'][1]:
                    temp =  all_select[i]
                    all_select[i] = all_select[j]
                    all_select[j] = temp

        select_pos = all_select[select_pos_index]['result']
        touch((select_pos[0] + center_area_point[0], select_pos[1] + center_area_point[1]))


def is_in_home(full_screen = None):
    if full_screen is None:
        full_screen = G.DEVICE.snapshot()
    center_area = get_center_screen(full_screen)
    home_mark_area = aircv.crop_image(full_screen, home_mark_area_point)
    home_mark = Template(r"tpl1695385387777.png", threshold=0.85).match_in(home_mark_area)
    if home_mark is not None:
        return True
    
    
    home_mark2 = Template(r"tpl1695311347294.png", threshold=0.85).match_in(center_area)
    
    if home_mark2 is not None:
        sleep(1)
        touch(Template(r"tpl1694095949187.png", record_pos=(-0.218, 0.387), resolution=(1080, 1920)))
    return False

def wait_back_home():
    while True:
        if is_in_home():
            return      
           
#根据有情训练    
def tarin_friendship(full_screen, min_count = 0, free_action = False):
    task_screen = get_task_screen(full_screen)
    pos = Template(r"tpl1694531664870.png").match_in(task_screen)
    touch((pos[0] + task_area_point[0], pos[1] + task_area_point[1]))
    wait(Template(r"tpl1694005273843.png"))
    try:    
        if free_action:
            touch_p = select_train_attribute(4)
            if get_friendship_info()[0] >= min_count:
                sleep(1)
                touch(touch_p)
                return True
            touch(Template(r"tpl1694010638710.png", record_pos=(-0.373, 0.826), resolution=(1080, 1920)))
            wait_back_home()
            return False

        select_pos = 0
        max_count = 0
        # 获取当前位置

        for i in range(len(strategy)):
            select_train_attribute(i)
            count = get_friendship_info()[0]
            if count >= max_count:
                if count == max_count and strategy[i] < strategy[select_pos]:
                    continue
                max_count = count
                select_pos = i
                if max_count >= 3:
                    break

        if max_count >= min_count:
            touch_p = select_train_attribute(select_pos)
            sleep(1)
            touch(touch_p)
            return True
        touch(Template(r"tpl1694010638710.png", record_pos=(-0.373, 0.826), resolution=(1080, 1920)))
        wait_back_home()
        return False
    except Exception as e:
        touch(Template(r"tpl1694005273843.png"))
        wait_back_home()
        return True
#选择训练属性    
def select_train_attribute(pos):
    full_screen = G.DEVICE.snapshot()
    
    if pos == 0 :
        speed = aircv.crop_image(full_screen, train_speed_area_point)
        speed_c = Template(r"tpl1694005273843.png").match_in(speed)
        speed_p = Template(r"tpl1694005537644.png", threshold=0.55).match_in(speed)
        speed_p = (speed_p[0] + train_speed_area_point[0] , speed_p[1] + train_speed_area_point[1])
        if speed_c is not None:
            sleep(1)
            return speed_p
        touch(speed_p)
        wait_train_select(train_speed_area_point)
        return speed_p
    if pos == 1:
        endurance = aircv.crop_image(full_screen, train_endurance_area_point)
        endurance_c = Template(r"tpl1694005273843.png").match_in(endurance)
        endurance_p = Template(r"tpl1694005611937.png", threshold=0.55).match_in(endurance)
        endurance_p = (endurance_p[0] + train_endurance_area_point[0] , endurance_p[1] + train_endurance_area_point[1])
        if endurance_c is not None:
            return endurance_p
        touch(endurance_p)
        wait_train_select(train_endurance_area_point)
        return endurance_p
    if pos == 2:
        power = aircv.crop_image(full_screen, train_power_area_point)
        power_c = Template(r"tpl1694005273843.png").match_in(power)
        power_p = Template(r"tpl1694005697910.png", threshold=0.55).match_in(power)
        power_p = (power_p[0] + train_power_area_point[0] , power_p[1] + train_power_area_point[1])
        if power_c is not None:
            return power_p
        touch(power_p)
        wait_train_select(train_power_area_point)
        return power_p
    if pos == 3:
        perseverance = aircv.crop_image(full_screen, train_perseverance_area_point)
        perseverance_c = Template(r"tpl1694005273843.png").match_in(perseverance)
        perseverance_p = Template(r"tpl1694005757330.png", threshold=0.55).match_in(perseverance)
        perseverance_p = (perseverance_p[0] + train_perseverance_area_point[0] , perseverance_p[1] + train_perseverance_area_point[1])
        if perseverance_c is not None:
            return perseverance_p
        touch(perseverance_p)
        wait_train_select(train_perseverance_area_point)
        return perseverance_p
    if pos == 4:
        intelligence = aircv.crop_image(full_screen, train_intelligence_area_point)
        intelligence_c = Template(r"tpl1694005273843.png").match_in(intelligence)
        intelligence_p = Template(r"tpl1694005828320.png", threshold=0.55).match_in(intelligence)
        intelligence_p = (intelligence_p[0] + train_intelligence_area_point[0] , intelligence_p[1] + train_intelligence_area_point[1])
        if intelligence_c is not None:
            return intelligence_p
        touch(intelligence_p)
        wait_train_select(train_intelligence_area_point)
        return intelligence_p

def wait_train_select(xunlian_area_point):
    wait_times = 0
    while True:
        full_screen = G.DEVICE.snapshot()
        select = aircv.crop_image(full_screen, xunlian_area_point)
        select_c = Template(r"tpl1694005273843.png").match_in(select)
        if select_c is not None:
            sleep(1)
            break
        sleep(0.2)
        wait_times = wait_times + 1
        if wait_times > 50:
            raise Exception('选择训练超时异常')
            
#获取友情羁绊信息
#return 【总数，速度，耐力， 力量， 毅力，智力】
def get_friendship_info():
    full_screen = G.DEVICE.snapshot()
    friendship_area_screen = aircv.crop_image(full_screen, friendship_area_point)
    speed_c = 0
    endurance_c = 0
    power_c = 0
    perseverance_c = 0
    intelligence_c = 0
    full_c = 0
    endurances = Template(r"tpl1694610603830.png", threshold=0.85).match_all_in(friendship_area_screen)
    if endurances is not None:
        endurance_c = len(endurances)
    speeds = Template(r"tpl1694610672274.png", threshold=0.85).match_all_in(friendship_area_screen)
    if speeds is not None:
        speed_c = len(speeds)
    
    powers = Template(r"tpl1695302289737.png", threshold=0.85).match_all_in(friendship_area_screen)
    if powers is not None:
        power_c = len(powers)
    perseverances = Template(r"tpl1695301644248.png", threshold=0.85).match_all_in(friendship_area_screen)
    if perseverances is not None:
        perseverance_c = len(perseverances)
    intelligences = Template(r"tpl1695301982066.png", threshold=0.85).match_all_in(friendship_area_screen)
    if intelligences is not None:
        intelligence_c = len(intelligences)
    
    fulls = Template(r"tpl1698329165414.png", threshold=0.97).match_all_in(friendship_area_screen)
    if fulls is not None:
        full_c = len(fulls)
    fulls = Template(r"tpl1697983542239.png", threshold=0.95).match_all_in(friendship_area_screen)
    if fulls is not None:
        full_c = len(fulls) + full_c
    total = speed_c + endurance_c + power_c + perseverance_c + intelligence_c - full_c
    return [total, speed_c, endurance_c, power_c, perseverance_c, intelligence_c]

#获取光圈信息
def get_halo_info():
    full_screen = G.DEVICE.snapshot()
    friendship_area_screen = aircv.crop_image(full_screen, friendship_area_point)
    halo_c = 0
    halos = Template(r"tpl1696948664599.png", threshold=0.6).match_all_in(friendship_area_screen)
    if halos is not None:
        halo_c = len(halos)

    return halo_c

def get_train_score(full_screen = None):
    if full_screen is None:
        full_screen = G.DEVICE.snapshot()
    speed_score = point2text((speed_area_point[0], speed_area_point[1] - 90, speed_area_point[2], speed_area_point[3] - 60), 1, full_screen)
    endurance_score = point2text((endurance_area_point[0], endurance_area_point[1] - 90, endurance_area_point[2], endurance_area_point[3] - 60), 1, full_screen)
    power_score = point2text((power_area_point[0], power_area_point[1] - 90, power_area_point[2], power_area_point[3] - 60), 1, full_screen)
    perseverance_score = point2text((perseverance_area_point[0], perseverance_area_point[1] - 90, perseverance_area_point[2], perseverance_area_point[3] - 60), 1, full_screen)
    intelligence_score = point2text((intelligence_area_point[0], intelligence_area_point[1] - 90, intelligence_area_point[2], intelligence_area_point[3] - 60), 1, full_screen)

    return [speed_score, endurance_score, power_score, perseverance_score, intelligence_score]


def is_go_out_friendship_mark(full_screen):
    task_screen = get_task_screen(full_screen)
    recheck = Template(r"tpl1695981420768.png").match_in(task_screen)
    return recheck is not None

#外出
def go_out(full_screen):
    global go_out_recheck
    task_screen = get_task_screen(full_screen)
    #检查是否有友人头像
    if not go_out_recheck:
        if is_go_out_friendship_mark(full_screen):
            go_out_recheck = True

    pos = Template(r"tpl1693926382372.png").match_in(task_screen)
    if pos is not None:
        touch((pos[0] + task_area_point[0], pos[1] + task_area_point[1]))
        if go_out_recheck:
            wait(Template(r"tpl1695981540263.png", target_pos=8, record_pos=(-0.004, -0.39), resolution=(720, 1280)))
            sleep(1)
            touch(Template(r"tpl1695981540263.png", target_pos=8, record_pos=(-0.004, -0.39), resolution=(720, 1280)))
        wait_out_home()     
    else:
        pos = Template(r"tpl1694101311089.png").match_in(task_screen)
        touch((pos[0] + task_area_point[0], pos[1] + task_area_point[1]))
        wait_out_home()
    
        
        
#休息    
def rest(full_screen):
    task_screen = get_task_screen(full_screen)
    pos = Template(r"tpl1693926793471.png").match_in(task_screen)
    if pos is not None:
        touch((pos[0] + task_area_point[0], pos[1] + task_area_point[1]))
        wait_out_home()
        return
    pos = Template(r"tpl1694101311089.png").match_in(task_screen)
    touch((pos[0] + task_area_point[0], pos[1] + task_area_point[1]))
    wait_out_home()

def get_friendship_screen(full_screen = None):
    if full_screen is None:
        full_screen = G.DEVICE.snapshot()
    friendship_area = aircv.crop_image(full_screen, friendship_area_point)
    return friendship_area
    
def get_task_screen(full_screen = None):
    if full_screen is None:
        full_screen = G.DEVICE.snapshot()
    task_area = aircv.crop_image(full_screen, task_area_point)
    return task_area

def get_top_screen(full_screen = None):
    if full_screen is None:
        full_screen = G.DEVICE.snapshot()
    top_area = aircv.crop_image(full_screen, top_area_point)
    return top_area

def get_bottom_screen(full_screen = None):
    if full_screen is None:
        full_screen = G.DEVICE.snapshot()
    bottom_area = aircv.crop_image(full_screen, bottom_area_poin)
    return bottom_area    

def get_center_screen(full_screen = None):
    if full_screen is None:
        full_screen = G.DEVICE.snapshot()
    center_area = aircv.crop_image(full_screen, center_area_point)
    return center_area       
    

#获取体力状态    
def get_action(top_area):

#     is_full = Template(r"tpl1698198985697.png", threshold=0.993).match_in(top_area)
#     if(is_full is not None):
#         return 100
#     is_90 = Template(r"tpl1698162071213.png", threshold=0.993).match_in(top_area)
#     if(is_90 is not None):
#         return 90
#     is_80 = Template(r"tpl1696936095055.png", threshold=0.993).match_in(top_area)
#     if(is_80 is not None):
#         return 80
#     is_60 = Template(r"tpl1696936131003.png", threshold=0.993).match_in(top_area)
#     if(is_60 is not None):
#         return 60
#     is_50 = Template(r"tpl1696936170736.png", threshold=0.993).match_in(top_area)
#     if(is_50 is not None):
#         return 50
#     is_40 = Template(r"tpl1696936239396.png", threshold=0.993).match_in(top_area)
#     if(is_40 is not None):
#         return 40
    is_40 = Template(r"tpl_tili40.png", threshold=0.993).match_in(top_area)
    if is_40 is not None:
        return 0
    is_50 = Template(r"tpl_tili50.png", threshold=0.993).match_in(top_area)
    if is_50 is not None:
        return 40
    is_60 = Template(r"tpl_tili60.png", threshold=0.993).match_in(top_area)
    if is_60 is not None:
        return 50
    is_80 = Template(r"tpl_tili80.png", threshold=0.993).match_in(top_area)
    if is_80 is not None:
        return 60
    is_90 = Template(r"tpl_tili90.png", threshold=0.993).match_in(top_area)
    if is_90 is not None:
        return 80
    is_95 = Template(r"tpl_tili95.png", threshold=0.993).match_in(top_area)
    if is_95 is not None:
        return 90
    return 100

#获取心情
def get_mood(mood_point):
    return point2text(mood_point)
#获取健康  如果为比赛日则为None
def get_health(task_area, page_type = 0):
    comfort = Template(r"tpl1693917475818.png", rgb=True).match_in(task_area)
    if(comfort is not None):
        return True
    discomfort = Template(r"tpl1694186486060.png", rgb=True).match_in(task_area)
    if(discomfort is not None):
        return False    
    return None

#等待跳出主页
def wait_out_home():
    while True:
        if not is_in_home():
            return

#获取属性
def get_attribute(full_screen, page_type = 0):
    speed = 0
    endurance = 0
    power = 0
    perseverance = 0
    intelligence = 0
    if page_type == 0:
        speed = aircv.crop_image(full_screen, speed_area_point)
        endurance = aircv.crop_image(full_screen, endurance_area_point)
        power = aircv.crop_image(full_screen, power_area_point)
        perseverance = aircv.crop_image(full_screen, perseverance_area_point)
        intelligence = aircv.crop_image(full_screen, intelligence_area_point)
    elif page_type == 1:
        speed = aircv.crop_image(full_screen, (speed_area_point[0], speed_area_point[1] + 66, speed_area_point[2], speed_area_point[3] + 66))
        endurance = aircv.crop_image(full_screen, (endurance_area_point[0], endurance_area_point[1] + 66, endurance_area_point[2], endurance_area_point[3] + 66))
        power = aircv.crop_image(full_screen, (power_area_point[0], power_area_point[1] + 66, power_area_point[2], power_area_point[3] + 66))
        perseverance = aircv.crop_image(full_screen, (perseverance_area_point[0], perseverance_area_point[1] + 66, perseverance_area_point[2], perseverance_area_point[3] + 66))
        intelligence = aircv.crop_image(full_screen, (intelligence_area_point[0], intelligence_area_point[1] + 66, intelligence_area_point[2], intelligence_area_point[3] + 66))

    attributes = [get_attribute_value(speed), get_attribute_value(endurance), get_attribute_value(power), get_attribute_value(perseverance), get_attribute_value(intelligence)]
    return attributes

    
#获取属性列表
def get_attribute_value(attribute_screen):
    attribute = screen2text(attribute_screen, ocr_tyep = 1)
    if attribute == 0:
        attribute = 1200
    return attribute

#获取技能点数
def get_skill(full_screen, page_type = 0):
    if page_type == 0:
        return int(point2text(skill_point, ocr_tyep = 1, full_screen = full_screen))
    elif page_type == 1:
        return int(point2text((skill_point[0], skill_point[1] + 66, skill_point[2], skill_point[3] + 66), ocr_tyep = 1, full_screen = full_screen))

# ocr_tyep = 0 为中文  1 为 英文/数字
def screen2text(screen, ocr_tyep = 0):
    pil_img = cv2_2_pil(screen)
    np_img = np.array(pil_img)
    if ocr_tyep == 0:
        out = cn_ocr.ocr(np_img)
        if out is None or len(out) == 0:
            return ""
        ocr_text = out[0]['text'].replace(" ", "")
        return ocr_fix(ocr_text)
    elif ocr_tyep == 1:
        out = en_ocr.ocr_for_single_line(np_img)
        if out['text'] == '':
            return 0
        return int(out['text'])

# ocr_tyep = 0 为中文  1 为 英文/数字
def point2text(area_point, ocr_tyep = 0, full_screen = None):
    if full_screen is None:
        full_screen = G.DEVICE.snapshot()
    area = aircv.crop_image(full_screen, area_point)
    return screen2text(area, ocr_tyep)

#修复误识别文本
def ocr_fix(ocr_text):
    if ocr_text in ocr_fix_table:
        return ocr_fix_table.get(ocr_text)
    return ocr_text
#字符串比较，允许一个字的容错
def str_compare(str1, str2):
    str1_c = len(str1)
    str2_c = len(str2)
    if abs(str1_c - str2_c) > 1:
        return False
    
    e_count = abs(str1_c - str2_c)
    min_c = min(str1_c, str2_c)
    for i in range(min_c):
        if str1[i] != str2[i]:
            e_count = e_count + 1
            if e_count > 1:
                return False
    return True



init_config()
do_task()







