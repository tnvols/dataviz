from collections import Counter
import csv
import numpy as np
import p1_parse as p


BELLHOP_ORDER = "../data/2014_11_10_1323_bellhops_order_export.csv"

order_file = p.parse(BELLHOP_ORDER, ",")
begin_date = "2014-10-01"
end_date = "2014-10-31"


def market_rev(market_input):
	household = []
	external = []
	vm_counter = Counter(item['charges_verified'] == "Yes" for item in order_file if item['move_date'] >= begin_date 
		and item['move_date'] <= end_date and item['deposit_paid'] != '' and item['market']+','+' '+item['state'] == market_input)
	verified_moves = float(vm_counter[True])
	external_counter = Counter(item['charges_verified'] == "Yes" for item in order_file if item['move_date'] >= begin_date 
		and item['move_date'] <= end_date and item['deposit_paid'] == '' and item['market']+','+' '+item['state'] == market_input)
	external_moves = float(external_counter[True])
	for item in order_file:
		markets = item['market']+','+' '+item['state']
		if (item['charges_verified'] == "Yes" and item['move_date'] >= begin_date
		    and item['move_date'] <= end_date and item['deposit_paid'] != ''
		    and markets == market_input):
			household.append(float(item['total_paid_by_customer']))
		elif (item['charges_verified'] == "Yes" and item['move_date'] >= begin_date
		    and item['move_date'] <= end_date and item['deposit_paid'] == ''
		    and item['remaining_balance'] != '' and item['remaining_balance'] >'0' and markets == market_input):
			external.append(float(item['total_payouts_to_bellhops']) * 2.14)

	total_moves = verified_moves + external_moves
	hh_rev = sum(household)
	ext_rev = sum(external)
	total_rev = hh_rev + ext_rev
	director_rev = (total_rev * .01)
	avg_moves_per_week = total_moves/4

	#print "%s %.2f %.2f %.2f %.2f %.2f" % (market_input, total_moves, hh_rev, ext_rev, total_rev, director_rev)
	print "%s %.2f" % (market_input, avg_moves_per_week)


def market_list():
	mkts = set()
	for item in order_file:
		mkts.add(item['market']+','+' '+item['state'])
	mark = sorted(mkts)
	for market in mark:
		market_rev(market)



def main():
	market_list()

 	
if __name__ == "__main__":
	main()
