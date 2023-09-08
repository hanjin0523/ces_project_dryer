from fastapi import FastAPI , WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from fastapi.websockets import WebSocket, WebSocketDisconnect
import asyncio
import re
from dryer_controller import controller
import atexit
import threading
import time
import datetime
import json
import dataBaseMaria
import socat_class


app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mariadb = dataBaseMaria.DatabaseMaria('211.230.166.113', 3306, 'jang', 'jang','cesdatabase','utf8')
dryer_controllers = [controller.DryerOnOff(), controller.DryerOnOff()]

power_handler_stopped = False
change_num_main = 0

@app.websocket("/ws/{dryer_number}")
async def websocket_endpoint(websocket: WebSocket, dryer_number:int):
    global change_num_main
    data_array = []
    try:
        await websocket.accept()
        print(change_num_main, "chang",dryer_number,"number","\033[31mRed change_num_main,dryer_number\033[0m")
        while change_num_main == dryer_number:
            set_time = dryer_controllers[change_num_main].setting_time
            pass_time = dryer_controllers[change_num_main].elapsed_time
            test = dryer_controllers[change_num_main].counter_time
            heat_ray = dryer_controllers[change_num_main].heat_ray
            blower = dryer_controllers[change_num_main].blower
            status = dryer_controllers[change_num_main].dryer_status
            print(test,"---test")
            print(set_time,"---set_time")
            print(pass_time,"---pass_time")
            try:
                send_time = (pass_time/test)*100
                rounded_time = round(send_time,1)
                data_array.clear()
                data_array.append(rounded_time)
                data_array.append(test-pass_time)
                data_array.append(heat_ray)
                data_array.append(blower)
                data_array.append(status)
                encoded_data = json.dumps(data_array)
                await websocket.send_text(encoded_data)
            except Exception as e:
                print(str(e),"???----???----")
            await asyncio.sleep(1)
        else:
            print("소켓닫힘")
            websocket.close()
    except WebSocketDisconnect:
        print("websocket closed")
        websocket.close()

@app.get("/send_operating_conditions/setting_off")
def operating_conditions_setting_off():
    dryer_controllers[change_num_main].operating_conditions = []
    dryer_controllers[change_num_main].counter_time = 0

@app.get("/send_operating_conditions/setting_on")
def send_operating_conditions(dry_number: int):
    result = mariadb.send_operating_conditions(dry_number)
    dryer_controllers[change_num_main].operating_conditions = result
    dryer_controllers[change_num_main].operating_conditions_setting()

@app.get("/change_dryer_num/{change_num}")
def modify_change_dryer_num(change_num: int):
    global change_num_main
    change_num_main = change_num
    dryer_controllers[change_num].dryer_number = change_num
    return

@app.get("/dryer_connection_list/")
def get_dryer_connection_list():
    result = mariadb.get_dryer_connection_list()
    return result

@app.post("/add_stage_list/")
async def add_stage_list(request: Request):
    data = await request.json()
    dryNumber = data['dryNumber']
    addTemp = data['addTemp']
    addHum = data['addHum']
    addTime = data['addTime']
    mariadb.add_stage_list(dryNumber, addTemp, addHum, addTime)
    return

@app.delete("/delete_stageNum")
def delete_stageNum(stageNum: str):
    mariadb.delete_stageNum(stageNum)
    return

@app.patch("/modifyStage/")
async def modify_stage(request: Request):
    stage_info = await request.json()
    seletStage = stage_info['seletStage']
    settingTemp = stage_info['settingTemp']
    settingHum = stage_info['settingHum']
    settingTime = stage_info['settingTime']
    mariadb.modify_stage(seletStage,settingTemp,settingHum,settingTime)
    return

@app.get("/get_detail_recipe")
async def get_detail_recipe(selectNum: int):
    result = mariadb.get_detail_recipe_list(selectNum)
    return result

@app.post('/add_dry_name/')
async def add_dry_name(request: Request):
    data = await request.json()
    add_name = data['inputName']
    mariadb.add_dry_name(add_name)
    return

@app.delete("/delete_dry_name/")
async def delete_dry_name(request: Request):
    data = await request.json()
    delete_name = data['selectNum']
    mariadb.delete_dry_name(delete_name)
    return

@app.patch("/modify_dry_name/")
async def modify_dry_name(request: Request):
    data = await request.json()
    print(data)
    select_num = data['selectNum']
    input_modify = data['inputName']
    mariadb.modify_dry_name(select_num, input_modify)
    return 

@app.get("/get_dry_menulist")
def get_dry_menulist(dryer_number: int):
    result = mariadb.get_dry_menulist(dryer_number)
    result_list = list(result)
    return result_list

@app.get("/get_detail_recipe/{recipe_num}")
def get_detail_recipe(recipe_num: int):
    result = mariadb.get_detail_recipe(recipe_num)
    result_list = list(result)
    print(result_list)
    return result_list

@app.post("/power")
async def power(request: Request):
        global change_num_main
        data = await request.json()
        if data['time'] == 0:
            setTime = 100000
        elif data['time'] != 0:
            setTime = data['time']
        dryer = dryer_controllers[change_num_main]
        if not dryer.is_running:
            if dryer.setting_time == 0:
                pass
                dryer.set_timer_setting(change_num_main)
            print(dryer,"선택된거..")
            power_task = threading.Thread(target=dryer.on_off_timer, args=())
            power_task.start()
            return setTime
        else:
            print("쓰레드가 이미 동작 중입니다.")

@app.post("/stop") 
async def stop_power(request: Request):
    global change_num_main
    dryer_controllers[change_num_main].timer_stop()
    # dryer_controllers[change_num_main].dryer_off(['h1_off', 'h2_off', 'h3_off'])
    return {"message": "Power handler stopping..."}

@app.post("/deodorization_operation")
async def deodorization_operation(request: Request):
    global change_num_main
    data = await request.json()
    command = data['arr']
    # dryer_controllers[change_num_main].handler_command(command)
    return

@app.get("/power/status")
async def get_power_status():
    global power_handler_stopped
    return {"power_handler_stopped": power_handler_stopped}

@app.get("/dry_status")
def get_dry_status(select_num: int):
    try:
        dry_status_data = dryer_controllers[select_num].get_senser1_data(['senser1'], select_num)
        return dry_status_data
    except:
        return {"message": "list index out of range error"}


