# testing python json module
# some basic example using json.dumps and json.loads
# with different optional parameters values

import json
import random

print("TESTTING JSON MODULE")

print("\t--------")
print("\tEncoding")
print("\t--------")

print("\t\tEncoding list of 5 random ints")
a = []
for i in range(5):
    a.append(random.randint(-1000, 1000))
print("\t\t\t",json.dumps(a))

print("\t\tChecking ensure_ascii")
a = {}
a[1] = "ascii characters"
a[2] = "non ascii characters (слово)"
print("\t\t\tTrue:", json.dumps(a, ensure_ascii=True))
print("\t\t\tFalse:", json.dumps(a, ensure_ascii=False))

print("\t\tChecking indent")
a = [1,2]
print("\t\t\tNone:", repr(json.dumps(a))[1:-1])
print("\t\t\t0:", repr(json.dumps(a, indent=0))[1:-1])
print("\t\t\t1:", repr(json.dumps(a, indent=1))[1:-1])
print("\t\t\t2:", repr(json.dumps(a, indent=2))[1:-1])

print("\t\tChecking different separators")
a = {1: "val1", 2: "val2"}
print("\t\t\t None :",json.dumps(a))
sep = ('|', '/')
print("\t\t\t",sep,":",json.dumps(a, separators=sep))

print("\t\tChecking sort_keys")
a = {"b":1, "a": 2, "t":3}
print("\t\t\tFalse:",json.dumps(a))
print("\t\t\tTrue:",json.dumps(a,sort_keys=True))

print("\t\tChecking allow_nan")
a = {"key1":float("inf")}
print("\t\t\tTrue:", json.dumps(a))
try:
    print("\t\t\tFalse:", json.dumps(a, allow_nan=False))
except ValueError as e:
    print("\t\t\tValueError cought while allow_nan=False:")
    print("\t\t\t\t",e)

print("\t--------")
print("\tDecoding")
print("\t--------")

s = """[{"key11":"val11", "key12":"val12"}, {"key21":"val21"}]"""
print("\t\tChecking object_hook")
print("\t\t\tjson string:",s)
print("\t\t\tfunction will return keys of a dictionary")
d = json.loads(s, object_hook=lambda x: set(x.keys()))
print("\t\t\t\t",d)

s = """{"key1":1, "key2":2}"""
print("\t\tChecking parse int")
print("\t\t\tjson string:",s)
print("\t\t\tFunction will increase each int by 1")
d = json.loads(s, parse_int=lambda x: int(x) + 1)
print("\t\t\t\t",d)
