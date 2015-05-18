REX:

A general purpose string and expression matching utility built as a 
wrapper on python re module to provide additional useful functionality

Some functionality:

1. built-in common patterns.

The most common patterns like mac address, ip address, etc can be used quite easily as below:

Consider the following string to be matched: 
macstr =  "Link encap:Ethernet  HWaddr 00:50:56:BB:1B:BE"

And you want to parse the string and get the mac address.

Your pattern will look like this:
    testpat = ".*HWaddr (mac:<macaddr>)"

    rexobj = rex.match_string(testpat, macstr)
    macval = rex.get_match_value(rexobj, "macaddr", 0)
    print "value: ", macval 
