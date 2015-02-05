'''
REX: A pattern matching utility.
It is a wrapper on top of the "re" regular expression module,
but enhances it by adding more functionality and ease of use.
'''

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os


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
        # result object type REXResult
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
    Apply the filters on user pattern to generate a new regular expression
    pattern.
    A user provided variable, should start with an alphabet, can be
    alphanumeric and can have _.
    '''
    # User pattern: (w:<name>)  --> Changes to (?P<name>\w)
    rex_pattern = re.sub(r'\(w:<([\w\d_]+)>\)', '(?P<\\1>\w+)', pattern)

    # User pattern: (d:<name>)  --> change to (?P<name>\d)
    rex_pattern = re.sub(r'\(d:<([\w\d_]+)>\)', '(?P<\\1>\d+)', rex_pattern)

    # User pattern: (W:<name>)  --> change to (?P<name>\w)
    rex_pattern = re.sub(r'\(W:<([\w\d_]+)>\)', '(?P<\\1>\W+)', rex_pattern)

    # User pattern: (any:<anyvalue> --> change to (?P<anyvalue>.*)
    rex_pattern = re.sub(r'\(any:<([\w\d_]+)>\)', '(?P<\\1>.*)', rex_pattern)

    # User pattern: (ip:<ipaddr>) --> Change to (?P<ipaddr>\d+\.\d+\.\d+\.\d+)
    rex_pattern = re.sub(r'\(ip:<([\w\d_]+)>\)',
                         '(?P<\\1>\d+\.\d+\.\d+\.\d+)', rex_pattern)

    # User pattern: (mac:<macaddr>) --> Change to (?P<mac>\w\w:\w\w:\w\w:..)
    rex_pattern = re.sub(r'\(mac:<([\w\d_]+)>\)',
                         '(?P<\\1>\w\w:\w\w:\w\w:\w\w:\w\w:\w\w)', rex_pattern)

    # Finally if no prefix is specified take default action.
    rex_pattern = re.sub(r'\(<([\w\d_]+)>\)', '(?P<\\1>.*)', rex_pattern)

    return rex_pattern

def match_string(pattern, search_string):
    '''
    Match a pattern in a string
    '''

    rexobj = REX(pattern, None)

    rexpatstr = reformat_pattern(pattern)
    #print "rexpatstr: ", rexpatstr

    rexpat = re.compile(rexpatstr)
    rexobj.rex_patternstr = rexpatstr
    rexobj.rex_pattern = rexpat

    line_count = 1
    for line in search_string.splitlines():
        line = line.strip()
        mobj = rexpat.match(line)
        if mobj:
            populate_resobj(rexobj, mobj, line_count)
        line_count += 1

    return rexobj

def populate_resobj(rexobj, mobj, loc):
    '''
    Popuate the result object and append it to the
    rexobj results.
    '''
    resobj = REXResult(mobj, loc)
    rexobj.matches.append(resobj)
    rexobj.res_count += 1


def match_file(pattern, filename):
    '''
    The function will match a pattern in a file and return
    a rex object, which will have all the matches found in the file.
    '''

    # Validate user data.

    if pattern is None:
        return None

    if os.stat(filename).st_size == 0:
        return None

    rexobj = REX(pattern, filename)

    rexpatstr = reformat_pattern(pattern)
    #print "rexpatstr: ", rexpatstr

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
            populate_resobj(rexobj, mobj, line_count)

        line_count += 1

    return rexobj


def get_dict_from_string(search_string):
    '''
    The function takes an multi-line output/string with the format
    "name/descr   : value", and converts it to a dictionary object
    with key value pairs, where key is built from the name/desc
    part and value as the value.

    eg:  "Serial Number: FCH1724V1GT" will be translated to
    dict['serial_number'] = "FCH1724V1GT"
    '''
    mac_search_pattern = r"(.*) *: ([\w|\d]+.*)"
    search_pattern = r"(.*) *: *(.*)"

    rexdict = {}
    for line in search_string.splitlines():
        line = line.strip()
        mobj = re.match(mac_search_pattern, line)
        if mobj:
            key = mobj.group(1).lower()
            key = "_".join(key.split()[0:3])
            key = key.strip()
            rexdict[key] = mobj.group(2)
            continue

        mobj = re.match(search_pattern, line)
        if mobj:
            key = mobj.group(1).lower()
            key = "_".join(key.split()[0:3])
            key = key.strip()
            rexdict[key] = mobj.group(2)

    return rexdict


def get_dictlist_from_string(search_string, split_string):
    '''
    The function is an extension of the get_dict_from_string() API.
    The function takes a multi-line output/string of the format
    "Category: xyz
       name: foo
       id: bar
     Category: abc
       name: foox
       id: barx
    :
    "
    It splits the output based on the splitstring passed as
    argument (eg "Category"), and converts the individual
    lines of the form "name:  value" to a dictionary object with
    key value pairs. The key is built from the name (LV) part.
    eg "First Name: Behzad" --> dict[first_name] = "Behzad"
    '''
    dictlist = []
    for out in search_string.split(split_string):
        tdict = get_dict_from_string(out)
        dictlist.append(tdict)

    return dictlist

def dump_rexobj_results(rexobj, options=None):
    '''
    print all the results.
    '''
    print "-" * 60
    print "Match count: ", rexobj.res_count
    matches = rexobj.matches
    for match in matches:
        print "Loc:", match.loc, ":: ",
        for key in match.named_groups.keys():
            print "%s: %s" % \
                (key, match.named_groups[key]),
        print ""

        #done = False
        #cnt = 0
        #while not done:
        #    try:
        #        print "%d: %s" % (cnt, match.reobj.group(cnt)),
        #        cnt += 1
        #    except IndexError:
        #        print ""
        #        done = True

def get_match_value(rexobj, key, index=0):
    '''
    Return a matched value for the key for a specific match from the
    results.
    '''
    if rexobj is None:
        return None

    if rexobj.res_count == 0:
        return None

    try:
        return rexobj.matches[index].named_groups[key]
    except IndexError:
        return None
    except KeyError:
        return None




