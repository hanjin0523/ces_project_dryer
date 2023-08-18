
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

    def get_senser_data(self, input_text):
        result = s.senser(self.dryer_number, input_text)
        data_str = result.decode('utf-8')
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

