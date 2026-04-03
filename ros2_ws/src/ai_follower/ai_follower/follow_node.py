import time
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray

from .mavlink_interface import MavlinkInterface

class FollowNode(Node):
    def __init__(self):
        super().__init__("follow_node")
        self.declare_parameter("mavlink_udp", "udp:127.0.0.1:14540")
        self.declare_parameter("setpoint_rate_hz", 20.0)
        self.declare_parameter("k_yaw", 1.2)
        self.declare_parameter("k_fwd", 1.0)
        self.declare_parameter("k_z", 0.6)
        self.declare_parameter("target_area", 0.015)
        self.declare_parameter("max_vx", 2.0)
        self.declare_parameter("max_vz", 1.0)
        self.declare_parameter("max_yaw_rate", 1.2)

        self.obs = None
        self.last_obs_t = 0.0

        udp = self.get_parameter("mavlink_udp").value
        self.mav = MavlinkInterface(udp_in=udp)

        self.sub = self.create_subscription(Float32MultiArray, "/target/obs", self.cb_obs, 10)
        rate = float(self.get_parameter("setpoint_rate_hz").value)
        self.timer = self.create_timer(1.0/rate, self.tick)

        self.get_logger().info("FollowNode running (sends body velocity setpoints over MAVLink)")

    def cb_obs(self, msg: Float32MultiArray):
        if len(msg.data) < 3:
            return
        self.obs = (float(msg.data[0]), float(msg.data[1]), float(msg.data[2]))
        self.last_obs_t = time.time()

    def clip(self, v, m):
        return max(-m, min(m, v))

    def tick(self):
        if self.obs is None or (time.time() - self.last_obs_t) > 0.5:
            self.mav.send_body_velocity(0.0, 0.0, 0.0, 0.0)
            return

        cx, cy, area = self.obs
        k_yaw = float(self.get_parameter("k_yaw").value)
        k_fwd = float(self.get_parameter("k_fwd").value)
        k_z = float(self.get_parameter("k_z").value)
        target_area = float(self.get_parameter("target_area").value)

        max_vx = float(self.get_parameter("max_vx").value)
        max_vz = float(self.get_parameter("max_vz").value)
        max_yaw = float(self.get_parameter("max_yaw_rate").value)

        yaw_rate = self.clip(-k_yaw * cx, max_yaw)
        vx = self.clip(k_fwd * (target_area - area), max_vx)
        vz = self.clip(k_z * (cy), max_vz)

        self.mav.send_body_velocity(vx, 0.0, vz, yaw_rate)


def main():
    rclpy.init()
    node = FollowNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
