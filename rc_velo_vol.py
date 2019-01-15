#! *-* coding: utf-8 *-*
#!/usr/bin/env python
"""
A simple scraper for recording the power supply of velodyne LiDAR,
by getting the `diag.json` files.

@author vincent cheung
@file rc_velo_vol.py
"""
import argparse
import math
import time
import requests
import json
import logging
import os

from volt_temp import Volt_temp

url_1 = 'http://192.168.100.201/cgi/diag.json'
url_2 = 'http://192.168.100.202/cgi/diag.json'
## For test only
url_3 = 'http://127.0.0.1:8000/example_diag.json'
url_4 = 'http://127.0.0.1:8000/example_diag.json'

# Sleep a period after getting one diag, in seconds.
sleep_prd = 1.0

def volt_temp_logger(volts, lidar_id):
    """
    A simple level logger based on the voltages and lidar_id.
    """
    # Round the voltage into xx.xx
    volts = round(volts, 2)
    if volts >= 11.5 and volts <= 12.5:
        logger.info('Lidar:{} voltage:{}'.format(lidar_id, volts))
    elif volts >= 10.0 and volts < 11.5:
        logger.warning('Lidar:{} voltage:{}'.format(lidar_id, volts))
    elif volts >= 9.0 and volts < 10.0:
        logger.error('Lidar:{} voltage:{}'.format(lidar_id, volts))
    else:
        logger.critical('Lidar:{} voltage:{}'.format(lidar_id, volts))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Velodyne LiDAR voltage logger.')
    parser.add_argument('--num', type=int, help='Num of LiDARs', default=2)
    parser.add_argument('--mode', choices=['run', 'test'], default='run')
    parser.add_argument('--version', action='version', version='%(prog)s alpha 1.0')
    args = args = parser.parse_args()
    if args.mode == 'test':
        url_lidar_1 = url_3
        url_lidar_2 = url_4
    else:
        url_lidar_1 = url_1
        url_lidar_2 = url_2      
    """
    Define logger and logfile path
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    rq = time.strftime('velo_volt-%Y%m%d%H%M', time.localtime(time.time()))
    log_path = os.path.join(os.getcwd(), 'data', 'logs')
    log_name = os.path.join(log_path, rq + '.log')
    logfile = log_name
    # Check path exists or not
    if not os.path.exists(log_path):
        #os.makedirs(log_path, exists_ok=True)
        os.makedirs(log_path)
    fh = logging.FileHandler(logfile, mode='w')
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    volt_temp_parser = Volt_temp()
    while True:
        """
        Get the `diag.json` file periodically
        Parse and logs
        """
        req = requests.get(url_lidar_1, timeout=0.20)
        js = req.json()['volt_temp']
        volt_temp_parser.parse(js)
        volt_temp_logger(js['bot']['pwr_v_in'], 201)

        if args.num >= 2:
            #TODO: Not yet support more than two LiDARs
            req = requests.get(url_lidar_2, timeout=0.20)
            js = req.json()['volt_temp']
            volt_temp_parser.parse(js)
            volt_temp_logger(js['bot']['pwr_v_in'], 202)
        time.sleep(sleep_prd)


