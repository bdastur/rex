rex
====
[![PyPI Version](https://img.shields.io/pypi/v/rexutil.svg)](https://pypi.python.org/pypi/rexutil)

A simple python module which serves as an abstraction to the python
regular expression (re) module in some use cases.

+ [Introduction] (https://github.com/bdastur/rex/blob/master/README.md#introduction)
+ [Features] (https://github.com/bdastur/rex/blob/master/README.md#features)
    [RE Pattern Abstractions] (https://github.com/bdastur/rex/blob/master/README.md#pabstractions)
  + [LR Value Parsing] (https://github.com/bdastur/rex/blob/master/README.md#lrvalue)
  + [Multiple LR Value Parsing] (https://github.com/bdastur/rex/blob/master/README.md#mlrvalue)
  + [Table formatParsing] (https://github.com/bdastur/rex/blob/master/README.md#tabular)
  [Getting Started/Installation] (https://github.com/bdastur/rex/blob/master/README.md#getting-started)


------
# Introduction:<a name="introduction"></a>

The rex module was born out of necessity. It was an attempt to simplify working with python regular expressions in a couple of different ways.  In the section below 
you can see some of the abstractions and features that it provides to simplify regex manipulations.

------
# Features:<a name="features"></a>

## **1. RE Pattern Abstractions**<a name="pabstractions"></a>

It can simplify writing regular expression patterns by providing some patterns that most commonly show up when parsing data.

  Here are some examples to explain what we mean. 
  Consider the below output from a command:
  ```
  READ: io=950144KB, aggrb=94947KB/s, minb=94947KB/s, maxb=94947KB/s, mint=10007msec, maxt=10007msec
  ```

  *Without* REX you would write a regexp pattern as below to capture all the data from this string. 
  > Note: Here the complex regex pattern is to match a decimal/non-decimal number followed by the units
          like KB, MB or KB/s

  ```
   ".*READ: io=(\d*\.\d+|\d+)(\w+|\w+/\w+),.*aggrb=(\d*\.\d+|\d+)(\w+|\w+/\w+),.*" \
   "minb=(\d*\.\d+|\d+)(\w+|\w+/\w+),.*maxb=(\d*\.\d+|\d+)(\w+|\w+/\w+),.*mint=(\d*\.\d+|\d+)(\w+|\w+/\w+),.*maxt=(\d*\.\d+|\d+)(\w+|\w+/\w+).*"              
  ```

  Now let's look at writing the same pattern using REX. I am sure you will agree that the pattern below is much cleaner
  and clearer than the one above.
  
  Rex provides various pattern abstractions, like *"measurement"* as in the case below that you can use to simplify your regex pattern.
  
  case that you can use to define what kind of pattern you expect and REX will generate the complex re pattern for you. The table
  below shows several of these tags that can be used to simplify your code.

   ```
   ".*READ:.*io=(measurement:<io>),.* aggrb=(measurement:<aggrbw>),.*minb=(measurement:<minavgbw>),.*" \                 
         "maxb=(measurement:<maxavgbw>),.*mint=(measurement:<minruntime>),.*maxt=(measurement:<maxruntime>)"    

   ```

### Usage:
 
   Writing a REX pattern will follow the santax (tag:<identifier>), where tag is the pattern abstraction tag provided by REX and the identifier is something
   that you can specify as an identifier. REX will generate a complex re pattern for you, so you do not have to worry about those nuances.

   You can then get the vaule of your mobj using mob.group('identifier'). 
   
   Example usage:.

   ```
    # Define your pattern
    pattern = ".*(ip:<interface_ip>):(d:<port>).*GW:(ip:<gw_ip>).*"

    formatted_pattern = rex.reformat_pattern(pattern, compile=True)

    matchobj = formatted_pattern.match(search_str)
    if matchobj:
        print "interface ip: ", matchobj.group('interface_ip')
        print "port: ", matchobj.group('port')

   ```

  **List of REX pattern abstractions:**
 
  
|REX Pattern Tags           |Description                                                                        |
|--------------------------|--------------------------------------------------------------------------------------|
|(w:\<identifier\>)           |Similar to the re \w - Matches any alphanumeric character                            |
|(d:\<identifier\>)           |Similar to the re \d - Matches any range of decimal digits.                      |
|(W:\<identifier\>)           |Similar to the re \W - Matches any non alphanumeric character            |
|(any:\<identifier\>)         |Similar to using .* - Match anything.                                             |
|(ip:\<identifier\>)          |Match ipv4 ip address string <0-3>:<0-3>:<0-3>:<0-3>                                |
|(mac:\<identifier\>)         |Matches a mac address format.                                                |
|(decimal:\<identifier\>)     |Matches a decimal or non decimal number                                | 
|(measurement:\<identifier\>) |Matches a number followed by alphanumeric value (eg: 78KB, 0.90KB/s 9022MB, etc)     |
|(ts\<n\>:\<identifier\>)  |Matches a timestamp type string.                                                   |


## **2. Parsing a LR Value String:**<a name="lrvalue"></a>
Many switches and even CLI outputs follow a LR value pattern. Eg <field> <delimiter> <vaule>. REX provides an API to parse just output
and return a dictionary of data that you can use.

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

### Usage:
Using this functionaity is as simple as calling a single API.
This is how we can use the LR value parsing: 
```
    import rex

    # Assume your CLI output as above is in a variable called data.
    data = some_api_to_get_data()

    rex_parsed_data = rex.parse_lrvalue_string(data, delimiter=":")

    print "chassis type: ", rex_parsed_data['chassis']
    print "serial no: ", rex_parsed_data['serial_no']

```


## **3. Parsing multiple LR Value strings.**<a name="mlrvalue"></a>
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

### Usage:
Similar to the LRValue parsing using this is a simple API call. The
output is a list of dict objects parsed by rex.

```
    import rex

    rexparsed_dictlist = rex.parse_multi_lrvalue_string(userdata, "Physical Drive Number", delimiter=":")

```


## **4. Parsing a tabular format string.**<a name="tabular"></a>
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


### Usage:
Here's an example of how we can use rex API to parse a tabular format data as above.

```
    import rex

    headers = ["Id", "Name", "State"]
    rex_parsed = rex.parse_tabular_string(data, headers)

```


------
# Getting Started:<a name="getting-started"></a>


## Installing using pip:
```
   pip install rexutil
   ```

## Installing (git clone):
```
git clone https://github.com/bdastur/rex -b master
```

## Usage:
```
   import rex
   ```

