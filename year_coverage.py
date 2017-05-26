# this helper module helps to determine
# which year were covered during the song collection

from collector import *


f = open('albumfiles/test/items.txt', encoding='utf8')
c = AlbumCollection.process_from_file(f)

result = set()

for item in c:
    result.add(item.release_date()[0])

for item in sorted(list(result)):
    print(item)