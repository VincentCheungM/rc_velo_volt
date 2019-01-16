#! *-* coding: utf-8 *-*
#!/usr/bin/env python
"""
A simple flask based webviewer for visualization of
LiDAR temperatures.

Usage: python app.py -f xxx.log

@author vincent cheung
"""
from __future__ import print_function
import argparse
import re
import sys

from flask import Flask
from flask import Markup
from flask import Flask
from flask import render_template

app = Flask(__name__)

class Sensor_data(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Sensor_datasets(object):
    """
    A simple class for holding datasets for chart.js on Ninja2 template.
    """
    def __init__(self, legend, values, labels):
        self.legend = legend # define legend
        self.values = values # raw y value
        self.labels = labels # raw x value
        self.pair = []# For holding sensor_data

@app.route("/")
def line_chart():
    global s_datasets_dicts, x
    if len(s_datasets_dicts) == 1:
        return render_template('line_chart.html', values1=s_datasets_dicts.values()[0].values, \
        legend1=s_datasets_dicts.values()[0].legend, labels = x)
    else:
        # return render_template('line_chart.html', values1=s_datasets_dicts.values()[0].pair, \
        # legend1=s_datasets_dicts.values()[0].legend, labels = x, \
        # values2=s_datasets_dicts.values()[1].pair, legend2=s_datasets_dicts.values()[1].legend)
        return render_template('line_chart.html', values1=s_datasets_dicts.values()[0].values, \
        legend1=s_datasets_dicts.values()[0].legend, labels = x, \
        values2=s_datasets_dicts.values()[1].values, legend2=s_datasets_dicts.values()[1].legend)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Webserver for LiDAR temperature logs.')
    parser.add_argument('-f', '--file', required=True, type=str, help='The path to LiDAR temperature logs.')
    parser.add_argument('-n', '--num', type=int, help='Num of LiDARs', default=2)
    args = parser.parse_args()
    s_datasets_dicts = {}
    x = [] # time stamp
    """
    TODO: Not yet clear about the logic.
    """
    s_datasets_dicts['201'] = Sensor_datasets(legend='{} {} {}'.format('LiDAR','201','voltage'), \
        values=[], labels=[])
    if args.num >=2:
        s_datasets_dicts['202'] = Sensor_datasets(legend='{} {} {}'.format('LiDAR','202','voltage'), \
            values=[], labels=[])
    with open(args.file) as f:
        lines = f.read().splitlines()
        """
        Split pattern: date, time, src, log_level, sensor_type, sensor_id, property, value

        In this case, property-value is `voltage`.
        """
        pattern = re.compile(r'([0-9]+-[0-9]+-[0-9]+)\s([0-9]+:[0-9]+:[0-9]+,[0-9]+)\s(-.*-)\s(.*?):\s(.*?):([0-9]+)\s(.*?):([0-9]+\.[0-9]*)')
        for l in lines:
            ret = pattern.search(l)
            date = ret.group(1)
            time = ret.group(2).replace(',', '.')
            log_level = ret.group(4)
            s_type = ret.group(5)
            s_id = ret.group(6)
            s_p = ret.group(7)
            s_v = ret.group(8)
            ## In case there are more ID.
            if s_id not in s_datasets_dicts:
                s_datasets_dicts[s_id] = Sensor_datasets(legend='{} {} {}'.format(s_type,s_id,s_p), \
                    values=[], labels=[])
            x.append(date+' '+time)
            # s_datasets_dicts[s_id].pair.append(Sensor_data(date+' '+time, s_v))
            ## Adding blank gaps to the other line
            if args.num >=2:
                if s_id == '201':
                    s_datasets_dicts['201'].values.append(s_v)
                    s_datasets_dicts['202'].values.append(' ')
                elif s_id == '202':
                    s_datasets_dicts['202'].values.append(s_v)
                    s_datasets_dicts['201'].values.append(' ')
    app.run(host='0.0.0.0', port=5001)
