#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from tf2_ros import StaticTransformBroadcaster
import math

class LivoxFramePublisher(Node):
    def __init__(self):
        super().__init__('mid360_front_frame_publisher')

        # Create static transform broadcaster
        self.broadcaster = StaticTransformBroadcaster(self)

        # Create transform from base_link to mid360_front
        transform = TransformStamped()
        transform.header.stamp = self.get_clock().now().to_msg()
        transform.header.frame_id = "base_link"
        transform.child_frame_id = "mid360_front"
        
        # Set translation (sensor position: x=0.15, z=0.35 from vehicle config)
        transform.transform.translation.x = 0.15
        transform.transform.translation.y = 0.0
        transform.transform.translation.z = 0.35
        
        # Set rotation (no rotation)
        transform.transform.rotation.x = 0.0
        transform.transform.rotation.y = 0.0
        transform.transform.rotation.z = 0.0
        transform.transform.rotation.w = 1.0
        
        # Send the transform
        self.broadcaster.sendTransform(transform)
        
        self.get_logger().info('Published static transform: base_link -> mid360_front')
        
        # Keep node alive
        # The transform is static, so we don't need to publish it repeatedly


def main(args=None):
    rclpy.init(args=args)
    node = LivoxFramePublisher()
    
    try:
        # Spin once to publish the transform, then shutdown
        rclpy.spin_once(node, timeout_sec=1.0)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()