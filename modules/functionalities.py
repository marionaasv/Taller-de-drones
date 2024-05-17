import threading
import time
import json
import math

from pymavlink import mavutil
import pymavlink.dialects.v20.all as dialect


# ====== CONNECT/DISCONNECT ======

def _handle_heartbeat(self):
    while True:
        msg = self.vehicle.recv_match(
            type='HEARTBEAT', blocking=True)
        if msg.base_mode == 89 and self.state == 'armed' :
            self.state = 'connected'


# Some more small functions
def _connect(self, connection_string, baud, callback=None, params=None):
    self.vehicle = mavutil.mavlink_connection(connection_string, baud)
    self.vehicle.wait_heartbeat()
    handleThread = threading.Thread (target = self._handle_heartbeat)
    handleThread.start()
    self.state = "connected"
    '''frequency_hz = 1
    self.vehicle.mav.command_long_send(
        self.vehicle.target_system, self.vehicle.target_component,
        mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL, 0,
        mavutil.mavlink.MAVLINK_MSG_ID_GLOBAL_POSITION_INT,  # The MAVLink message ID
        1e6 / frequency_hz,
        # The interval between two messages in microseconds. Set to -1 to disable and 0 to request default rate.
        0, 0, 0, 0,  # Unused parameters
        0,
        # Target address of message stream (if message has target address fields). 0: Flight-stack default (recommended), 1: address of requestor, 2: broadcast.
    )'''
    self.vehicle.mav.request_data_stream_send(
        self.vehicle.target_system, self.vehicle.target_component,
        mavutil.mavlink.MAV_DATA_STREAM_POSITION,
        10,
        1
    )
    if callback != None:
        if self.id == None:
            if params == None:
                callback()
            else:
                callback(params)
        else:
            if params == None:
                callback(self.id)
            else:
                callback(self.id, params)


def connect(self,
            connection_string,
            baud,
            id= None,
            blocking=True,
            callback=None,
            params = None):
    if self.state == 'disconnected':
        self.id = id
        if blocking:
            self._connect(connection_string, baud)
        else:
            connectThread = threading.Thread(target=self._connect, args=[connection_string, baud, callback, params, ])
            connectThread.start()
        return True
    else:
        return False

def disconnect (self):
    if self.state == 'connected':
        self.state = "disconnected"
        self.vehicle.mav.request_data_stream_send(
            self.vehicle.target_system, self.vehicle.target_component,
            mavutil.mavlink.MAV_DATA_STREAM_POSITION,
            10,
            0
        )
        self.stop_sending_telemetry_info()
        self.stop_sending_local_telemetry_info()
        self.vehicle.close()
        return True
    else:
        return False


# ====== ARM/DISARM ======

def _arm(self, callback=None, params=None):
    self.state = "arming"
    mode = 'GUIDED'
    # Get mode ID
    mode_id = self.vehicle.mode_mapping()[mode]
    self.vehicle.mav.set_mode_send(
        self.vehicle.target_system,
        mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
        mode_id)
    arm_msg = self.vehicle.recv_match(type='COMMAND_ACK', blocking=True, timeout=3)

    self.vehicle.mav.command_long_send(self.vehicle.target_system, self.vehicle.target_component,
                                       mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)
    self.vehicle.motors_armed_wait()
    self.state = "armed"
    if callback != None:
        if self.id == None:
            if params == None:
                callback()
            else:
                callback(params)
        else:
            if params == None:
                callback(self.id)
            else:
                callback(self.id, params)


def arm(self, blocking=True, callback=None, params=None):
    if self.state == 'connected':
        if blocking:
            self._arm()
        else:
            armThread = threading.Thread(target=self._arm, args=[callback, params])
            armThread.start()
        return True
    else:
        return False


# ====== TAKE OFF ======

def _takeOff(self, aTargetAltitude, callback=None, params=None):
    self.state = "takingOff"
    self.vehicle.mav.command_long_send(self.vehicle.target_system, self.vehicle.target_component,
                                       mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, aTargetAltitude)

    while True:
        msg = self.vehicle.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
        # print('meg ', msg)
        if msg:
            msg = msg.to_dict()
            alt = float(msg['relative_alt'] / 1000)
            if alt >= aTargetAltitude * 0.90:
                print("Reached target altitude")
                break
        time.sleep(2)

    self.state = "flying"
    if callback != None:
        if self.id == None:
            if params == None:
                callback()
            else:
                callback(params)
        else:
            if params == None:
                callback(self.id)
            else:
                callback(self.id, params)


def takeOff(self, aTargetAltitude, blocking=True, callback=None, params=None):
    if self.state == 'armed':
        if blocking:
            self._takeOff(aTargetAltitude)
        else:
            takeOffThread = threading.Thread(target=self._takeOff, args=[aTargetAltitude, callback, params])
            takeOffThread.start()
        return True
    else:
        return False

# ====== GO DOWN/LAND/RTL ======

def _goDown(self, mode, callback=None, params = None):

    # Get mode ID
    mode_id = self.vehicle.mode_mapping()[mode]
    self.vehicle.mav.set_mode_send(
        self.vehicle.target_system,
        mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
        mode_id)
    #arm_msg = self.vehicle.recv_match(type='COMMAND_ACK', blocking=True, timeout=3)
    #
    while True:
        msg = self.vehicle.recv_match(type='GLOBAL_POSITION_INT', blocking=False)
        if msg:
            msg = msg.to_dict()
            alt = float(msg['relative_alt'] / 1000)
            print (alt)
            if alt < 0.5:
                break
            time.sleep(2)

    self.vehicle.motors_disarmed_wait()
    self.state = "connected"
    if callback != None:
        print ('llamo al call back')
        if self.id == None:
            if params == None:
                callback()
            else:
                callback(params)
        else:
            if params == None:
                callback(self.id)
            else:
                callback(self.id, params)


