from collections import Counter

import p1_parse as p
import locale
from bookedmoves import BELLHOP_ORDER

order_file = p.parse(BELLHOP_ORDER, ",")
begin_date = "2014-01-01"
end_date = "2014-12-03"
#market_input = raw_input("Market(ex. Chattanooga, TN): ")

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')


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

	#print "%s %.2f %.2f %.2f %.2f %.2f" % (market_input, total_moves, hh_rev, ext_rev, total_rev, director_rev)

	print "-----------" *10
	print "MOVE & REVENUE DATA FOR %s FROM %s to %s" % (market_input, begin_date, end_date)
	print "-----------" *10
	print "Number of Household Moves: %.2f" % verified_moves
	print "Number of Commercial Moves: %.2f" % external_moves
	print "Total Number of Moves: %.2f" % total_moves
	print "-----------" *2
	print "Household Revenue: " + locale.currency(hh_rev, grouping=True)
	print "Commercial Revenue: " + locale.currency(ext_rev, grouping=True)
	print "Total Revenue: " + locale.currency(total_rev, grouping=True)
	print "Total Estimated Director Payout: " + locale.currency(director_rev, grouping=True)


def market_rev_totals():
	household = []
	external = []
	vm_counter = Counter(item['charges_verified'] == "Yes" for item in order_file if item['move_date'] >= begin_date 
		and item['move_date'] <= end_date and item['deposit_paid'] != '')
	verified_moves = float(vm_counter[True])
	external_counter = Counter(item['charges_verified'] == "Yes" for item in order_file if item['move_date'] >= begin_date 
		and item['move_date'] <= end_date and item['deposit_paid'] == '')
	external_moves = float(external_counter[True])
	for item in order_file:
		if (item['charges_verified'] == "Yes" and item['move_date'] >= begin_date
		    and item['move_date'] <= end_date and item['deposit_paid'] != ''):
			household.append(float(item['total_paid_by_customer']))
		elif (item['charges_verified'] == "Yes" and item['move_date'] >= begin_date
		    and item['move_date'] <= end_date and item['deposit_paid'] == ''
		    and item['remaining_balance'] != '' and item['remaining_balance'] >'0'):
			external.append(float(item['total_payouts_to_bellhops']) * 2.14)

	total_moves = verified_moves + external_moves 	
	hh_rev = sum(household)
	ext_rev = sum(external)
	total_rev = hh_rev + ext_rev
	director_rev = (total_rev * .01)

	print "-----------" *10
	print "MOVE & REVENUE DATA FOR FROM %s to %s" % (begin_date, end_date)
	print "-----------" *10
	print "Number of Household Moves: %.2f" % verified_moves
	print "Number of Commercial Moves: %.2f" % external_moves
	print "Total Number of Moves: %.2f" % total_moves
	print "-----------" *2
	print "Household Revenue: %.2f" % hh_rev
	print "Commercial Revenue: %.2f" % ext_rev
	print "Total Revenue: %.2f" % total_rev
	print "Total Estimated Director Payout: %.2f" % director_rev


def market_list():
	mkts = set()
	for item in order_file:
		mkts.add(item['market']+','+' '+item['state'])
	mark = sorted(mkts)
	for market in mark:
		market_rev(market)


def total_rev():
	household = []
	phone_order = []
	vm_counter = Counter(item['charges_verified'] == "Yes" for item in order_file if item['move_date'] >= begin_date 
		and item['move_date'] <= end_date and item['deposit_paid'] != '')
	verified_moves = float(vm_counter[True])
	pm_counter = Counter(item['charges_verified'] == "Yes" for item in order_file if item['move_date'] >= begin_date 
		and item['move_date'] <= end_date and item['deposit_paid'] != '' and item['booked_by'] != '')
	phone_moves = float(pm_counter[True])
	for item in order_file:
		if (item['charges_verified'] == "Yes" and item['move_date'] >= begin_date
		    and item['move_date'] <= end_date and item['deposit_paid'] != '' and item['booked_by'] != ''):
			phone_order.append(float(item['total_paid_by_customer']))
		if (item['charges_verified'] == "Yes" and item['move_date'] >= begin_date
		    and item['move_date'] <= end_date and item['deposit_paid'] != ''):
			household.append(float(item['total_paid_by_customer']))


	phone = phone_moves
	hh_rev = sum(household)
	phone_rev = sum(phone_order)


	print "-----------" *10
	print "Household Revenue Data From %s to %s" % (begin_date, end_date)
	print "-----------" *10
	print "Number of Household Moves: %.2f" % verified_moves
	print "Number of Phone orders: %.2f" % phone
	print "-----------" *2
	print "Household Revenue: %.2f" % hh_rev
	print "Revenue From Phone Bookings: %.2f" % phone_rev


def main():
	#market_list()
	#total_rev()
	market_rev_totals()
 	
if __name__ == "__main__":
	main()




			





