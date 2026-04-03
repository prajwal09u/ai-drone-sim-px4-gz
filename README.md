# ai-drone-sim-px4-gz

Dockerized **PX4 SITL + Gazebo** simulation with a minimal **ROS 2** follower stack.

This project runs:
- PX4 SITL multicopter
- Gazebo (gz-sim) world with a simple moving target model
- ROS 2 nodes:
  - `vision_node`: detects a colored target in the camera stream (HSV threshold)
  - `follow_node`: sends MAVLink velocity setpoints to follow the target

## Requirements
- Docker + Docker Compose v2
- (Recommended) Linux host. On Windows/macOS you may need additional X/GUI setup.

## Quick start

### 1) Start simulation
```bash
docker compose up --build
```

### 2) (Optional) Open a shell in the ROS container
```bash
docker exec -it ai-drone-ros bash
```

## Notes / Troubleshooting
- This is a **starter sim** aimed at running end-to-end quickly.
- Offboard control in PX4 requires setpoints streaming; the follower sends setpoints continuously.
- If you don’t see images, check the camera topic and the bridge settings.

## Safety
Use simulation first. Do **not** fly real hardware with this code without adding proper failsafes.
