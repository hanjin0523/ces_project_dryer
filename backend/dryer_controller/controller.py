
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import socat_class
import time
import re

socket_obj = socat_class.Socket_test('192.168.0.62', 8111, 3)

class DryerOnOff:
    def __init__(self):
        pass
    
    dryer_number: int = 0
    dryer_status: bool = False
    heat_ray: bool = False
    blower: bool = False
    dehumidifier: bool = False
    setting_time: int = 0
    elapsed_time: int = 0 ##경과시간..
    set_time: int = 0
    counter_time: int = 0

    def handler_command(self, input_text):
        result = socket_obj.power_on(self.dryer_number, input_text)
        self.dryer_status = True
        print("작동여부", self.dryer_status)
        return result 

    def dryer_off(self, input_text):
        result = socket_obj.power_off(self.dryer_number, input_text) 
        self.dryer_status = False
        print("작동여부", self.dryer_status)
        return result

    def get_senser1_data(self, input_text, select_num):
        result = socket_obj.senser(select_num, self.dryer_number,  input_text)
        if result is not None:
            data_str = result.decode('utf-8')
            pattern = r'T1=([\d.]+),H1=([\d.]+)'
            match = re.search(pattern, data_str)
            result_array = []
            print(data_str)
            if match:
                t1_value = float(match.group(1))
                h1_value = float(match.group(2))
                result_array = [t1_value, h1_value]
                return result_array
        else:
            return[00,00]
        
    def get_senser3_data(self, input_text, select_num):
        result = socket_obj.senser(select_num, self.dryer_number,  input_text)
        if result is not None:
            data_str = result.decode('utf-8')
            pattern = r'T1=([\d.]+),H1=([\d.]+)'
            match = re.search(pattern, data_str)
            result_array = []
            if match:
                t2_value = float(match.group(1))
                h2_value = float(match.group(2))
                result_array = [t2_value, h2_value]
                print(result_array,"가져온값22")
                return result_array
        else: 
            return [10, 10]  # 수정된 부분: [00, 00] 대신 [0, 0]으로 반환합니다.

    def on_off_timer(self, setting_time, dryer_num):
        global_time = round(time.time())
        self.set_time = global_time - setting_time
        self.setting_time = setting_time
        self.counter_time = setting_time
        if len(socket_obj.clients) >= dryer_num:
            first_client_socket = socket_obj.clients[dryer_num]
            while global_time >= self.set_time:
                time.sleep(1)
                first_client_socket[0].sendall('h1_on'.encode()) ## 여기에 on할거 모두 적어야함
                self.set_time += 1
                self.elapsed_time += 1
                self.setting_time -= 1
                print(f"{dryer_num}번가동중..", global_time, self.set_time)
            else:
                first_client_socket[0].sendall('h1_off'.encode())
                self.setting_time = 0
                self.elapsed_time = 0
                self.set_time = 0
                print("휴동중...")
                return 
        else:
            print("error")
            pass

class Dryer_status(DryerOnOff):

    temperature: int = 0
    humidity: int = 0

