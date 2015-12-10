#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Copyright 2015 Behzad Dastur

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

'''
REX: A general purpose string and pattern matching utility
built as a wrapper on python re to provide additional functionalit
and ease of use. For more details check the README.md file.'''

import re
import os

__version__ = "0.0.1"


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
                         '(?P<\\1>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})',
                         rex_pattern)

    # User pattern: (mac:<macaddr>) --> Change to (?P<mac>\w\w:\w\w:\w\w:..)
    rex_pattern = re.sub(r'\(mac:<([\w\d_]+)>\)',
                         '(?P<\\1>\w\w:\w\w:\w\w:\w\w:\w\w:\w\w)', rex_pattern)

    ######################################
    # Timestamp patterns.
    # User pattern: (ts[n]:<timestamp>) -->
    # Converted to: The below options.
    ######################################

    # User pattern: (ts1:<timestamp>)
    # Keystone, nova, libvirt, cinder
    # Example: 2015-11-13 06:38:04.571
    rex_pattern = re.sub(
        r'\(ts1:<([\w\d_]+)>\)',
        '(?P<\\1>(\d{4})-(\d{1,2})-(\d{1,2}) (\d+):(\d+):(\d+)\.(\d+))',
        rex_pattern)

    # User pattern: (ts2:<timestamp>)
    # contrail
    # Example: 2015-11-13 Fri 13:14:51:907.395 PST
    rex_pattern = re.sub(
        r'\(ts2:<([\w\d_]+)>\)',
        '(?P<\\1>(\d{4})-(\d{1,2})-(\d{1,2}) (\w{3}) (\d+):(\d+):(\d+):(\d+)\.(\d+))',
        rex_pattern)

    # User pattern: (ts3:<timestamp>)
    # apache2
    # Example: Thu Aug 20 14:18:34 2015
    rex_pattern = re.sub(
        r'\(ts3:<([\w\d_]+)>\)',
        '(?P<\\1>(\w{3}) (\w{3}) (\d{1,2}) (\d+):(\d+):(\d+) (\d{4}))',
        rex_pattern)

    # User pattern: (ts4:<timestamp>)
    # Example: 02/Nov/2015:09:03:19 -0800
    rex_pattern = re.sub(
        r'\(ts4:<([\w\d_]+)>\)',
        '(?P<\\1>(\d+)\/(\w{3})\/(\d{4}):(\d+):(\d+):(\d+) -(\d+))',
        rex_pattern)

    # User pattern: (ts5:<timestamp>)
    # ceph logs.
    # Example: 2015-11-13 06:25:29.436844
    rex_pattern = re.sub(
        r'\(ts5:<([\w\d_]+)>\)',
        '(?P<\\1>(\d{4})-(\d{1,2})-(\d{1,2}) (\d+):(\d+):(\d+)\.(\d+))',
        rex_pattern)

    # User pattern: (ts6:<timestamp>)
    # cassandra
    # Example:2015-10-23 12:38:15
    rex_pattern = re.sub(
        r'\(ts6:<([\w\d_]+)>\)',
        '(?P<\\1>(\d{4})-(\d{1,2})-(\d{1,2}) (\d+):(\d+):(\d+))',
        rex_pattern)

    # User pattern: (ts7:<timestamp>)
    # haproxy
    # Example: 13/Nov/2015:06:25:05.465
    rex_pattern = re.sub(
        r'\(ts7:<([\w\d_]+)>\)',
        '(?P<\\1>(\d+)\/(\w{3})\/(\d{4}):(\d+):(\d+):(\d+)\.(\d+))',
        rex_pattern)

    # User pattern: (ts8:<timestamp>)
    # mysql
    # Example: 12:03:28
    rex_pattern = re.sub(
        r'\(ts8:<([\w\d_]+)>\)',
        '(?P<\\1>(\d+):(\d+):(\d+))',
        rex_pattern)

    # User pattern: (ts9:<timestamp>)
    # reddis
    # Example: 08 Nov 06:26:05.084
    rex_pattern = re.sub(
        r'\(ts9:<([\w\d_]+)>\)',
        '(?P<\\1>(\d+) (\w{3}) (\d+):(\d+):(\d+)\.(\d+))',
        rex_pattern)

    # user pattern: (ts10:<timestamp>)
    # supervisord, zookeeper
    # Example: 2015-06-30 10:59:18,133
    rex_pattern = re.sub(
        r'\(ts10:<([\w\d_]+)>\)',
        '(?P<\\1>(\d{4})-(\d{1,2})-(\d{1,2}) (\d+):(\d+):(\d+),(\d+))',
        rex_pattern)

    # User pattern: (ts11:<timestamp>)
    # dmesg
    # Example: 11148214.574583
    rex_pattern = re.sub(
        r'\(ts11:<([\w\d_]+)>\)',
        '(?P<\\1>(\d+)\.(\d+))',
        rex_pattern)

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


def parse_lrvalue_string(search_string,
                         delimiter=":"):
    '''
    The function takes a multi-line output/string with the format
    "name/descr   : value", and converts it to a dictionary object
    with key value pairs, where key is built from the name/desc
    part and value as the value.

    eg:  "Serial Number: FCH1724V1GT" will be translated to
    dict['serial_number'] = "FCH1724V1GT"
    '''
    mac_search_pattern = r"(.*) *%s ([\w|\d]+.*)" % delimiter
    search_pattern = r"(.*) *%s *(.*)" % delimiter

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


def parse_multi_lrvalue_string(search_string, split_string):
    '''
    The function is an extension of the parse_lrvalue_string() API.
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
        tdict = parse_lrvalue_string(split_string + out)
        dictlist.append(tdict)

    return dictlist


def parse_tabular_string(search_string,
                         header_keys,
                         delimiter=None,
                         merge_list=None):
    '''
    Given a string in a tabular format, parse it and return a
    dictionary
    @args:
        search_string: This is a string in tabular format (e.g.: output of df
        command)
        header_keys: This is a list of strings for the headers.
        delimiter(optional): Default is None, which translates to spaces
        merge_list(optional): In some cases 2 fields need to be merged as they
        are one value.
    '''
    first_line = True
    parsed_results = []
    for line in search_string.splitlines():
        if first_line:
            first_line = False
        else:
            result = {}
            row = line.split()
            if merge_list:
                for mergeset in merge_list:
                    fidx = mergeset[0]
                    lidx = mergeset[1]
                    try:
                        row[fidx] = "_".join(row[fidx:(lidx+1)])
                        row.remove(row[lidx])
                    except IndexError:
                        pass

            if len(row) != len(header_keys):
                print "Incorrect fields len "
                continue
            key_count = 0
            for column in row:
                result[header_keys[key_count]] = column
                key_count += 1
            parsed_results.append(result)

    return parsed_results


def dump_rexobj_results(rexobj, options=None):
    '''
    print all the results.
    '''
    print("-" * 60)
    print("Match count: ", rexobj.res_count)
    matches = rexobj.matches
    for match in matches:
        print("Loc:", match.loc, ":: ")
        for key in match.named_groups.keys():
            print("%s: %s" %
                  (key, match.named_groups[key]))
        print("")

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




