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
# socket_obj = socat_class.Socket_test('192.168.0.62', 8111, 3)

power_handler_stopped = False
change_num_main = 0

@app.websocket("/ws/{dryer_number}")
async def websocket_endpoint(websocket: WebSocket, dryer_number:int):
    await websocket.accept()
    while True:
        data_array = []
        set_time = dryer_controllers[dryer_number].setting_time
        pass_time = dryer_controllers[dryer_number].elapsed_time
        test = dryer_controllers[dryer_number].counter_time
        print(set_time,"set_time",pass_time,"pass_time")
        if set_time != 0:
            send_time = (pass_time/test)*100
            rounded_time = round(send_time,1)
            data_array.append(rounded_time)
            data_array.append(set_time)
            encoded_data = json.dumps(data_array)
            await websocket.send_text(encoded_data)
        await asyncio.sleep(1)

@app.get("/change_dryer_num/{change_num}")
def modify_change_dryer_num(change_num: int):
    dryer_controllers[change_num].dryer_number = change_num
    global change_num_main
    change_num_main = change_num
    print(change_num_main)
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


# def power_handle(time1=None):
#     print(change_num_main,"change_num_main")
#     command = ['h1_on', 'h2_on', 'h3_on']
#     command1 = ['h1_off', 'h2_off', 'h3_off']
#     test_time = 0
#     try:
#         dryer_controller.handler_command(command)
#         while time1 >= test_time:
#             time.sleep(1)
#             test_time += 1
#         dryer_controller.handler_command(command1)
        # controller = dryer_controller if change_num_main == 0 else dryer_controller1
        # if time1:
        #     dryer_controller.handler_command(command)
        #     time.sleep(time1)
        #     dryer_controller.handler_command(command1)
#     except asyncio.CancelledError:
#         print('')
#     return {"bool": False}

# def power_handle1(time1=None):
#     print(change_num_main,"change_num_main")
#     command = ['h1_on', 'h2_on', 'h3_on']
#     command1 = ['h1_off', 'h2_off', 'h3_off']
#     test_time = 0
#     try:
#         dryer_controller1.handler_command(command)
#         while time1 >= test_time:
#             time.sleep(1)
#             test_time += 1
#         dryer_controller1.handler_command(command1)
#     except asyncio.CancelledError:
#         print('')
#     return {"bool": False}


@app.post("/power")
async def power(request: Request):
        global change_num_main
        data = await request.json()
        setTime = data['time']
        print(change_num_main)
        if change_num_main == 0:
            print("0번작동")
            power_task = threading.Thread(target=dryer_controllers[0].on_off_timer, args=(setTime, change_num_main))
            power_task.start()
            return setTime
        if change_num_main == 1:
            print("1번작동")
            power_task1 = threading.Thread(target=dryer_controllers[1].on_off_timer, args=(setTime, change_num_main))
            power_task1.start()
            return setTime
        return {"message": "Power handler started. The task will be stopped after 10 seconds."}

@app.post("/stop") 
async def stop_power(request: Request):
    global change_num_main
    dryer_controllers[change_num_main].dryer_off(['h1_off', 'h2_off', 'h3_off'])
    return {"message": "Power handler stopping..."}

@app.post("/deodorization_operation")
async def deodorization_operation(request: Request):
    global change_num_main
    data = await request.json()
    command = data['arr']
    dryer_controllers[change_num_main].handler_command(command)
    return

@app.get("/power/status")
async def get_power_status():
    global power_handler_stopped
    return {"power_handler_stopped": power_handler_stopped}

@app.get("/dry_status")
def get_dry_status(select_num: int):
    print(select_num,"select_num")
    try:
        dry_status_data = dryer_controllers[select_num].get_senser1_data(['senser1'], select_num)
        return dry_status_data
    except:
        return {"message": "list index out of range error"}

# out_count = 20
# target_1 = '192.168.0.24'
# target_1 = '192.168.0.23'

# setup_init_time = time.time() + 10.0
# global_time = time.time()
# set_global_time = time.time()
# while True:
#     time.sleep(0.5)
#     global_time = time.time()
#     if global_time > set_global_time:
#         set_global_time = global_time + 1.0
#         print("test> " + str(global_time))
#         if len(socket_obj.clients) > 0:
#             for i in socket_obj.clients:
#                 client_settime = i[2]
#                 if global_time > client_settime: 
#                     i[0].sendall('h1_off'.encode())
#                     print("off")
#                 else: 
#                     i[0].sendall('h1_on'.encode())
#                     print("on")
