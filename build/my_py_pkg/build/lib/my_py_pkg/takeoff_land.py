#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from mavros_msgs.srv import CommandBool, SetMode
import time

class TakeoffLandNode(Node):
    def __init__(self):
        super().__init__("takeoff_land_node")
        
        # Service Clients
        self.arm_client = self.create_client(CommandBool, "/mavros/cmd/arming")
        self.mode_client = self.create_client(SetMode, "/mavros/set_mode")

    def set_mode(self, mode):
        self.get_logger().info(f"Changing mode to {mode}...")
        self.mode_client.wait_for_service()
        
        req = SetMode.Request()
        req.custom_mode = mode
        future = self.mode_client.call_async(req)
        rclpy.spin_until_future_complete(self, future)
        if future.result().mode_sent:
            self.get_logger().info("Mode change successful!")
        else:
            self.get_logger().error("Mode change failed.")

    def set_arm(self, arm_state):
        action = "ARMING" if arm_state else "DISARMING"
        self.get_logger().info(f"{action} drone...")
        self.arm_client.wait_for_service()
        
        req = CommandBool.Request()
        req.value = arm_state
        future = self.arm_client.call_async(req)
        rclpy.spin_until_future_complete(self, future)

def main(args=None):
    rclpy.init(args=args)
    node = TakeoffLandNode()
    
    # 1. Prepare for flight
    node.set_mode("AUTO.LOITER")
    time.sleep(2)
    
    # 2. Arm the drone
    node.set_arm(True)
    time.sleep(2)
    
    # 3. Takeoff!
    node.get_logger().info("Initiating Takeoff sequence...")
    node.set_mode("AUTO.TAKEOFF")
    
    # Wait for the drone to reach the sky and hover
    node.get_logger().info("Hovering and enjoying the view for 15 seconds...")
    time.sleep(15)
    
    # 4. Land back on the ground
    node.get_logger().info("Initiating Landing sequence...")
    node.set_mode("AUTO.LAND")
    
    # Wait for the drone to touch down
    time.sleep(15)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
