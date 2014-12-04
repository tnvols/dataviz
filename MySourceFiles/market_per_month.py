from collections import Counter
import csv
import numpy as np
import p1_parse as p
from bookedmoves import BELLHOP_ORDER


order_file = p.parse(BELLHOP_ORDER, ",")
begin_date = raw_input("Start date: ")
end_date = raw_input("End date: ")
jan_st = "2014-01-01"
jan_end = "2014-01-31"
feb_st = "2014-02-01"
feb_end = "2014-02-28"
mar_st = "2014-03-01"
mar_end = "2014-03-31"
apr_st = "2014-04-01"
apr_end = "2014-04-30"
may_st = "2014-05-01"
may_end = "2014-05-31"
june_st = "2014-06-01"
june_end = "2014-06-30"
july_st = "2014-07-01"
july_end = "2014-07-31"
aug_st = "2014-08-01"
aug_end = "2014-08-31"
sep_st = "2014-09-01"
sep_end = "2014-09-30"
oct_st = "2014-10-01"
oct_end = "2014-10-15"


def market_rev(market_input):
	spots = []
	for item in order_file:
		if (item['move_date'] >= begin_date and item['move_date'] <= end_date
			and item['charges_verified'] == 'Yes' and item['market']+','+' '+item['state'] == market_input)

	
	total_spots = verified_moves + external_moves

	print "%s %d" % (market_input, total_moves)



def main():
	market_rev("Austin, TX")
	market_rev("Auburn, AL")
	market_rev("Athens, GA")
 	
if __name__ == "__main__":
	main()