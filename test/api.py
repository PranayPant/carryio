
import sys, os, logging
sys.path.append( os.path.abspath('.') )

import requests, time, json
from threading import Thread

from summoner import Summoner

def get_summs( batch, DIVISION, TIER, QUEUE ):

    HEADERS = {
        "Origin": "https://developer.riotgames.com",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Riot-Token": "RGAPI-3d3eb40e-c3b7-4d45-9a15-734e241cc43b",
        "Accept-Language": "en-US,en-AS;q=0.7,en;q=0.3",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
         (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763"
    }
    URL = f'https://na1.api.riotgames.com/lol/league/v4/entries/{QUEUE}/{TIER}/{DIVISION}?page='

    res = requests.get( URL + str(batch), headers=HEADERS )
    summs = res.json()

    #logger.debug(f'API sent {summs}')

    global summoners
    summoners.extend( summs )

if len(sys.argv) < 3:
    print('Usage: python api.py <TIER> <DIVISION I-IV> [QUEUE]')
    sys.exit(0)

DIVISION  = sys.argv[2]
TIER = sys.argv[1]
QUEUE = sys.argv[3] if len(sys.argv) >= 4 else 'RANKED_SOLO_5x5'

LOG_LEVEL = sys.argv[4] if len(sys.argv) >= 5 else logging.DEBUG
NUM_THREADS = os.cpu_count() if os.cpu_count() else 2

log_filename = 'app.log'
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')

fh = logging.FileHandler(filename=os.path.join('./log', log_filename))
fh.setLevel(LOG_LEVEL)
fh.setFormatter(formatter)
logger.addHandler( fh )

summoners = []

start = time.process_time()

i = 1
while i < NUM_THREADS * 10:

    # Delay for riot api
    time.sleep(2)

    threads = [ Thread( target=get_summs, args=[batch, DIVISION, TIER, QUEUE] ) for batch in range(i, i + NUM_THREADS) ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    i += NUM_THREADS

end = time.process_time()

summoner_objs = [ Summoner.from_json( summ ) for summ in summoners if type( summ ) != str ]
print(f'{len(summoner_objs)} summoners collected in {end-start}s')

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
