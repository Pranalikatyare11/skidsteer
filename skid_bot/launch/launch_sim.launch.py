#!/usr/bin/env python3

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, Command
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue
from ament_index_python.packages import get_package_share_directory
import os

simulator_pkg = 'skid_bot'


# rviz_config_file = os.path.join(get_package_share_directory(simulator_pkg), 'rviz', '3DRviz.rviz')


def generate_launch_description():

    pkg_share = FindPackageShare("skid_bot")

    default_world = PathJoinSubstitution([
        pkg_share,
        "cpr_inspection",
        "model.world"
    ])

    world_file = LaunchConfiguration("world")

    xacro_file = PathJoinSubstitution([
        pkg_share,
        "description",
        "robot.urdf.xacro"
    ])

    robot_description = ParameterValue(
        Command(['xacro ', xacro_file]),
        value_type=str
    )

   
    rsp = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{
            "robot_description": robot_description,
            "use_sim_time": True,
        }],
        output="screen"
    )

  
    gzserver = ExecuteProcess(
        cmd=[
            "env",
            "GAZEBO_MODEL_DATABASE_URI=",
            "gzserver",
            "-s", "libgazebo_ros_init.so",
            "-s", "libgazebo_ros_factory.so",
            world_file
        ],
        output="screen"
    )
    gzclient = ExecuteProcess(
        cmd=[
            "env",
            "GAZEBO_MODEL_DATABASE_URI=",
            "gzclient"
        ],
        output="screen"
    )

    spawn = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=[
            "-topic", "/robot_description",
            "-entity", "skid_bot"
        ],
        output="screen"
    )

    teleop_node = Node(
        package='teleop_twist_keyboard',
        executable='teleop_twist_keyboard',
        name='teleop_keyboard',
        output='screen',
        prefix='xterm -e',
        parameters=[{'use_sim_time': True}]
    )


    return LaunchDescription([
        DeclareLaunchArgument(
            "world",
            default_value=default_world,
            description="Full path to the world file"
        ),
        rsp,
        gzserver,
        gzclient,
        spawn,

        teleop_node, 
    ])



