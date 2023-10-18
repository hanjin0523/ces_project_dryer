from fastapi import FastAPI , WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from fastapi.websockets import WebSocket, WebSocketDisconnect
from pyfcm import FCMNotification
import asyncio
from dryer_controller import controller
from fastapi import Depends
import threading
import json
import dataBaseMaria
import logging
import time

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

mariadb = dataBaseMaria.DatabaseMaria('211.230.166.59', 3306, 'jang', 'jang','cesdatabase','utf8')
dryer_controllers = [controller.DryerOnOff(), controller.DryerOnOff()]
connected_clients = []

firebase_config = {
    "api_key" : "AIzaSyCuWyZF6HrW6VuLS1XzaoKVbXtFnqvzuP8",
    "project_id" : "ces_dryer",
}
fcm = FCMNotification(api_key=firebase_config["api_key"])

power_handler_stopped = False
# change_num_main = 0

def get_change_num_main(dryer_number: int = 0):
    if dryer_number == 0:
        return 0 
    else:
        return change_num_main

@app.websocket("/ws/{dryer_number}")
async def websocket_endpoint(websocket: WebSocket, dryer_number:int, change_num_main: int = Depends(get_change_num_main)):
    data_array = []
    try:
        await websocket.accept()
        connected_clients.append(websocket)
        while change_num_main == dryer_number:
            pass_time = dryer_controllers[change_num_main].elapsed_time
            test = dryer_controllers[change_num_main].counter_time
            heat_ray = dryer_controllers[change_num_main].heat_ray
            blower = dryer_controllers[change_num_main].blower
            dehumidifier = dryer_controllers[change_num_main].dehumidifier
            status = dryer_controllers[change_num_main].dryer_status
            try:
                send_time = (pass_time/test)*100
                rounded_time = round(send_time,1)
                data_array.clear()
                data_array.append(rounded_time)
                data_array.append(test-pass_time)
                data_array.append(heat_ray)
                data_array.append(blower)
                data_array.append(dehumidifier)
                data_array.append(status)
                encoded_data = json.dumps(data_array)
                await websocket.send_text(encoded_data)
            except Exception as e:
                pass
            await asyncio.sleep(0.1)
        else:
            print("소켓닫힘")
            websocket.close()
    except WebSocketDisconnect:
        connected_clients.remove(websocket)
        print("websocket closed")
        websocket.close()



@app.get("/send_operating_conditions/setting_off")
def operating_conditions_setting_off(change_num_main: int = Depends(get_change_num_main)):
    dryer_controllers[change_num_main].operating_conditions = []
    dryer_controllers[change_num_main].counter_time = 0

@app.get("/send_operating_conditions/setting_on")
def send_operating_conditions(dry_number: int, change_num_main: int = Depends(get_change_num_main)):
    start_time = time.time() 
    result = mariadb.send_operating_conditions(dry_number)
    dryer_controllers[change_num_main].operating_conditions = result
    dryer_controllers[change_num_main].operating_conditions_setting()
    end_time = time.time()  
    processing_time = end_time - start_time  
    print(f"Request processed in {processing_time:.2f} seconds")
    return dryer_controllers[change_num_main].counter_time


@app.get("/change_dryer_num/{change_num}")
def modify_change_dryer_num(change_num: int):
    change_num_main = change_num
    change_dry_num = get_change_num_main(change_num)
    dryer_controllers[change_num].dryer_number = change_dry_num
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

@app.get("/get_detail_stage")
async def get_detail_recipe(selectNum: int):
    result = mariadb.get_detail_recipe_list(selectNum)
    print(result,"----result")
    return result

@app.post('/add_dry_name/')
async def add_dry_name(request: Request):
    data = await request.json()
    print(data)
    add_name = data['inputName']
    dryer_number = data['dryerNumber']
    mariadb.add_dry_name(add_name, dryer_number)
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
async def get_detail_recipe(recipe_num: int):
    try:
        result = mariadb.get_detail_recipe(recipe_num)
        result_list = list(result)
        print(result_list,"---result_list---")
        return result_list
    except Exception as e:
        print("스테이지불러오기실패", str(e))

@app.post("/power")
async def power(request: Request, change_num_main: int = Depends(get_change_num_main)):
        change_num_main = change_num_main
        try:
            # global change_num_main
            data = await request.json()
            setTime = data['time']
            dryer = dryer_controllers[change_num_main]
            if not dryer.is_running:
                if dryer.setting_time == 0:
                    pass
                    dryer.set_timer_setting(change_num_main)
                power_task = threading.Thread(target=dryer.on_off_timer, args=())
                power_task.start()
                return setTime
            else:
                print("쓰레드가 이미 동작 중입니다.")
        except Exception as e:
            print("소켓연결안됨", str(e))

@app.post("/stop")
async def stop_power(request: Request, change_num_main: int = Depends(get_change_num_main)):
    # global change_num_main
    try:
        dryer_controllers[change_num_main].timer_stop()
        # dryer_controllers[change_num_main].dryer_off(['h1_off', 'h2_off', 'h3_off'])
        return {"message": "Power handler stopping..."}
    except Exception as e:
        print("건조기가 없습니다.", str(e))

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
        return {"message": "No connected clients."}