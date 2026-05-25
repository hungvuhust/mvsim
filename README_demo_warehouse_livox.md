# Demo: Warehouse + Livox LiDAR

MVSim simulation — warehouse environment with Livox LiDAR sensor, joystick teleop.

---

## Requirements

- ROS 2 Humble
- Ubuntu 22.04

---

## Clone Source

```bash
git clone https://github.com/hungvuhust/mvsim.git --recursive
cd mvsim
```

Nếu đã clone rồi mà chưa có submodule:

```bash
git submodule update --init --recursive
```

---

## Install Dependencies

```bash
bash install_depend.sh
```

---

## Build

```bash
cd ~/mvsim
colcon build --symlink-install
source install/setup.bash
```

---

## Run

```bash
bash run.sh
```

Simulator opens. Use joystick to drive robot:
- Hold **LB** (button 6) to enable control
- **Left stick Y** → forward/backward
- **Left stick X** → turn
- Hold **RB** (button 5) for turbo speed

---

## Launch Arguments

| Argument | Default | Description |
|---|---|---|
| `world_file` | `demo_warehouse_livox.world.xml` | World file path |
| `headless` | `False` | Run without GUI |
| `do_fake_localization` | `False` | Publish fake `map→odom` TF |
| `publish_tf_odom2baselink` | `False` | Publish `odom→base_link` TF |

Example with custom args:

```bash
ros2 launch mvsim demo_warehouse_livox.launch.py headless:=True
```

---

## Topics

| Topic | Type | Description |
|---|---|---|
| `/cmd_vel` | `geometry_msgs/Twist` | Robot velocity command |
| `/livox/lidar` | `sensor_msgs/PointCloud2` | Livox LiDAR pointcloud |
| `/livox/imu` | `sensor_msgs/Imu` | IMU data |

---

## TF Frames

```
map → odom → base_link → livox_frame
```

Static TF `base_link → livox_frame`: offset `(-0.07, 0, 0.337)`, rotated 180° around Y.
