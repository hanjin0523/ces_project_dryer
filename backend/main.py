from fastapi import FastAPI , WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from fastapi.websockets import WebSocket,WebSocketDisconnect
from pyfcm import FCMNotification
import asyncio
from dryer_controller import controller
from fastapi import Depends
import threading
import json
import dataBaseMaria
from typing import List

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
# dryer_controllers = [controller.DryerOnOff(), controller.DryerOnOff()]
dryer_controllers = {}
dryer_set_number = 0
dryer_set_device_id = ''
connected_clients: List[WebSocket] = []

firebase_config = {
    "api_key" : "AIzaSyCuWyZF6HrW6VuLS1XzaoKVbXtFnqvzuP8",
    "project_id" : "ces_dryer",
}
fcm = FCMNotification(api_key=firebase_config["api_key"])

power_handler_stopped = False

class dry_accept:

    def get_dryer_controller(dryer_number: int):
        try:
            if dryer_number not in dryer_controllers:
                dryer_controllers[dryer_number] = controller.DryerOnOff()
                return True
            else:
                return False
        except Exception as e:
            print('get_dryer_controller처리안됨...', str(e))
    
def get_change_num_main():
    pass

@app.websocket("/ws/{dryer_number}")
async def websocket_endpoint(websocket: WebSocket, dryer_number:int):
    print(dryer_number,"dryer_number----")
    data_array = []
    try:
        await websocket.accept()
        connected_clients.append(websocket)
        print(connected_clients)
        while True:
            total_time = dryer_controllers[dryer_set_device_id].total_time
            test = dryer_controllers[dryer_set_device_id].counter_time
            heat_ray = dryer_controllers[dryer_set_device_id].heat_ray
            blower = dryer_controllers[dryer_set_device_id].blower
            dehumidifier = dryer_controllers[dryer_set_device_id].dehumidifier
            status = dryer_controllers[dryer_set_device_id].dryer_status
            Remaining_time = total_time - test
            try:
                send_time = (Remaining_time/total_time)*100
            except:
                Remaining_time = 0
                send_time = 0
                pass
            rounded_time = round(send_time,1)
            data_array.clear()
            data_array.append(rounded_time)
            data_array.append(test)
            data_array.append(heat_ray)
            data_array.append(blower)
            data_array.append(dehumidifier)
            data_array.append(status)
            encoded_data = json.dumps(data_array)
            try:
                await websocket.send_text(encoded_data)
            except Exception as e:
                print(str(e))
                connected_clients.remove(websocket)
                break
            await asyncio.sleep(1)
            print("소켓열림!!!!---")
    except WebSocketDisconnect:
        websocket.close()
        connected_clients.remove(websocket)
        print("websocket closed")

@app.get("/send_operating_conditions/setting_off")
def operating_conditions_setting_off():
    dryer_controllers[dryer_set_device_id].operating_conditions = []
    dryer_controllers[dryer_set_device_id].counter_time = 0

@app.get("/send_operating_conditions/setting_on")
def send_operating_conditions(dry_number: int):
    # start_time = time.time() 
    result = mariadb.send_operating_conditions(dry_number)
    dryer_controllers[dryer_set_device_id].operating_conditions = result
    dryer_controllers[dryer_set_device_id].operating_conditions_setting()
    # end_time = time.time()  
    # processing_time = end_time - start_time  
    # print(f"Request processed in {processing_time:.2f} seconds")
    return dryer_controllers[dryer_set_device_id].counter_time


@app.get("/change_dryer_num")
def modify_change_dryer_num(request: Request):
    global dryer_set_number
    global dryer_set_device_id
    dryer_set_number = request.query_params.get('dryer_number')
    dryer_set_device_id = request.query_params.get('device_id')
    # dry_accept.dryer_controllers[change_num].dryer_number = change_dry_num
    return

@app.get("/dryer_connection_list/")
def get_dryer_connection_list():
    # result = mariadb.get_dryer_connection_list()
    result = list(dryer_controllers.keys())
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
        return result_list
    except Exception as e:
        print("스테이지불러오기실패", str(e))

@app.post("/power")
async def power(request: Request):
        try:
            data = await request.json()
            setTime = data['time']
            dryer = dryer_controllers[dryer_set_device_id]
            print(dryer,"-dryer--")
            if not dryer.is_running:
                if dryer.setting_time == 0:
                    pass
                    # dryer.set_timer_setting(dryer_set_number)
                power_task = threading.Thread(target=dryer.on_off_timer, args=(dryer_set_number,))
                power_task.start()
                return setTime
            else:
                print("쓰레드가 이미 동작 중입니다.")
        except Exception as e:
            print("소켓연결안됨", str(e))

@app.get("/stop")
async def stop_power():
    global dryer_set_device_id
    try:
        dryer_controllers[dryer_set_device_id].timer_stop()
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
async def get_dry_status(select_num: int):
    try:
        temp_hum_data = dryer_controllers[dryer_set_device_id].get_senser1_data(select_num)
        if temp_hum_data == False:
            del dryer_controllers[dryer_set_device_id]
        print(temp_hum_data,"===temp_hum_data===")
        return temp_hum_data
    except:
        return {"message": "No connected clients."}