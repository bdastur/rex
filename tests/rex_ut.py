'''
REX UT.
'''

import unittest
import sys
sys.path.append("../")
import rex
import re
import pprint


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

    def test_match_ipaddr(self):
        '''
        Match ipaddr pattern
        '''
        teststring = "13 06:25:06 m001d haproxy[37217]: 10.163.41.1:55238 "
        pattern = ".* (ip:<ipaddr>):(d:<port>).*"

        rexpat = rex.reformat_pattern(pattern)
        print "REXPAT: ", rexpat

        mobj = re.match(rexpat, teststring)
        if mobj:
            print "Matched: ", mobj.group(0)
            print "ipaddr: ", mobj.group('ipaddr')
            print "port: ", mobj.group('port')

    def test_match_ipaddr_invalid(self):
        '''
        Match: invalid ipaddr pattern
        '''
        teststring = "13 06:25:06 m001d haproxy[37217]: 310.41.1.4344:43238 xy"
        pattern = ".* (ip:<ipaddr>):(d:<port>).*"

        rexpat = rex.reformat_pattern(pattern)
        print "REXPAT: ", rexpat

        mobj = re.match(rexpat, teststring)
        if mobj:
            print "Matched: ", mobj.group(0)

    def test_match_ts1(self):
        '''
        Test the timestamp match functionality
        '''
        teststr = "2015-11-13 06:38:04.571 23441 INFO nova.openstack.common.service [-] Child 28349 killed by signal 9"
        pattern = ".*(ts1:<timestamp>).*"

        rexpat = rex.reformat_pattern(pattern)
        print "REXPAT: ", rexpat

        mobj = re.match(rexpat, teststr)
        if mobj:
            print "Matched: ", mobj.group(0)
            print "year: ", mobj.group(2)
            print "Month: ", mobj.group(3)
            print "date: ", mobj.group(4)
            print "hour: ", mobj.group(5)
            print "min: ", mobj.group(6)
            print "sec: ", mobj.group(7)
            print "msec: ", mobj.group(8)

    def test_match_ts2(self):
        '''
        Test the timestamp match functionality.
        '''
        teststr = "2015-11-13 Fri 12:47:01:041.992 PST  gngsvm001d [Thread 140217231050496, Pid 41480]"
        pattern = ".*(ts2:<timestamp>)"

        rexpat = rex.reformat_pattern(pattern)
        print "REXPAT: ", rexpat

        mobj = re.match(rexpat, teststr)
        if mobj:
            print "Matched: ", mobj.group(1)
            print "year: ", mobj.group(2)
            print "month: ", mobj.group(3)

    def match_timestamp(self, pattern, teststr, isvalid=True):
        '''
        Generic function for timestamp match test.
        '''
        rexpat = rex.reformat_pattern(pattern)
        print "String: ", teststr
        print "REXPATTERN: ", rexpat

        mobj = re.match(rexpat, teststr)
        if mobj:
            print "matched: ", mobj.group(1)

    def test_match_ts3(self):
        '''
        Test timestamp match functionality.
        '''
        teststr = "172.29.106.218 - - [02/Nov/2015:09:03:19 -0800] \"GET /horizon"
        pattern = ".*(ts3:<timestamp>.*)"

        self.match_timestamp(pattern, teststr)

    def test_match_ts4(self):
        '''
        Test timestamp match functionality.
        '''
        teststr = ""
        pattern = ".*(ts4:<timestamp>.*)"
        self.match_timestamp(pattern, teststr)

    def test_match_ts5(self):
        '''
        Test timestamp match functionality
        '''
        teststr = "2015-11-13 06:25:07.799684 mon.0 10.163.41.4:6789/0 799978 : "
        pattern = ".*(ts5:<timestamp>).*"
        self.match_timestamp(pattern, teststr)

    def test_match_ts6(self):
        '''
        Test timestamp match functionality
        '''
        teststr = " INFO [OptionalTasks:1] 2015-09-20 10:22:58,580 ColumnFamilyStore.java (line 626)"
        pattern = ".*(ts6:<timestamp>).*"
        self.match_timestamp(pattern, teststr)

    def test_match_ts7(self):
        '''
        Test timestamp match functionality
        '''
        teststr = "10.163.41.8:37615 [13/Nov/2015:06:22:05.843] mysql mysql/mysql1 1"
        pattern = ".*\[(ts7:<timestamp>).*"
        self.match_timestamp(pattern, teststr)

    def test_match_ts8(self):
        '''
        Test timestamp match functionality
        '''
        teststr = "150630 11:40:26 InnoDB: Initializing buffer pool, size = 128.0M"
        pattern = ".*(ts8:<timestamp>).*"
        self.match_timestamp(pattern, teststr)

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

        rexdict = rex.parse_lrvalue_string(test_string)
        self.failUnless(rexdict['serial_number'] == "FCH1278Ad")
        self.failUnless(rexdict['product_name'] == "UCS C240 M3S")

    def test_parse_lrval_string(self):
        '''
        Test the API to parse a LR value string.
        '''
        fhandle = open("test_data/lrvalue_output.txt", "r")
        data = fhandle.read()
        parsed_data = rex.parse_lrvalue_string(data)
        print "Parsed data: ", parsed_data

    def test_parse_lrval2_string(self):
        '''
        Test the API to parse a LR value string.
        '''
        fhandle = open("test_data/lrvalue2_output.txt", "r")
        data = fhandle.read()
        parsed_data = rex.parse_lrvalue_string(data, delimiter=":")
        print "Parsed data: ", parsed_data

    def test_parse_lrval3_string(self):
        '''
        Test the API to parse a LR value string.
        '''
        fhandle = open("test_data/lrvalue3_output.txt", "r")
        data = fhandle.read()
        parsed_data = rex.parse_lrvalue_string(data, delimiter="=")
        print "Parsed data: ", parsed_data

    def test_parse_multi_lrvalue_string(self):
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
        dictlist = rex.parse_multi_lrvalue_string(test_string,
                                                  "Physical Drive Number")
        print pprint.PrettyPrinter(indent=4).pprint(dictlist)

    def test_parse_mlrvalue_string(self):
        '''
        Test the parse_multi_lrvalue_string API
        '''
        fhandle = open("test_data/mlrvalue_output.txt", "r")
        data = fhandle.read()
        parsed_data = rex.parse_multi_lrvalue_string(data,
                                                     "Physical Drive Number")
        print pprint.PrettyPrinter(indent=2).pprint(parsed_data)








