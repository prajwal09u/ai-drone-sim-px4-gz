from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='ai_follower',
            executable='vision_node',
            name='vision_node',
            output='screen',
            parameters=['/ros2_ws/src/ai_follower/config/params.yaml'],
        ),
        Node(
            package='ai_follower',
            executable='follow_node',
            name='follow_node',
            output='screen',
            parameters=['/ros2_ws/src/ai_follower/config/params.yaml'],
        ),
    ])
