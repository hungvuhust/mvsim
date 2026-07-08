#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu, PointCloud2

class TopicRemapper(Node):
    def __init__(self):
        super().__init__('topic_remapper')
        
        # IMU remap
        self.imu_sub = self.create_subscription(
            Imu,
            '/imu',
            self.imu_callback,
            10
        )
        self.imu_pub = self.create_publisher(
            Imu,
            '/sensors/lidar/mid360_front/imu',
            10
        )
        
        # Lidar remap
        self.lidar_sub = self.create_subscription(
            PointCloud2,
            '/lidar_points',
            self.lidar_callback,
            10
        )
        self.lidar_pub = self.create_publisher(
            PointCloud2,
            '/sensors/lidar/mid360_front/pointcloud',
            10
        )

        self.get_logger().info('Topic remapper started: /imu -> /sensors/lidar/mid360_front/imu, /lidar_points -> /sensors/lidar/mid360_front/pointcloud')
    
    def imu_callback(self, msg):
        self.imu_pub.publish(msg)
    
    def lidar_callback(self, msg):
        self.lidar_pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = TopicRemapper()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()