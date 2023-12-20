from fastapi import FastAPI , WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from fastapi.websockets import WebSocket,WebSocketDisconnect
import asyncio
from dryer_controller import controller
import threading
import json
import dataBaseMaria
from typing import List
from routers.socket_router import router
from websockets.exceptions import ConnectionClosedError
import socket_class_v3
import logging_file.logging_debug as logging_debug

logger = logging_debug.Logger(__name__).get_logger()
logger.setLevel(logging_debug.logging.DEBUG)

app = FastAPI()
app.include_router(router)

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
dryer_set_device_id = None
connected_clients: List[WebSocket] = []
power_handler_stopped = False

socket_obj = socket_class_v3.Socket_test(host='192.168.0.62', port=8111)

class dry_accept:

    def get_dryer_controller(dryer_id: str):
        try:
            if dryer_id not in dryer_controllers:
                dryer_controllers[dryer_id] = controller.DryerOnOff(socket_obj)
                logger.info("컨트롤러객체 생성 : %s", dryer_controllers[dryer_id])
                return True
            else:
                return False
        except Exception as e:
            logger.error('get_dryer_controller처리안됨...%s', str(e))

def get_change_num_main():
    pass

@app.get("/")
async def root():
    return {"message": "Hi Heatio"}

@app.get("/dryer_status_realtime")
async def dryer_status_realtime(select_num: int) -> List[str]:
    try:
        result = dryer_controllers[dryer_set_device_id].get_dryer_status(select_num)
        return result
    except Exception as e:
        logger.error("건조기상태소켓에러. : %s", str(e))

@app.websocket("/ws/{dryer_number}")
async def websocket_endpoint(websocket: WebSocket, dryer_number:int):
    try:
        await websocket.accept()
        while True:
            controller = dryer_controllers[dryer_set_device_id]
            total_time = controller.total_time
            test = controller.counter_time
            Remaining_time = total_time - test
            send_time = (Remaining_time / total_time) * 100 if total_time != 0 else 0
            rounded_time = round(send_time,1)
            data_array = [
                rounded_time,
                test,
                controller.heat_ray,
                controller.blower,
                controller.dehumidifier,
                controller.dryer_status,
            ]
            encoded_data = json.dumps(data_array)
            try:
                await websocket.send_text(encoded_data)
            except Exception as e:
                print(str(e))
                break
            await asyncio.sleep(1)
    except ConnectionClosedError:
        websocket.close()
    except WebSocketDisconnect:
        websocket.close()

@app.get("/send_operating_conditions/setting_off")
def operating_conditions_setting_off() -> None:
    try:
        dryer_controllers[dryer_set_device_id].operating_conditions = []
        # dryer_controllers[dryer_set_device_id].counter_time = 0
    except Exception as e:
        logger.error("오퍼레이팅오프에러 : %s", str(e))

@app.get("/send_operating_conditions/setting_on")
def send_operating_conditions(dry_number: int) -> int:
    try:
        result = mariadb.send_operating_conditions(dry_number)
        dryer_controllers[dryer_set_device_id].operating_conditions = result
        dryer_controllers[dryer_set_device_id].operating_conditions_setting()
        return dryer_controllers[dryer_set_device_id].counter_time
    except Exception as e:
        logger.error("오퍼레이팅오프에러 : %s", str(e))

@app.get("/change_dryer_num")
def modify_change_dryer_num(request: Request):
    global dryer_set_number
    global dryer_set_device_id

    def str_to_bytes(s):
        first_part = s[:6]
        second_part = s[6:]
        second_part = '00' + second_part
        sum_part = first_part + second_part
        chunks = [sum_part[i:i+2] for i in range(0, len(sum_part), 2)]
        return bytes(int(chunk) for chunk in chunks)
    
    dryer_set_number = request.query_params.get('dryer_number')
    dryer_set_device_id_str = request.query_params.get('device_id')

    byte_array = str_to_bytes(dryer_set_device_id_str)
    dryer_set_device_id = byte_array
    return {"message": "Dryer number changed..."}

@app.get("/dryer_connection_list/")
def get_dryer_connection_list() -> List[str]:
    global dryer_set_device_id

    def str_conversion(packet):
        return ''.join(str(byte) for byte in packet)

    result = list(dryer_controllers.keys())
    result_id = [str_conversion(id) for id in result]
    logger.info("건조기리스트 : %s", dryer_set_device_id) 

    try:
        if dryer_set_device_id is None:
            dryer_set_device_id = result[0]
    except Exception as e:
        logger.error("건조기리스트에러 : %s",str(e))

    return result_id

