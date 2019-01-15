#! *-* coding: utf-8 *-*
#!/usr/bin/env python
"""
Test for Velodyne voltage temperature class.

@author vincent cheung
@file volt_temp_test.py
"""
import unittest
import json

from volt_temp import Volt_temp

class Volt_temp_Test(unittest.TestCase):
    """
    Unit test class for `volt_temp`
    TODO: Not yet finish.
    """
    def setUp(self):
        # 每个测试用例执行之前做操作
        self.volt_temp = Volt_temp()
        self.js = json.load(open('example_diag.json'))['volt_temp']
        #print ('\n Using example_diag.json: {}\n'.format(self.js))

    @classmethod
    def tearDownClass(self):
         print('Test finish')

    @classmethod
    def setUpClass(self):
        self.js = json.load(open('example_diag.json'))['volt_temp']
        print ('\nUsing `example_diag.json` : {}\n'.format(self.js))
        print('Test setup')

    def test_scale_parm(self):
        self.assertEqual(2.5/4096, self.volt_temp.scale_1x_vref)
        self.assertEqual(5.0/4096, self.volt_temp.scale_2x_vref)

    def test_hdltop_volts_to_hv(self):
        self.assertEqual(0.0, self.volt_temp.hdltop_volts_to_hv(5))
        self.assertEqual(101.0, self.volt_temp.hdltop_volts_to_hv(6))

    def test_lm20_volts_to_degCel(self):
        self.assertEqual(-0.0018359481264269562, self.volt_temp.lm20_volts_to_degCel(1.8639))

    def test_acs17_volts_to_amps(self):
        self.assertEqual(0, self.volt_temp.acs17_volts_to_amps(2.5))
        self.assertEqual(25, self.volt_temp.acs17_volts_to_amps(5))

    def test_scale_volt_temp(self):
        #TODO: Not yet finish
        self.volt_temp.scale_volt_temp(self.js)
        self.assertEqual(11.802978515625, self.js['bot']['pwr_v_in'])

    def test_parse(self):
        #TODO: Not yet finish
        self.volt_temp.parse(self.js)
        self.assertEqual(11.802978515625, self.js['bot']['pwr_v_in'])

if __name__ == '__main__':
    unittest.main()#运行所有的测试用例