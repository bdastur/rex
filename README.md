[TOC]

rex
===
A simple python module which serves as an abstraction to the python
regular expression (re) module in some use cases.

------
# Introduction:

The rex module was born out of necessity. I found myself writing code to parse a lot of command line output for some switches which did not have a good API interface and also in some cases where CLI was the best option to get the data I needed.

In a lot of cases the output format was very similar where I could generalize and try to come up with a common API that can be used for any such CLI. I could not find anything that would fit the bill, and rex was born.

------

# Functionality:
The module provides the following main abstractions:

## **1. Parsing a LR Value String:**
Consider the output of a CLI "show chassis" below from a switch. 
```
  chassis : UCS43
  Serial no : USC788dc
  Firmware : 12.01(99)
  PID : UCS4343
  UUID : URY888dR7R7R8-090-99
  Description : Ucs M3 Series Chassis

```
The LRValue parser will parse this output and return a dictionary:
```
{ 
  'firmware': '12.01(99)', 
  'description': 'Ucs M3 Series Chassis', 
  'serial_no': 'USC788dc',
  'pid': 'UCS4343', 
  'chassis': 'UCS43', 
  'uuid': 'URY888dR7R7R8-090-99'
 }
```

## **2. Parsing multiple LR Value strings.**
A similar use case is where you have multiple  blocks of LRValue paris.
Consider the example of a CLI to display adapters.
```
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
```

In this case the LRValue parser will parse the output and
return a list of dictionary object
```
[ { },
  { 'coerced_size': '952720 MB',
    'controller': 'SLOT-4',
    'drive_firmware': 'CC03',
    'health': 'Good',
    'manufacturer': 'ATA',
    'model': 'ST91000640NS',
    'physical_drive_number': '',
    'predictive_failure_count': '0',
    'status': 'Unconfigured Good',
    'type': 'HDD'},
  { 'coerced_size': '952720 MB',
    'controller': 'SLOT-4',
    'drive_firmware': 'CC03',
    'health': 'Good',
    'manufacturer': 'ATA',
    'model': 'ST91000640NS',
    'physical_drive_number': '',
    'predictive_failure_count': '0',
    'status': 'Unconfigured Good'}]
```

## **3. Parsing a tabular format string.**
Very common output format is a tabular format with fields seperated by 
delimiters (spaces, |, etc).

An example here is the "df" command:
```
Filesystem     1K-blocks     Used Available Use% Mounted on
/dev/md1        95926932 27688272  63359156  31% /
udev           132014724        4 132014720   1% /dev
tmpfs           52809712      448  52809264   1% /run
none                5120        0      5120   0% /run/lock
none           132024280        0 132024280   0% /run/shm
cgroup         132024280        0 132024280   0% /sys/fs/cgroup
/dev/md0          943544    28960    865820   4% /boot
/dev/md2       806415824 63998212 701447384   9% /var
```

Here the taubular string parser will parse the output, and return a list
of dictionary objects as below:
```
[ { '1k-blocks': '95926932',
    'Available': '63359156',
    'Filesystem': '/dev/md1',
    'Mounted_on': '/',
    'usage%': '31%',
    'used': '27688272'},
  { '1k-blocks': '132014724',
    'Available': '132014720',
    'Filesystem': 'udev',
    'Mounted_on': '/dev',
    'usage%': '1%',
    'used': '4'},
  { '1k-blocks': '52809712',
    'Available': '52809264',
    'Filesystem': 'tmpfs',
    'Mounted_on': '/run',
    'usage%': '1%',
    'used': '448'},
  { '1k-blocks': '5120',
    'Available': '5120',
    'Filesystem': 'none',
    'Mounted_on': '/run/lock',
    'usage%': '0%',
    'used': '0'},
  { '1k-blocks': '132024280',
    'Available': '132024280',
    'Filesystem': 'none',
    'Mounted_on': '/run/shm',
    'usage%': '0%',
    'used': '0'},
  { '1k-blocks': '132024280',
    'Available': '132024280',
    'Filesystem': 'cgroup',
    'Mounted_on': '/sys/fs/cgroup',
    'usage%': '0%',
    'used': '0'},
  { '1k-blocks': '943544',
    'Available': '865820',
    'Filesystem': '/dev/md0',
    'Mounted_on': '/boot',
    'usage%': '4%',
    'used': '28960'},
  { '1k-blocks': '806415824',
    'Available': '701447384',
    'Filesystem': '/dev/md2',
    'Mounted_on': '/var',
    'usage%': '9%',
    'used': '63998212'}]

```


## **4. Common (re) Pattern Abstractions**
Another use case where parsing strings is needed is in logs and other program output. 
Some of the common patterns which can abstract a lot of pain in writing regular expression strings
are below:

### 1. IP Address:
Here is an example of a log from haproxy:
```
Nov 16 16:35:06 testhost1 haproxy[37217]: 192.16.41.8:45133 [16/Nov/2015:16:32:04.152] mysql mysql/mysql1 1/0/182236 12736 -- 647/261/261/261/0 0/0
Nov 16 16:35:06 testhost1 haproxy[37217]: 192.16.41.8:45100 [16/Nov/2015:16:32:03.525] mysql mysql/mysql1 1/0/182932 13077 -- 647/261/261/261/0 0/0
Nov 16 16:35:06 testhost1 haproxy[37217]: 192.16.41.8:45131 [16/Nov/2015:16:32:04.105] mysql mysql/mysql1 1/0/182483 12592 -- 647/261/261/261/0 0/0
Nov 16 16:35:07 testhost1 haproxy[37217]: 192.16.41.8:45182 [16/Nov/2015:16:32:05.396] mysql mysql/mysql1 1/0/182246 8352 -- 647/261/261/261/0 0/0
Nov 16 16:35:07 testhost1 haproxy[37217]: 192.16.41.4:55572 [16/Nov/2015:16:32:07.711] mysql mysql/mysql1 1/0/180119 16915 -- 647/261/261/261/0 0/0

```

Consider we want to parse the log and get all the ip addresses and ports. Here is how we can do that
using the rex reformat pattern API.

First we define our search pattern:
```
# Get the ipaddress and port no from the output.                         
pattern = ".* (ip:<ipaddr>):(d:<port>).*"
```

Invoke the rex "reformat_pattern() API.
```                                              
rexpat = rex.reformat_pattern(pattern)                                   
```

Now we can use this as a pattern to search. In this case the re.finditer to iterate
through all the matches:
```                                                                          
for mobj in re.finditer(rexpat, data):                                   
    print "IP ADDR: %s, PORT: %s" % \                                    
        (mobj.group(1), mobj.group(2))    
```

This returns the output:
```
IP ADDR: 192.16.41.8, PORT: 45133
IP ADDR: 192.16.41.8, PORT: 45100
IP ADDR: 192.16.41.8, PORT: 45131
IP ADDR: 192.16.41.8, PORT: 45182
IP ADDR: 192.16.41.4, PORT: 55572
```

### 2. MAC Addresses:

### 3. Timestamps:

