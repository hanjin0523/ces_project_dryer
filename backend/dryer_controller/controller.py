
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import socat_class

import re

s = socat_class.Socket_test('192.168.0.62', 8111, 3)

class DryerOnOff:

    dryer_number: int = 0
    dryer_status: bool = False
    heat_ray: bool = False
    blower: bool = False
    dehumidifier: bool = False

    def handler_command(self, input_text):
        result = s.power_on(self.dryer_number, input_text)
        self.dryer_status = True
        print("작동여부", self.dryer_status)
        return result 

    def dryer_off(self, input_text):
        result = s.power_off(self.dryer_number, input_text) 
        self.dryer_status = False
        print("작동여부", self.dryer_status)
        return result

    def get_senser1_data(self, input_text, select_num):
        result = s.senser(select_num, self.dryer_number,  input_text)
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
                print(result_array, "가져온값")
                return result_array
        else:
            return[00,00]
        
    def get_senser3_data(self, input_text, select_num):
        result = s.senser(select_num, self.dryer_number,  input_text)
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

        

class Dryer_status(DryerOnOff):

    temperature: int = 0
    humidity: int = 0