def RTL (self, blocking=True, callback=None, params = None):
    if self.state == 'flying':
        self.state = 'returning'
        if blocking:
            self._goDown('RTL')
        else:
            goingDownThread = threading.Thread(target=self._goDown, args=['RTL', callback, params])
            goingDownThread.start()
        return True
    else:
        return False

def Land (self, blocking=True, callback=None, params = None):
    if self.state == 'flying':
        self.state = 'landing'
        if blocking:
            self._goDown('LAND')
        else:
            print ('pongo en marcha el thread para land')
            goingDownThread = threading.Thread(target=self._goDown, args=['LAND', callback, params])
            goingDownThread.start()
        return True
    else:
        return False

# ====== TELEMETRY ======

def _send_telemetry_info(self, process_telemetry_info):
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

            vx =  float(msg['vx'])
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

            if self.id == None:
                process_telemetry_info (telemetry_info)
            else:
                process_telemetry_info (self.id, telemetry_info)
        time.sleep(1)


def send_telemetry_info(self, process_telemetry_info):
    telemetryThread = threading.Thread(target=self._send_telemetry_info, args=[process_telemetry_info,])
    telemetryThread.start()

def stop_sending_telemetry_info(self):
    self.sendTelemetryInfo = False


# ====== NAVGIATION ======
def _prepare_command(self, velocity_x, velocity_y, velocity_z, bodyRef=False):
    """
    Move vehicle in direction based on specified velocity vectors.
    """
    print('3 vamos ', bodyRef)
    if bodyRef:
        print('body')
        msg = mavutil.mavlink.MAVLink_set_position_target_local_ned_message(
            10,  # time_boot_ms (not used)
            self.vehicle.target_system,
            self.vehicle.target_component,
            mavutil.mavlink.MAV_FRAME_BODY_OFFSET_NED,  # frame
            0b0000111111000111,  # type_mask (only speeds enabled)
            0,
            0,
            0,  # x, y, z positions (not used)
            velocity_x,
            velocity_y,
            velocity_z,  # x, y, z velocity in m/s
            0,
            0,
            0,  # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
            0,
            0,
        )  # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)

    else:
        print('local ned')
        msg = mavutil.mavlink.MAVLink_set_position_target_global_int_message(
            10,  # time_boot_ms (not used)
            self.vehicle.target_system,
            self.vehicle.target_component,
            mavutil.mavlink.MAV_FRAME_LOCAL_NED,  # frame
            0b0000111111000111,  # type_mask (only speeds enabled)
            0,
            0,
            0,  # x, y, z positions (not used)
            velocity_x,
            velocity_y,
            velocity_z,  # x, y, z velocity in m/s
            0,
            0,
            0,  # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
            0,
            0,
        )  # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)

    return msg


def _startGo(self):
    self.cmd = self._prepare_command(0, 0, 0)
    while self.going:
        self.vehicle.mav.send(self.cmd)
        time.sleep(1)
    self.cmd = self._prepare_command(0, 0, 0)
    time.sleep(1)


def startGo(self):
    if self.state == 'flying':
        self.going = True
        startGoThread = threading.Thread(target=self._startGo)
        startGoThread.start()


def stopGo(self):
    self.going = False


def changeNavSpeed(self, speed):
    self.navSpeed = speed
    self.go(self.direction)


def go(self, direction):
    speed = self.navSpeed
    self.direction = direction
    if self.going:
        if direction == "North":
            self.cmd = self._prepare_command(speed, 0, 0)  # NORTH
        if direction == "South":
            self.cmd = self._prepare_command(-speed, 0, 0)  # SOUTH
        if direction == "East":
            self.cmd = self._prepare_command(0, speed, 0)  # EAST
        if direction == "West":
            self.cmd = self._prepare_command(0, -speed, 0)  # WEST
        if direction == "NorthWest":
            self.cmd = self._prepare_command(speed, -speed, 0)  # NORTHWEST
        if direction == "NorthEast":
            self.cmd = self._prepare_command(speed, speed, 0)  # NORTHEST
        if direction == "SouthWest":
            self.cmd = self._prepare_command(-speed, -speed, 0)  # SOUTHWEST
        if direction == "SouthEast":
            self.cmd = self._prepare_command(-speed, speed, 0)  # SOUTHEST
        if direction == "Stop":
            self.cmd = self._prepare_command(0, 0, 0)  # STOP
        if direction == "Forward":
            self.cmd = self._prepare_command(speed, 0, 0, bodyRef=True)
        if direction == "Back":
            self.cmd = self._prepare_command(-speed, 0, 0, bodyRef=True)
        if direction == "Left":
            self.cmd = self._prepare_command(0, speed, 0, bodyRef=True)
        if direction == "Right":
            self.cmd = self._prepare_command(0, -speed, 0, 0, bodyRef=True)
        if direction == "Up":
            self.cmd = self._prepare_command(0, 0, -speed, bodyRef=True)
        if direction == "Down":
            self.cmd = self._prepare_command(0, 0, speed, bodyRef=True)




