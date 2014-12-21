'''
REX: A pattern matching utility.
It is a wrapper on top of the "re" regular expression module,
but enhances it by adding more functionality and ease of use.
'''

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("rex")


class REX(object):
    '''
    REX: Class instance.
    '''
    def __init__(self, pattern, filename=None):
        '''
        Initialization.
        '''
        self.user_pattern = pattern
        self.search_file = filename
        self.rex_patternstr = None
        self.rex_pattern = None
        # Results store the list of result object.
        # result object ('match obj', 'user defined values')
        #self.results = []
        self.matches = []
        self.res_count = 0

class REXResult(object):
    '''
    REX Result class.
    '''
    def __init__(self, reobj, loc):
        '''
        Initialization.
        '''
        self.reobj = reobj
        self.loc = loc
        self.named_groups = reobj.groupdict()


def reformat_pattern(pattern):
    '''
    Apply the filters on user pattern to generate a new regular
    expression pattern.
    A user provided variable, should start with an alphabet, can be
    alphanumeric and can have _.
    '''
    # User pattern: (w:<name>)  --> Changes to (?P<name>\w)
    rex_pattern = re.sub(r'\(w:<([\w\d_]+)>\)', '(?P<\\1>\w+)', pattern)

    # User pattern: (d:<name>)  --> change to (?P<name>\d)
    rex_pattern = re.sub(r'\(d:<([\w\d_]+)>\)', '(?P<\\1>\d+)', rex_pattern)

    # User pattern: (W:<name>)  --> change to (?P<name>\w)
    rex_pattern = re.sub(r'\(W:<([\w\d_]+)>\)', '(?P<\\1>\W+)', rex_pattern)

    # User pattern: (ip:<ipaddr>) --> Change to (?P<ipaddr>\d+\.\d+\.\d+\.\d+)
    rex_pattern = re.sub(r'\(ip:<([\w\d_]+)>\)',
                         '(?P<\\1>\d+\.\d+\.\d+\.\d+)', rex_pattern)

    # Finally if no prefix is specified take default action.
    rex_pattern = re.sub(r'\(<([\w\d_]+)>\)', '(?P<\\1>.*)', rex_pattern)

    return rex_pattern


def match_string(pattern, string):
    '''
    Match a pattern in a string
    '''
    rexpattern = reformat_pattern(pattern)

    rexcomp = re.compile(rexpattern)
    mobj = rexcomp.match(string)
    if mobj:
        print "matched: ", mobj.group(0), mobj.group('name'), mobj.group(2)


def populate_resobj(rexobj, mobj, loc):
    '''
    Popuate the result object and append it to the
    rexobj results.
    '''
    resobj = REXResult(mobj, loc)
    rexobj.matches.append(resobj)

    rex_resobj = {}
    rex_resobj = {}
    rex_resobj['reobj'] = mobj
    rex_resobj['loc'] = loc
    rexobj.res_count += 1
    for key in mobj.groupdict().keys():
        rex_resobj[key] = mobj.groupdict()[key]
    #rexobj.results.append(rex_resobj)


def match_file(pattern, filename):
    '''
    The function will match a pattern in a file and return
    a rex object, which will have all the matches found in the file.
    '''

    # Validate user data.

    if pattern is None:
        logger.error("Invalid pattern")
        return None

    if os.stat(filename).st_size == 0:
        logger.error("Invalid file")
        return None

    rexobj = REX(pattern, filename)

    rexpatstr = reformat_pattern(pattern)
    print "rexpatstr: ", rexpatstr

    rexpat = re.compile(rexpatstr)
    rexobj.rex_patternstr = rexpatstr
    rexobj.rex_pattern = rexpat

    sfile = open(filename, 'r')
    data = sfile.read()
    sfile.close()

    line_count = 1
    for line in data.splitlines():
        mobj = rexpat.match(line)
        if mobj:
            print "matched: ", mobj.group(0), mobj.group(1)
            populate_resobj(rexobj, mobj, line_count)
            #rex_resobj = {}
            #rex_resobj['reobj'] = mobj
            #rex_resobj['loc'] = line_count
            #rexobj.results.append(rex_resobj)
            rexobj.res_count += 1
            #mydict = mobj.groupdict()
            #print "mydict: ", mydict, mydict.keys()
            #print "dir mydict: ", dir(mydict)
            #for key in mydict.keys():
            #    print "val: ", mydict[key]

        line_count += 1

    return rexobj


def dump_rexobj_results(rexobj, options=None):
    '''
    print all the results.
    '''
    matches = rexobj.matches
    for match in matches:
        for key in match.named_groups.keys():
            print  "%s: %s" %(key, match.named_groups[key]),
        print ""
        done = False
        cnt = 0
        while not done:
            try:
                print "%d: %s" % (cnt, match.reobj.group(cnt)),
                cnt += 1
            except IndexError:
                print ""
                done = True





