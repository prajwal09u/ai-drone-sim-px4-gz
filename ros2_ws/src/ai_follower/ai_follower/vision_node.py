import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import Float32MultiArray

import numpy as np
import cv2

from cv_bridge import CvBridge

class VisionNode(Node):
    def __init__(self):
        super().__init__("vision_node")
        self.declare_parameter("image_topic", "/camera/image_raw")
        self.declare_parameter("target_hsv_low", [0, 140, 80])
        self.declare_parameter("target_hsv_high", [10, 255, 255])
        self.declare_parameter("min_area", 300)

        self.image_topic = self.get_parameter("image_topic").value
        low = self.get_parameter("target_hsv_low").value
        high = self.get_parameter("target_hsv_high").value
        self.hsv_low = np.array(low, dtype=np.uint8)
        self.hsv_high = np.array(high, dtype=np.uint8)
        self.min_area = int(self.get_parameter("min_area").value)

        self.pub = self.create_publisher(Float32MultiArray, "/target/obs", 10)
        self.sub = self.create_subscription(Image, self.image_topic, self.cb, 10)
        self.bridge = CvBridge()
        self.get_logger().info(f"VisionNode subscribed to {self.image_topic}")

    def cb(self, msg: Image):
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
        h, w = frame.shape[:2]

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.hsv_low, self.hsv_high)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not cnts:
            return
        c = max(cnts, key=cv2.contourArea)
        area = cv2.contourArea(c)
        if area < self.min_area:
            return

        M = cv2.moments(c)
        if M["m00"] <= 1e-6:
            return
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])

        cx_norm = (2.0 * cx / max(1, w)) - 1.0
        cy_norm = (2.0 * cy / max(1, h)) - 1.0
        area_norm = float(np.clip(area / float(w*h), 0.0, 1.0))

        out = Float32MultiArray()
        out.data = [float(cx_norm), float(cy_norm), float(area_norm)]
        self.pub.publish(out)


def main():
    rclpy.init()
    node = VisionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
