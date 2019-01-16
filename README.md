# Velodyne LiDAR voltage logger
It will logs the voltages of Velodyne LiDARs at **`./data/logs/velo_volt-%Y%m%d%H%M.log`** with format like `2019-01-15 17:29:08,284 - rc_velo_vol.py[line:31] - INFO: Lidar:201 voltage:11.802978515625`.

> Note: Users may need to change the url Velodyne LiDARs by modifying `url_1` and `url_2`.

## Usage
```shell
python rc_velo_vol.py
```
### Test Mode Usage
```shell
# On one terminal and in this folder
python3 -m http.server
# On another terminal and in this folder
python rc_velo_vol.py --mode test
```

## Requirements
```txt
requests
```
```shell
pip install requests
```

### TODO
- [x] A simple voltage viewer    
- [] Log other diag parameters    
- [] Support more than two LiDARs