@app.post("/add_stage_list/")
async def add_stage_list(request: Request) -> None:
    data = await request.json()
    dryNumber = data['dryNumber']
    addTemp = data['addTemp']
    addHum = data['addHum']
    addTime = data['addTime']
    mariadb.add_stage_list(dryNumber, addTemp, addHum, addTime)
    return

@app.delete("/delete_stageNum")
def delete_stageNum(stageNum: str) -> None:
    mariadb.delete_stageNum(stageNum)
    return

@app.patch("/modifyStage/")
async def modify_stage(request: Request) -> None:
    stage_info = await request.json()
    seletStage = stage_info['seletStage']
    settingTemp = stage_info['settingTemp']
    settingHum = stage_info['settingHum']
    settingTime = stage_info['settingTime']
    mariadb.modify_stage(seletStage,settingTemp,settingHum,settingTime)
    return

@app.get("/get_detail_stage")
async def get_detail_recipe(selectNum: int) -> List[str]:
    result = mariadb.get_detail_recipe_list(selectNum)
    return result

@app.post('/add_dry_name/')
async def add_dry_name(request: Request) -> None:
    data = await request.json()
    add_name = data['inputName']
    dryer_number = data['dryerNumber']
    mariadb.add_dry_name(add_name, dryer_number)
    return

@app.delete("/delete_dry_name/")
async def delete_dry_name(request: Request) -> None:
    data = await request.json()
    delete_name = data['selectNum']
    mariadb.delete_dry_name(delete_name)
    return

@app.patch("/modify_dry_name/")
async def modify_dry_name(request: Request) -> None:
    data = await request.json()
    select_num = data['selectNum']
    input_modify = data['inputName']
    mariadb.modify_dry_name(select_num, input_modify)
    return 

@app.get("/get_dry_menulist")
def get_dry_menulist(dryer_number: int) -> List[str]:
    result = mariadb.get_dry_menulist(dryer_number)
    result_list = list(result)
    return result_list

@app.get("/get_detail_recipe/{recipe_num}")
async def get_detail_recipe(recipe_num: int) -> List[str]:
    try:
        result = mariadb.get_detail_recipe(recipe_num)
        result_list = list(result)
        return result_list
    except Exception as e:
        logger.error("스테이지불러오기실패", str(e))

@app.post("/power")##소켓으로빼자
async def power(request: Request) -> None:
        try:
            data = await request.json()
            setTime = data['time']
            dryer = dryer_controllers[dryer_set_device_id]
            if not dryer.is_running:
                if dryer.setting_time == 0:
                    pass
                power_task = threading.Thread(target=dryer.on_off_timer, args=(dryer_set_number,dryer_set_device_id))
                power_task.start()
                return setTime
            else:
                logger.error("쓰레드가 이미 동작 중입니다.")
        except Exception as e:
            logger.error("소켓연결안됨 : %s", str(e))

@app.get("/pause")##소켓으로빼자
async def stop_power() -> None:
    global dryer_set_device_id
    try:
        dryer_controllers[dryer_set_device_id].timer_stop(dryer_set_number)
        # dryer_controllers[change_num_main].dryer_off(['h1_off', 'h2_off', 'h3_off'])
        return {"message": "Power handler stopping..."}
    except Exception as e:
        logger.error("건조기가 없습니다. : %s", str(e))

@app.get("/stop")##소켓으로빼자
async def stop_power() -> None:
    global dryer_set_device_id
    try:
        dryer_controllers[dryer_set_device_id].stop_dryer(dryer_set_number)
        # dryer_controllers[change_num_main].dryer_off(['h1_off', 'h2_off', 'h3_off'])
        return {"message": "Power handler stopping..."}
    except Exception as e:
        logger.error("건조기가 없습니다. : %s", str(e))

@app.post("/deodorization_operation")
async def deodorization_operation(request: Request) -> None:
    global change_num_main
    data = await request.json()
    command = data['arr']
    # dryer_controllers[change_num_main].handler_command(command)
    return

@app.get("/power/status")##소켓으로빼자
async def get_power_status() -> bool:
    global power_handler_stopped
    return {"power_handler_stopped": power_handler_stopped}

@app.get("/dry_status")##소켓으로빼자
async def get_dry_status(select_num: int) -> bool:
    try:
        # if len(dryer_controllers) > 0:
        temp_hum_data = dryer_controllers[dryer_set_device_id].get_senser1_data(select_num)
        return temp_hum_data
        # else:
        #     logger.error("건조기가 전원이 켜지지 않았습니다.")
    except Exception as e:
        logger.error("건조기가 없습니다. : %s", str(e))
        return {"message": "No connected clients."}
    
############테스트############
@app.get("/sessiontest/{command}")
def session_test(command: str):
    dryer_controllers[dryer_set_device_id].session_test(command)

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
