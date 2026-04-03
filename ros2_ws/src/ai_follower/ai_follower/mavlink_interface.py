import time
from pymavlink import mavutil

class MavlinkInterface:
    def __init__(self, udp_in="udp:127.0.0.1:14540"):
        self.master = mavutil.mavlink_connection(udp_in)
        self.master.wait_heartbeat(timeout=30)
        self.sysid = self.master.target_system
        self.compid = self.master.target_component

    def send_body_velocity(self, vx, vy, vz, yaw_rate):
        now_ms = int(time.time() * 1000)
        type_mask = 0b0000111111000111
        self.master.mav.set_position_target_local_ned_send(
            now_ms,
            self.sysid,
            self.compid,
            mavutil.mavlink.MAV_FRAME_BODY_NED,
            type_mask,
            0, 0, 0,
            vx, vy, vz,
            0, 0, 0,
            0,
            yaw_rate
        )
