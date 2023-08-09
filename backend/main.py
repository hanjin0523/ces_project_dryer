from fastapi import FastAPI , WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
import asyncio
import re


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

mariadb = dataBaseMaria.DatabaseMaria('localhost', 3306, 'jang', 'jang','cestest','utf8')
# s = socat_class.Socket_test('192.168.0.62', 8111)
# s = socat_class.Socket_test('10.211.55.2', 8111)

power_handler_stopped = False

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
    print(stageNum, "stageNum")
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
def get_dry_menulist():
    result = mariadb.get_dry_menulist()
    result_list = list(result)
    return result_list

@app.get("/get_detail_recipe/{recipe_num}")
def get_detail_recipe(recipe_num: int):
    result = mariadb.get_detail_recipe(recipe_num)
    result_list = list(result)
    print(result_list)
    return result_list

async def power_handle(time1=None):
    global power_handler_stopped
    power_handler_stopped = False
    command = ['h1_on', 'h2_on', 'h3_on']
    command1 = ['h1_off', 'h2_off', 'h3_off']
    try:
        s.power_handler(command)
        for _ in range(time1 * 10):
            if power_handler_stopped:
                break
            await asyncio.sleep(0.1)
        s.power_handler(command1)
    except asyncio.CancelledError:
        print('')
    finally:
        power_handler_stopped = True
    return {"bool":False}

power_task = None

@app.post("/power")
async def power(request: Request):
    global power_task
    global power_handler_stopped
    if power_handler_stopped:
        data = await request.json()
        setTime = data['time']
        power_handler_stopped = False
        power_task = asyncio.create_task(power_handle(setTime))
        return {"message": "Power handler started. The task will be stopped after 10 seconds."}
    else:
        return {"message": "Power handler is already running."}

@app.post("/stop")
async def stop_power(request: Request):
    global power_handler_stopped
    power_handler_stopped = True
    # s.power_handler(['h1_off', 'h2_off', 'h3_off'])
    return {"message": "Power handler stopping..."}

@app.post("/deodorization_operation")
async def deodorization_operation(request: Request):
    data = await request.json()
    command = data['arr']
    s.power_handler(command)
    return

@app.get("/power/status")
async def get_power_status():
    global power_handler_stopped
    return {"power_handler_stopped": power_handler_stopped}

@app.get("/dry_status")
def get_dry_status():
    data = s.senser1()
    data_str = data.decode('utf-8')
    pattern = r'T2=([\d.]+),H2=([\d.]+)'
    match = re.search(pattern, data_str)
    result_array = []
    if match:
        t1_value = float(match.group(1))
        h1_value = float(match.group(2))
        t1_value = int(t1_value)
        h1_value = int(h1_value)
        result_array = [t1_value, h1_value]
    return result_array