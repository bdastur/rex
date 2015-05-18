'''
REX UT.
'''

import unittest
import sys
sys.path.append("../")
import rex


class REXUT(unittest.TestCase):
    '''
    REX unit tests.
    '''
    def test_reformat_pattern(self):
        '''
        test reformat_pattern API.
        '''
        print("test_reformat_pattern")
        test_pattern = "(w:<name>) is (w:<attribute>)"
        matchpat = "(?P<name>\w+) is (?P<attribute>\w+)"
        rexpat = rex.reformat_pattern(test_pattern)
        self.failUnless(rexpat == matchpat)

        test_pattern = "(d:<number>),testst_-(w:<name>), xyz(W:<attr>),(<foo>)"
        matchpat = "(?P<number>\d+),testst_-(?P<name>\w+), " \
            "xyz(?P<attr>\W+),(?P<foo>.*)"

        rexpat = rex.reformat_pattern(test_pattern)
        self.failUnless(rexpat == matchpat)

        test_pattern = "(d:<number>), IP: (ip:<ipaddr>),.*"
        rexpat = rex.reformat_pattern(test_pattern)
        print("rexpat: ", rexpat)

    def test_match_string(self):
        '''
        test match string.
        '''
        print("test_match_string")

        teststr = "Mary had 8 Lambs, and they were white as snow."
        testpat = "(w:<name>) had (d:<num>) Lambs"
        rex.match_string(testpat, teststr)

    def test_match_mac(self):
        '''
        Test matching mac address pattern.
        '''
        macstr = "Link encap:Ethernet  HWaddr 00:50:56:BB:1B:BE"
        testpat = ".*HWaddr (mac:<macaddr>)"
        rexobj = rex.match_string(testpat, macstr)
        val = rex.get_match_value(rexobj, "macaddr", 0)
        self.failUnless(val == "00:50:56:BB:1B:BE")

    def test_match_file(self):
        '''
        test match_file(pattern, filename)
        '''
        print("test match file")
        # [2014-12-10:9095 ERROR]IP: 172.22.1983, MAC:44:aa:ea:9d:43:23, \
        # INT:eth0,
        # testpattern = "[(d:<year>)\-(d:<month>)\-(d:<day>) (w:<loglevel>)]" \
        #    "IP: (ip:<ipaddr>).*"
        # [2014-12-10:9088 INFO]Mary had 8 Lambs, and they \
        # all where white as Sn0w.

        testpattern = "\[(d:<year>)-(d:<month>)-(d:<day>)" \
            ":(\d+) (w:<level>)\](w:<name>) had (d:<num>) Lambs.*"
        testfile = "test_data/simple.txt"
        rexobj = rex.match_file(testpattern, testfile)
        rex.dump_rexobj_results(rexobj)

    def test_get_dict_from_string(self):
        '''
        Test the get_dict_from_string() API.
        '''
        test_string = "Chassis:  " + "\n" + \
            "Serial Number:  FCH1278Ad" + "\n" + \
            "Product Name:  UCS C240 M3S " + "\n" + \
            "PID : UCS-C240-M3S" + "\n" \
            "UUID: 8C88d92232111DK-CEDI8987D-U89" + "\n" + \
            "Locator LED: off" + "\n"

        rexdict = rex.get_dict_from_string(test_string)
        self.failUnless(rexdict['serial_number'] == "FCH1278Ad")
        self.failUnless(rexdict['product_name'] == "UCS C240 M3S")

    def test_get_dictlist_from_string(self):
        '''
        Test the get_dictlist_from_string() API.
        '''
        test_string = \
            """
            Physical Drive Number 21:
                Controller: SLOT-4
                Health: Good
                Status: Unconfigured Good
                Manufacturer: ATA
                Model: ST91000640NS
                Predictive Failure Count: 0
                Drive Firmware: CC03
                Coerced Size: 952720 MB
                Type: HDD
            Physical Drive Number 22:
                Controller: SLOT-4
                Health: Good
                Status: Unconfigured Good
                Manufacturer: ATA
                Model: ST91000640NS
                Predictive Failure Count: 0
                Drive Firmware: CC03
                Coerced Size: 952720 MB
                Type: HDD
            """
        dictlist = rex.get_dictlist_from_string(test_string,
                                                "Physical Drive Number")
        print("dictlist: ", dictlist)








