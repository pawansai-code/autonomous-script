#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from mavros_msgs.srv import CommandBool, SetMode
import time

class ArmDisarmNode(Node):
    def __init__(self):
        super().__init__("arm_disarm_node")
        
        # Create Service Clients for Mode and Arming
        self.arm_client = self.create_client(CommandBool, "/mavros/cmd/arming")
        self.mode_client = self.create_client(SetMode, "/mavros/set_mode")

    def set_mode(self, mode):
        self.get_logger().info(f"Changing mode to {mode}...")
        self.mode_client.wait_for_service()
        
        req = SetMode.Request()
        req.custom_mode = mode
        future = self.mode_client.call_async(req)
        
        # Wait for the drone to reply
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
        
        # Wait for the drone to reply
        rclpy.spin_until_future_complete(self, future)
        if future.result().success:
            self.get_logger().info(f"{action} successful!")
        else:
            self.get_logger().error(f"{action} failed.")

def main(args=None):
    rclpy.init(args=args)
    node = ArmDisarmNode()
    
    # Step 1: Change to a safe mode (AUTO.LOITER or GUIDED)
    node.set_mode("AUTO.LOITER")
    time.sleep(2)
    
    # Step 2: Arm the drone
    node.set_arm(True)
    
    # Step 3: Keep the motors spinning for 10 seconds
    node.get_logger().info("Waiting 10 seconds...")
    time.sleep(10)
    
    # Step 4: Disarm the drone
    node.set_arm(False)

    # Clean up and exit
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
