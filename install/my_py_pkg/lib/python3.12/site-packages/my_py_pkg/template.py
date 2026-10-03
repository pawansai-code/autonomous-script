#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

class MyCustomNode(Node):   #modify name 
    def _init_(self):
        super()._init_("node_name")     #modify name

def main(args=Node):
    rclpy.init(args=args)
    node = MyCustomNode()   #modify name
    rclpy.spin(node)
    rclpy.shutdown()


if _name_ == "_main_":
    main()