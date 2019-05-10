
from pyquery import PyQuery as pq
from os import path
import json, math, time

BASE_PATH = 'https://na.op.gg/ranking/ladder'

# Get total summoners
d = pq( url=BASE_PATH )
desc = d('div.PageDescription span.Text').text()

TOTAL_SUMMONERS = int( "".join([ c for c in desc if c.isdigit() ]) )
NUM_PAGES = int(math.ceil(TOTAL_SUMMONERS/100))

# Get summoner names from each page
players = []
start = time.process_time()
for page in range( 1, 100 ):
	d = pq( url=path.join( BASE_PATH, f'page={page}' ) )
	rows = d('table.ranking-table tbody tr')
	for row in rows:
		players.append( pq(row).find('td.ranking-table__cell--summoner span').text() )
end = time.process_time()
print( f'Gathering players took {str(end-start)}s' )
'''
f = open( './data/players.txt', 'w+' )
f.writelines( "%s\n" % player for player in players )
f.close()
'''
