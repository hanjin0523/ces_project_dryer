
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

# import socat_class
import socket_class_v3
import time
import re
import queue
import threading
import dataToGraphite

# socket_obj = socat_class.Socket_test('192.168.0.62', 8111, 3)
socket_obj = socket_class_v3.Socket_test(host='192.168.0.62', port=8111)

class DryerOnOff:
    
    def __init__(self):
        self.my_queue = queue.Queue()
        self.operating_conditions = [] 
        self.elapsed_time: int = 0 ##경과시간..
        self.dryer_status: bool = False
        self.is_running: bool = False
        self.dryer_number: int = 0
        self.heat_ray: bool = False
        self.blower: bool = False
        self.dehumidifier: bool = False
        self.setting_time: int = 0
        self.elapsed_time: int = 0 ##경과시간..
        self.total_time = 0
        self.counter_time = 0
        self.set_time: int = 0
        self.stop_timer: int = 0
        self.temperature: int = 0
        self.humidity: int = 0
        self.set_temperature: int = 0
        self.set_humidity: int = 0
        self.status_temp_hum: list = []

    def handler_command(self, input_text):
        result = socket_obj.power_on_off(self.dryer_number, input_text)
        self.blower = True
        return result 

    def dryer_off(self, input_text):
        result = socket_obj.power_off(self.dryer_number, input_text) 
        self.blower = False
        return result

    def get_senser1_data(self, select_num: int, dryer_set_device_id: str):
        try:
            result = socket_obj.senser(select_num, dryer_set_device_id)
            self.status_temp_hum = result
            return result
        except Exception as e:
            print("센서예외처리", str(e))

    def test(self):
        return self.status_temp_hum

    def set_timer_setting(self, dryer_number):
        # global_time = round(time.time())
        # self.set_time = global_time - (setting_time+self.stop_timer)
        self.dryer_number = dryer_number
        # self.setting_time = setting_time
        # self.counter_time = setting_time

    def add_task_to_queue(self, task):
        self.my_queue.put(task)

    def operating_conditions_setting(self,):
        self.counter_time = 0
        total_sum_time = 0
        for operating in self.operating_conditions:
            stage_time = operating[3]
            self.counter_time += stage_time
            total_sum_time += stage_time
        self.counter_time = total_sum_time
        self.total_time = total_sum_time
        return total_sum_time

    def controller_on(self, dryer_set_number):
        socket_obj.power_on_off(dryer_set_number,self.operating_conditions)
        pass
    
    def on_off_timer(self, dryer_set_number: int, dryer_set_device_id: str):
        if len(socket_obj.clients) >= self.dryer_number:
            global_time = round(time.time())
            self.is_running = True
            self.dryer_status = True
            if self.setting_time == 0:
                self.controller_on(dryer_set_number)
            for myqueue in self.operating_conditions:
                self.set_time = global_time - ((myqueue[3] + 1) + self.stop_timer)
                if self.elapsed_time == 0:
                    self.setting_time = int(myqueue[3])
                else:
                    self.stop_and_go(dryer_set_number)
                    self.setting_time = int(myqueue[3])
                    self.setting_time = self.setting_time - self.elapsed_time           
                self.set_temperature = int(myqueue[4])
                self.set_humidity = int(myqueue[5])##데이터베이스에서 시간가져옴
                # self.controller_on(dryer_set_number)
                while self.setting_time > 0 and self.is_running:
                    self.dehumidifier = True
                    if self.status_temp_hum:
                        dataToGraphite.send_data_to_server(self.status_temp_hum, dryer_set_device_id)
                        if self.status_temp_hum[0] < self.set_temperature:
                            self.heat_ray = True
                        else:
                            self.heat_ray = False
                        if self.status_temp_hum[1] > self.set_humidity:
                            self.blower = True
                        else:
                            self.blower = False
                    self.set_time += 1
                    self.elapsed_time += 1
                    self.setting_time -= 1
                    self.counter_time -= 1
                    print(self.setting_time, "남은시간..-----")
                    if self.setting_time == 0:
                        self.elapsed_time = 0
                    time.sleep(1)
                if not self.is_running:
                    self.dryer_status = False
                    self.heat_ray = False
                    self.blower = False
                    break
            else:
                self.dryer_status = False
                self.set_time = 0
                self.setting_time = 0
                self.elapsed_time = 0
                self.heat_ray = False
                self.dehumidifier = False
                self.blower = False
                self.counter_time = 0
                self.is_running = False
        else:
            print("error")
            pass

    def timer_stop(self, dryer_set_number: int):
        socket_obj.power_pause(dryer_set_number)
        self.is_running = False
        self.heat_ray = False
        self.blower = False
        self.dehumidifier = False
        self.dryer_status = False
        self.setting_time = self.setting_time

    def stop_and_go(self, dryer_set_number):
        socket_obj.power_restart(dryer_set_number)

    def stop_dryer(self, dryer_set_number):
        socket_obj.power_stop(dryer_set_number)
        self.is_running = False
        self.dryer_status = False
        self.counter_time = 0
        self.elapsed_time = 0
        self.total_time = 0
        self.heat_ray = False
        self.blower = False
        self.dehumidifier = False
        self.setting_time = 0

    def session_test(self, command: str):
        socket_obj.test_packet(command)


