
import sys, os
sys.path.append( os.path.abspath('.') )

import requests, sys, time, json
from threading import Thread
import multiprocessing as mp

from summoner import Summoner

def get_summs( batch ):

    DIVISION  = sys.argv[2]
    TIER = sys.argv[1]
    QUEUE = sys.argv[3] if len(sys.argv) >= 4 else 'RANKED_SOLO_5x5'
    HEADERS = {
        "Origin": "https://developer.riotgames.com",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Riot-Token": "RGAPI-f1c031c7-ce9e-4f3c-9de8-fddb158d5853",
        "Accept-Language": "en-US,en-AS;q=0.7,en;q=0.3",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
         (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763"
    }
    URL = f'https://na1.api.riotgames.com/lol/league/v4/entries/{QUEUE}/{TIER}/{DIVISION}?page='

    res = requests.get( URL + str(batch), headers=HEADERS )
    summs = res.json()
    #print(f'status code {res.status_code}')
    #print(f'{len( summs )} summoners in {TIER} {DIVISION}')

    global summoners
    summoners.extend( summs )

if len(sys.argv) < 3:
    print('Usage: python api.py <TIER> <DIVISION I-IV> [QUEUE]')
    sys.exit(0)

summoners = []
NUM_THREADS = os.cpu_count() if os.cpu_count() else 2

i = 1
while i < NUM_THREADS * 15:

    # Delay for riot api
    time.sleep(1)

    threads = [ Thread( target=get_summs, args=[batch] ) for batch in range(i, i + NUM_THREADS) ]

    start = time.process_time()

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    end = time.process_time()

    i += NUM_THREADS

print(f'{len(summoners)} summoners collected in {end-start}s')

summoner_objs = [ Summoner.from_json( summ ) for summ in summoners ]
for summ in summoner_objs:
    summ['win_rates'] = int(summ['wins']) / ( int(summ['wins']) + int(summ['losses']) )
    summ['games_played'] = int(summ['wins']) + int(summ['losses'])

filtered_summs = Summoner.list_filter( summoner_objs, 'games_played', 100 )
Summoner.sort( filtered_summs, 'win_rates' )

start = time.process_time()
f = open( './data/leaguers.txt', 'w+' )
f.write( f"{ json.dumps( Summoner.list_json( filtered_summs ), indent=3 ) }\n" )
f.close()
end = time.process_time()
print(f'Data written in {end-start}s')

sys.path.pop()




