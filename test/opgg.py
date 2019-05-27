
import requests, sys, time, json, os
from threading import Thread

from pyquery import PyQuery as pq

def scrape( summoner ):


    d = pq( url=BASE_PATH + summoner  )
    cs = d('div.GameItemList div.GameItem div.Content div.Stats div.CS span').text()

    global infos
    infos.append( {'summonerName': summoner, 'cs': cs} )

NUM_THREADS = os.cpu_count() if os.cpu_count() else 2
BASE_PATH = 'https://na.op.gg/summoner/userName='
PAGE_LENGTH = NUM_THREADS * 10

with open( './data/leaguers.txt', 'r' ) as f:

    summoners = json.load( f )
    infos = []
    threads = [ None ]

    start = time.process_time()

    i = j = 0
    while len(threads) > 0 and i < PAGE_LENGTH:

        threads = []

        if j < len( summoners ):
            for n in range( NUM_THREADS ):
                threads.append( Thread( target=scrape, args=[ summoners[i + n]['summonerName']  ] ) )
                j += 1

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        i += NUM_THREADS

    end = time.process_time()

    print(f'Collected info about {len(infos)} summoners in {end-start}s')

    start = time.process_time()
    f = open( './data/infos.txt', 'w+' )
    f.write( f"{ json.dumps( infos, indent=3 ) }" )
    f.close()
    end = time.process_time()
    print(f'Data written in {end-start}s')
