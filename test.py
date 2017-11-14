from analysis import *
from musicitem import *

'''
a = TimeDelta('ko', None, 1)
a._middle_feature = Feature.process_from_file(('0',0.8919999999999999,0.559,285040.0,0.33,0.0,0,-8.251,0,0.0285,135.109,0,0.28))

f = Feature.process_from_file(('0hP2CWKkYccPiIdvuGd8Sf',0.242,0.594,204613,0.989,0,11,-0.016,1,0.333,93.839,4,0.697))

print(a.getk(f))

print('hello')
'''

from auth import sp as client

r = client.audio_features(['4kflIGfjdZJW4ot2ioixTB',
                           '4etypRtRn8IgsxZu6BhRS6'])
for item in r:
    print(item)
    print('----------')

f = Feature.process(r[0])
s = Feature.process(r[1])
print(f.equal_characteristics(s))