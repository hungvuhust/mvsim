# Generic ROS2 launch file
# Read: https://mvsimulator.readthedocs.io/en/latest/mvsim_node.html

from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
import os


def generate_launch_description():

    # args that can be set from the command line or a default will be used
    world_file_launch_arg = DeclareLaunchArgument(
        "world_file", description='Path to the *.world.xml file to load', default_value='mvsim_tutorial/demo_warehouse_livox.world.xml')

    headless_launch_arg = DeclareLaunchArgument(
        "headless", default_value='False')

    do_fake_localization_arg = DeclareLaunchArgument(
        "do_fake_localization", default_value='False', description='publish fake identity tf "map" -> "odom"')

    publish_tf_odom2baselink_arg = DeclareLaunchArgument(
        "publish_tf_odom2baselink", default_value='False', description='publish tf "odom" -> "base_link"')

    force_publish_vehicle_namespace_arg = DeclareLaunchArgument(
        "force_publish_vehicle_namespace", default_value='False',
        description='Use vehicle name namespace even if there is only one vehicle')

    publish_log_topics_arg = DeclareLaunchArgument(
        "publish_log_topics", default_value='False',
        description='Publish every CSV-logger column as a std_msgs/Float64 topic per vehicle. '
                    'High-rate, disabled by default.')

    use_rviz_arg = DeclareLaunchArgument(
        'use_rviz', default_value='True',
        description='Whether to launch RViz2'
    )

    rviz_config_file_arg = DeclareLaunchArgument(
        'rviz_config_file', default_value='mvsim_tutorial/demo_warehouse_ros2.rviz',
        description='If use_rviz:="True", the configuration file for rviz'
    )

    mvsim_node = Node(
        package='mvsim',
        executable='mvsim_node',
        name='mvsim',
        output='screen',
        parameters=[
            {
                "world_file": LaunchConfiguration('world_file'),
                "headless": LaunchConfiguration('headless'),
                "do_fake_localization": LaunchConfiguration('do_fake_localization'),
                "publish_tf_odom2baselink": LaunchConfiguration('publish_tf_odom2baselink'),
                "force_publish_vehicle_namespace": LaunchConfiguration('force_publish_vehicle_namespace'),
                "publish_log_topics": LaunchConfiguration('publish_log_topics'),
                "simul_rate": 500.0,
            }]
    )

    rviz2_node = Node(
        condition=IfCondition(LaunchConfiguration('use_rviz')),
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=[] if LaunchConfiguration('rviz_config_file') == '' else [
                '-d', LaunchConfiguration('rviz_config_file')]
    )

    static_tf_base_to_livox = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='static_tf_base_link_to_livox_frame',
        arguments=['-0.07', '0', '0.337', '0',
                   '0', '3.14159265', 'base_link', 'livox_frame']
    )

    joy_node = Node(
        package='joy',
        executable='joy_node',
        name='joy_node',
        parameters=[{
            'deadzone': 0.1,
            'autorepeat_rate': 20.0,
        }]
    )

    teleop_twist_joy_node = Node(
        package='teleop_twist_joy',
        executable='teleop_node',
        name='teleop_twist_joy',
        parameters=[{
            'axis_linear.x': 1,
            'axis_angular.yaw': 0,
            'scale_linear.x': 1.0,
            'scale_angular.yaw': 1.0,
            'enable_button': 6,
            'enable_turbo_button': 5,
            'scale_linear_turbo.x': 2.0,
            'scale_angular_turbo.yaw': 2.0,
        }],
        remappings=[
            ('cmd_vel', '/cmd_vel'),
        ]
    )

    return LaunchDescription([
        world_file_launch_arg,
        headless_launch_arg,
        do_fake_localization_arg,
        publish_tf_odom2baselink_arg,
        force_publish_vehicle_namespace_arg,
        publish_log_topics_arg,
        use_rviz_arg,
        rviz_config_file_arg,
        mvsim_node,
        # rviz2_node,
        # static_tf_base_to_livox,
        joy_node,
        teleop_twist_joy_node,
    ])
