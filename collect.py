
import time

from rifters import leagues
from summ_data import scrape
from summoner import Summoner


me = "jiangpro"

peers_jk = leagues( me, 'NA' )
summoners = []

start = time.perf_counter_ns()
for pj in peers_jk:
	summ = scrape( pj )
	summoners.append( summ )
end = time.perf_counter_ns()
elapsed_secs = (end - start) / 1000000000
print( f"Collecting took {str(elapsed_secs)}s" )

filtered_summs = [ summ.filter() for summ in summoners ]
Summoner.sort( filtered_summs, 'win_rates', False )


f = open('silvers.txt', 'w+')
start = time.perf_counter()
f.writelines( f"{summ}\n" for summ in filtered_summs )
end = time.perf_counter()
elapsed_secs = (end - start) / 1000000000
f.close()
print( f"Storing took {str(elapsed_secs)}s" )

