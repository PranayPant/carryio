
from selenium import webdriver
import time

options = webdriver.ChromeOptions()
options.add_argument('headless')
browser = webdriver.Chrome( executable_path='/Users/p0p007i/Documents/chromedriver', options=options )

#browser.get('https://na.op.gg/ranking/ladder/')

PLAYERS_SELECTOR = 'table.ranking-table tbody tr.ranking-table__row td.ranking-table__cell a span'
NEXT_PAGE_SELECTOR = lambda page: f'div.ranking-pagination ul li.ranking-pagination__item:nth-of-type({page}) a'

summoners = []

start = time.perf_counter_ns()
for i in range( 1, 100 ):
	browser.get( f'https://na.op.gg/ranking/ladder/page=1' )
	players = [ p.text for p in browser.find_elements_by_css_selector( PLAYERS_SELECTOR ) ]
	summoners.extend( players )
	#browser.find_element_by_css_selector( NEXT_PAGE_SELECTOR(i) ).send_keys("\n")
end = time.perf_counter_ns()

print( f"Completed in {len(summoners)} players in {str( max(1, (end-start)/1000000000) ) }s \
({ len(summoners) // int((end-start)/1000000000) } players/s)" )
print( summoners )

browser.close()
