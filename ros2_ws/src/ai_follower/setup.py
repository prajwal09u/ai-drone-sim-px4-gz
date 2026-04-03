from setuptools import setup

package_name = 'ai_follower'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/sim_follow.launch.py']),
        ('share/' + package_name + '/config', ['config/params.yaml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='you',
    maintainer_email='you@example.com',
    description='ROS 2 follower demo for PX4 SITL using MAVLink + OpenCV',
    license='MIT',
    entry_points={
        'console_scripts': [
            'vision_node = ai_follower.vision_node:main',
            'follow_node = ai_follower.follow_node:main',
        ],
    },
)
