#! *-* coding: utf-8 *-*
#!/usr/bin/env python
"""
Velodyne voltage temperature class, modify from Velodyne `js/diag.js`.

@author vincent cheung
@file volt_temp.py
"""
import math

class Volt_temp(object):
    """
    Velodyne voltage temperature class, modify from Velodyne `js/diag.js`.
    """

    def __init__(self):
        self.scale_2x_vref = 5.0/4096
        self.scale_1x_vref = 2.5/4096
    
    def hdltop_volts_to_hv(self, volts):
        return 101.0 * (volts - 5.0)

    def lm20_volts_to_degCel(self, volts):
        return -1481.96 + math.sqrt(2.1962E6 + (1.8639 - volts)/3.88E-6)
    
    def acs17_volts_to_amps(self, volts):
        return 10.0 * (volts - 2.5)
    
    def parse(self, volt_temp):
        """
        Parse the raw json data into resonable data.
        """
        self.scale_volt_temp(volt_temp)
    
    def scale_volt_temp(self, volt_temp):
        """
        Scale the raw json data into resonable data.
        """
        for sample in volt_temp['top']:
            volt_temp['top'][sample] *= self.scale_2x_vref

        for sample in volt_temp['bot']:
            volt_temp['bot'][sample] *= self.scale_2x_vref

        volt_temp['top']['hv'] = self.hdltop_volts_to_hv(volt_temp['top']['hv'])
        volt_temp['top']['lm20_temp'] = self.lm20_volts_to_degCel(volt_temp['top']['lm20_temp'])
        volt_temp['top']['pwr_5v'] *= 2.0
        volt_temp['top']['pwr_5v_raw'] *= 2.0
        
        volt_temp['bot']['i_out'] = self.acs17_volts_to_amps(volt_temp['bot']['i_out'])
        volt_temp['bot']['lm20_temp'] = self.lm20_volts_to_degCel(volt_temp['bot']['lm20_temp'])
        volt_temp['bot']['pwr_5v'] *= 2.0
        volt_temp['bot']['pwr_v_in'] *= 11.0

if __name__ == '__main__':
    """
    Simple unit test.
    """
    print ('hello')