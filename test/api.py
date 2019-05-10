
import requests, sys, time, json
from threading import Thread
import multiprocessing as mp

def get_summs( batch ):

    if len(sys.argv) < 3:
        print('Usage: python api.py <DIVISION> <TIER [I-IV]> [QUEUE]')
        sys.exit(0)

    DIVISION  = sys.argv[1]
    TIER = sys.argv[2]
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

summoners = []

i = 1
while i < 150:

    time.sleep(2)

    threads = [ Thread( target=get_summs, args=[batch] ) for batch in range(i, i + 12) ]

    start = time.process_time()

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    end = time.process_time()

    i += 12

print(f'{len(summoners)} summoners collected in {end-start}s')
f = open( './data/leaguers.txt', 'w+' )
f.writelines( f"{json.dumps( player, indent=3 )}\n" for player in summoners )
f.close()
