
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import socat_class
import time
import re
import queue

socket_obj = socat_class.Socket_test('192.168.0.62', 8111, 3)

class DryerOnOff:
    def __init__(self):
        self.my_queue = queue.Queue()

    is_running: bool = False
    dryer_number: int = 0
    dryer_status: bool = False
    heat_ray: bool = False
    blower: bool = False
    dehumidifier: bool = False
    setting_time: int = 0
    elapsed_time: int = 0 ##경과시간..
    set_time: int = 0
    counter_time: int = 0
    stop_timer: int = 0
    temperature: int = 0
    humidity: int = 0
    set_temperature: int = 0
    set_humidity: int = 0
    total_time = 0

    operating_conditions = [] 

    def handler_command(self, input_text):
        result = socket_obj.power_on_off(self.dryer_number, input_text)
        self.blower = True
        return result 

    def dryer_off(self, input_text):
        result = socket_obj.power_off(self.dryer_number, input_text) 
        self.blower = False
        return result

    def get_senser1_data(self, input_text, select_num):
        result = socket_obj.senser(select_num, self.dryer_number,  input_text)
        if result is not None:
            data_str = result.decode('utf-8')
            pattern = r'T1=([\d.]+),H1=([\d.]+)'
            match = re.search(pattern, data_str)
            result_array = []
            if match:
                t1_temperature = float(match.group(1))
                h1_humidity = float(match.group(2))
                self.temperature = t1_temperature
                self.humidity = h1_humidity
                result_array = [t1_temperature, h1_humidity]
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
                return result_array
        else: 
            return [10, 10]  # 수정된 부분: [00, 00] 대신 [0, 0]으로 반환합니다.

    def set_timer_setting(self, dryer_number):
        # global_time = round(time.time())
        # self.set_time = global_time - (setting_time+self.stop_timer)
        self.dryer_number = dryer_number
        # self.setting_time = setting_time
        # self.counter_time = setting_time

    def add_task_to_queue(self, task):
        self.my_queue.put(task)

    def operating_conditions_setting(self,):
        # self.counter_time = 0
        for operating in self.operating_conditions:
            self.counter_time += operating[3]

    def on_off_timer(self):
        if len(socket_obj.clients) >= self.dryer_number:
            try:
                global_time = round(time.time())
                for myqueue in self.operating_conditions:
                    self.is_running = True
                    self.dryer_status = True
                    self.set_time = global_time - ((myqueue[3]+1)+self.stop_timer)
                    self.setting_time = int(myqueue[3])
                    self.set_temperature = int(myqueue[4])
                    self.set_humidity = int(myqueue[5])##데이터베이스에서 시간가져옴
                    while self.setting_time > 0 and self.is_running:
                        print(self.setting_time, "남은시간====")
                        time.sleep(1)
                        self.set_time += 1
                        self.elapsed_time += 1
                        self.setting_time -= 1
                        if self.set_temperature > self.temperature:
                            self.heat_ray = True
                            socket_obj.power_on_off(self.dryer_number,['h1_on','h2_on','h3_on'])
                        elif self.set_temperature < self.temperature:
                            self.heat_ray = False 
                            socket_obj.power_on_off(self.dryer_number,['h1_off','h2_off','h3_off'])
                        if self.set_humidity > self.humidity:
                            self.dryer_off(['fan1_off', 'fan2_off'])## 여기에 on할거 모두 적어야함
                        elif self.set_humidity < self.humidity:
                            self.handler_command(['fan1_on', 'fan2_on'])
                    else:
                        self.heat_ray = False
                        self.blower = False
                        self.dryer_status = False
                self.elapsed_time = 0
                print("여기에 코드가 실행되어야하는데 이게 맞냐!!!!")
            except Exception as e:  
                print(str(e),"error")
            else:
                socket_obj.power_on_off(self.dryer_number,['h1_off','h2_off','h3_off'])
                self.dryer_off(['fan1_of','fan2_of'])
        else:
            print("error")
            pass

    def timer_stop(self,):
        self.stop_timer = self.setting_time
        self.heat_ray = False   ##열선작동여부를 전송
        self.blower = False
        self.dryer_status = False
        self.is_running = False

class Dryer_status(DryerOnOff):

    temperature: int = 0
    humidity: int = 0


    # def on_off_timer(self):
    #     input_text_off = ['h1_off','h2_off','h3_off']
    #     if len(socket_obj.clients) >= self.dryer_number:
    #         try:
    #             first_client_socket = socket_obj.clients[self.dryer_number]
    #             first_client_socket[0].sendall('h1_off'.encode())

    #             while self.setting_time > 0 and self.is_running:
    #                 print(self.stop_timer, "stop_timer", self.dryer_number,"dryer_number")
    #                 time.sleep(1)
    #                 # socket_obj.power_on_off(self.dryer_number,input_text_on)
    #                 first_client_socket[0].sendall('h1_on'.encode()) ## 여기에 on할거 모두 적어야함
    #                 self.heat_ray = True   ##열선작동여부를 전송
    #                 self.blower = True
    #                 self.set_time += 1
    #                 self.elapsed_time += 1
    #                 self.setting_time -= 1
    #             else:
    #                 self.heat_ray = False   ##열선작동여부를 전송
    #                 self.blower = False
    #                 self.is_running = False
    #                 # socket_obj.power_on_off(self.dryer_number,input_text_off)
    #                 first_client_socket[0].sendall('h1_off'.encode())
    #                 if self.setting_time == 0:
    #                     self.elapsed_time = 0
    #         except Exception as e:
    #             print(str(e),"error")
    #     else:
    #         print("error")
    #         pass