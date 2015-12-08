# goal: show that the value of the output, hours, is always > 120

hours = readInt()
assert hours > 2
"""{ 1. hours > 2    premise  }"""
minutes = hours * 60
"""{ 1.  hours > 2           premise
     2.  minutes == hours * 60  premise
     3.  minutes > 120          algebra 1 2
}"""
print hours, minutes
raw_input()

