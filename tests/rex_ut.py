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
        print "test_reformat_pattern"
        test_pattern = "(w:<name>) is (w:<attribute>)"
        matchpat = "(?P<name>\w+) is (?P<attribute>\w+)"
        rexpat = rex.reformat_pattern(test_pattern)
        self.failUnless(rexpat == matchpat)

        test_pattern = "(d:<number>),testst_-(w:<name>), xyz(W:<attr>),(<foo>)"
        matchpat = "(?P<number>\d+),testst_-(?P<name>\w+), xyz(?P<attr>\W+),(?P<foo>.*)"

        rexpat = rex.reformat_pattern(test_pattern)
        self.failUnless(rexpat == matchpat)

        test_pattern = "(d:<number>), IP: (ip:<ipaddr>),.*"
        rexpat = rex.reformat_pattern(test_pattern)
        print "rexpat: ", rexpat

    def test_match_string(self):
        '''
        test match string.
        '''
        print "test_match_string"

        teststr = "Mary had 8 Lambs, and they were white as snow."
        testpat = "(w:<name>) had (d:<num>) Lambs"
        rex.match_string(testpat, teststr)


    def test_match_file(self):
        '''
        test match_file(pattern, filename)
        '''
        print "test match file"
        # [2014-12-10:9095 ERROR]IP: 172.22.1983, MAC:44:aa:ea:9d:43:23, INT:eth0,
        # testpattern = "[(d:<year>)\-(d:<month>)\-(d:<day>) (w:<loglevel>)]" \
        #    "IP: (ip:<ipaddr>).*"
        # [2014-12-10:9088 INFO]Mary had 8 Lambs, and they all where white as Sn0w.

        testpattern = "\[(d:<year>)-(d:<month>)-(d:<day>):(\d+) (w:<level>)\](w:<name>) had (d:<num>) Lambs.*"
        testfile = "test_data/simple.txt"
        rexobj = rex.match_file(testpattern, testfile)
        rex.dump_rexobj_results(rexobj)






