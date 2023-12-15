
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import time
import queue
import dataToGraphite
import logging_file.logging_debug as logging_debug

logger = logging_debug.Logger(__name__).get_logger()
logger.setLevel(logging_debug.logging.DEBUG)

class DryerOnOff:
    
    def __init__(self, socket):
        self.socket_obj = socket
        self.my_queue = queue.Queue()
        self.operating_conditions = [] 
        self.elapsed_time: int = 0
        self.dryer_status: bool = False
        self.is_running: bool = False
        self.dryer_number: int = 0
        self.heat_ray: bool = False
        self.blower: bool = False
        self.dehumidifier: bool = False
        self.setting_time: int = 0
        self.total_time = 0
        self.counter_time = 0
        self.set_time: int = 0
        self.stop_timer: int = 0
        self.set_temperature: int = 0
        self.set_humidity: int = 0
        self.status_temp_hum: list = []

    def handler_command(self, input_text):
        result = self.socket_obj.power_on_off(self.dryer_number, input_text)
        self.blower = True
        return result 

    def dryer_off(self, input_text):
        result = self.socket_obj.power_off(self.dryer_number, input_text) 
        self.blower = False
        return result

    def get_senser1_data(self, select_num: int):
        if not self.is_running:
            try:
                result = self.socket_obj.senser(select_num)
                self.status_temp_hum = result
                return result
            except Exception as e:
                logger.error("센서예외처리", str(e))
        else:
            result = self.status_temp_hum
            return result

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
        self.socket_obj.power_on_off(dryer_set_number,self.operating_conditions)
        pass
    
    def str_conversion(self, packet):
        return ''.join(str(byte) for byte in packet)

    def on_off_timer(self, dryer_set_number: int, dryer_set_device_id: str):
        if len(self.socket_obj.clients) >= self.dryer_number:
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
                rec_counter = 0
                while self.setting_time > 0 and self.is_running:
                    self.dehumidifier = True
                    if rec_counter == 5:
                        self.status_temp_hum = self.socket_obj.senser(dryer_set_number)
                        device_id = self.str_conversion(dryer_set_device_id)
                        dataToGraphite.send_data_to_server(self.status_temp_hum, device_id)
                        if self.status_temp_hum is not None:
                            temperature, humidity = self.status_temp_hum
                            self.heat_ray = temperature < self.set_temperature
                            self.blower = humidity > self.set_humidity
                        rec_counter = 0
                    self.set_time += 1
                    self.elapsed_time += 1
                    self.setting_time -= 1
                    self.counter_time -= 1
                    rec_counter += 1
                    if self.setting_time == 0:
                        self.elapsed_time = 0
                    time.sleep(1)
                if not self.is_running:
                    self.dryer_status = False
                    self.heat_ray = False
                    self.blower = False
                    return self.setting_time 
                    # break
            else:
                self.dryer_status = False
                self.set_time = 0
                self.setting_time = 0
                self.elapsed_time = 0
                self.heat_ray = False
                self.dehumidifier = False
                self.blower = False
                self.counter_time = self.total_time
                self.is_running = False
                return self.setting_time 
        else:
            logger.error("웹소켓에러error")
            pass

    def timer_stop(self, dryer_set_number: int):
        self.socket_obj.power_pause(dryer_set_number)
        self.is_running = False
        self.heat_ray = False
        self.blower = False
        self.dryer_status = False
        self.dehumidifier = False
        self.setting_time = self.setting_time

    def stop_and_go(self, dryer_set_number):
        self.socket_obj.power_restart(dryer_set_number)

    def stop_dryer(self, dryer_set_number):
        self.socket_obj.power_stop(dryer_set_number)
        self.is_running = False
        self.dryer_status = False
        self.counter_time = self.total_time
        self.elapsed_time = 0
        self.heat_ray = False
        self.blower = False
        self.dehumidifier = False
        self.setting_time = 0

    def session_test(self, command: str):
        self.socket_obj.test_packet(command)


