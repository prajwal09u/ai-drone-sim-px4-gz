# ai-drone-sim-px4-gz

Dockerized **PX4 SITL + Gazebo** simulation starter with a minimal **ROS 2** follower stack.

## Status (important)
This repository is a **starter scaffold**. On **macOS (especially Apple Silicon M1/M2/M3)**, Gazebo GUI/rendering and PX4 sim toolchains inside Docker are frequently problematic.

This repo is updated to:
- run **headless by default**
- force **linux/amd64** containers on Apple Silicon (Docker Desktop emulation)
- build PX4 SITL inside the container (avoids missing/private images)

## Requirements
- Docker Desktop for Mac

## Quick start (macOS M1/M2/M3)

1) Open Docker Desktop

2) In the project folder, run:

```
docker compose up --build
```

## Notes
- If you downloaded an older ZIP, it may still reference a missing image. Prefer cloning or re-downloading from the repo `main` branch.
- If you want a fully working Gazebo world + camera pipeline on macOS, the most reliable approach is to run Gazebo/PX4 natively on Ubuntu (or in a Linux VM). This repo can be adapted for that once we confirm your target.
