import json
import math
import threading
import time

from pymavlink import mavutil


def _send_telemetry_info(self, process_telemetry_info, update_position_callback):
    self.alt = 0
    self.sendTelemetryInfo = True
    while self.sendTelemetryInfo:
        #msg = self.vehicle.recv_match(type='AHRS2', blocking= True).to_dict()
        msg = self.vehicle.recv_match(type='GLOBAL_POSITION_INT', blocking= True)
        if msg:
            msg = msg.to_dict()
            self.lat = float(msg['lat'] / 10 ** 7)
            self.lon = float(msg['lon'] / 10 ** 7)
            self.alt = float(msg['relative_alt']/1000)
            self.heading = float(msg['hdg'] / 100)

            vx = float(msg['vx'])
            vy = float(msg['vy'])
            self.groundSpeed = math.sqrt( vx*vx+vy*vy)/100
            telemetry_info = {
                'lat': self.lat,
                'lon': self.lon,
                'alt': self.alt,
                'groundSpeed':  self.groundSpeed,
                'heading': self.heading,
                'state': self.state
            }
            update_position_callback(self.lat, self.lon)

            if self.id == None:
                process_telemetry_info(telemetry_info)
            else:
                process_telemetry_info(self.id, telemetry_info)
        time.sleep(1)


def send_telemetry_info(self, process_telemetry_info, update_position_callback):
    #if not hasattr(self, 'telemetryThread') or not self.telemetryThread.is_alive():
    telemetryThread = threading.Thread(target=self._send_telemetry_info, args=[process_telemetry_info, update_position_callback])
    telemetryThread.start()


def stop_sending_telemetry_info(self):
    self.sendTelemetryInfo = False