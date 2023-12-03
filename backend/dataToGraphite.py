import socket
import pickle
import struct
import threading
import time
import config



class CarbonIface(object):
    def __init__(self, host, port, event_url=None):
        self.host = host
        self.port = port
        self.event_url = event_url
        self.__data = []
        self.__data_lock = threading.Lock()

    def add_data(self, metric, value, ts=None):
        if not ts:
            ts = time.time()
        if self.__data_lock.acquire():
            self.__data.append((metric, (ts, value)))
            self.__data_lock.release()
            return True
        return False

    def add_data_dict(self, dd):
        if self.__data_lock.acquire():
            for k, v in dd.items():
                ts = v.get("ts", time.time())
                value = v.get("value")
                self.__data.append((k, (ts, value)))
            self.__data_lock.release()
            return True
        return False

    def add_data_list(self, dl):
        if self.__data_lock.acquire():
            self.__data.extend(dl)
            self.__data_lock.release()
            return True
        return False

    def send_data(self, data=None):
        save_in_error = False

        if not data:
            if self.__data_lock.acquire():
                data = self.__data
                self.__data = []
                save_in_error = True
                self.__data_lock.release()
            else:
                return False

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        payload = pickle.dumps(data)
        header = struct.pack("!L", len(payload))
        message = header + payload

        s.connect((self.host, self.port))

        try:
            s.send(message)
        except:
            print("Error when sending data to carbon")
            if save_in_error:
                self.__data.extend(data)
            return False
        else:
            print('Sent data to {host}:{port}: {0} metrics, {1} bytes'.format(len(data), len(message), host = self.host, port=self.port))
            return True
        finally:
            s.close()

def send_data_to_server(temp_hum_data, dryer_set_device_id):
    print(temp_hum_data,dryer_set_device_id,"----그라파이트에 데이터 보내기---")
    try:
        field = ['status_temp', 'status_hum']
        # carbon = CarbonIface(config.BACKEND_CONFIG['dbip'], 3332)
        carbon = CarbonIface(config.BACKEND_CONFIG['dbip'], 2004)
        ts = time.time()
        for i in range(0, len(field)):
            metric = config.BACKEND_CONFIG['metric'] + dryer_set_device_id + field[i]
            carbon.add_data(metric, temp_hum_data[i], ts)
        carbon.send_data()
        return True
    except Exception as e:
        print("그라파이트에러", e)