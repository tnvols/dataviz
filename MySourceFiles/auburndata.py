from collections import Counter
from operator import truediv
import datetime
import csv
import p1_parse as p
from bookedmoves import BELLHOP_ORDER

BELLHOP_PROFILES = "../data/2014_10_15_2336_bellhops_export.csv"

order_file = p.parse(BELLHOP_ORDER, ",")
bellhops_file = p.parse(BELLHOP_PROFILES, ',')
begin_date = "2014-08-15"
end_date = "2014-10-28"


def movers_in_cities(market_input):
	unique_hops = set()
	for item in order_file:
		markets = item['market']+','+' '+item['state']
		if (item['charges_verified'] == "Yes" and item['move_date'] >= begin_date
		    and item['move_date'] <= end_date and item['deposit_paid'] != ''
		    and markets == market_input and item['bellhops_assigned'] != ''
		    and item['bellhops_assigned'] > '0'):
			unique_hops.add(item['captain'])
			wing_list = item['wingmen'].split()
			for i in wing_list:
				unique_hops.add(i)
	total = len(unique_hops)
	return total

def two_movers(market_input):
	unique_hops = []
	three = set()
	for item in order_file:
		markets = item['market']+','+' '+item['state']
		if (item['charges_verified'] == "Yes" and item['move_date'] >= begin_date
		    and item['move_date'] <= end_date and item['deposit_paid'] != ''
		    and markets == market_input and item['bellhops_assigned'] != ''
		    and item['bellhops_assigned'] > '0'):
			unique_hops.append(item['captain'])
			wing_list = item['wingmen'].split()
			for i in wing_list:
				unique_hops.append(i)
	for i in unique_hops:
		if unique_hops.count(i) >= 5:
			three.add(i)
	num_worked_three = len(three)
	orgs_list = []
	major_list = []
	hired = []
	emails = []
	for bellhop in bellhops_file:
		if bellhop['user__email'] in three and bellhop['employment_status'] == 'approved':
			emails.append(bellhop['user__email'])
	org = sorted(orgs_list)
	major = sorted(major_list)
	hire = sorted(hired)
	email = sorted(emails)

	print '----------'*5
	print '%s Hop Data from %s to %s' % (market_input, begin_date, end_date)
	print '----------'*5
	#print 'Number of Hops that worked 1 job and stopped: %d' % num_worked_three
	#print 'Organizations these hops were/are in:'
	#print org
	#print 'Majors of these hops:'
	#print major
	#print 'Dates these hops were hired:'
	#print hire
	#print
	for i in email:
		print i


def hop_market_data(market_input):
	unique_hops = []
	working = set()
	for item in order_file:
		markets = item['market']+','+' '+item['state']
		if (item['charges_verified'] == "Yes" and item['move_date'] >= begin_date
		    and item['move_date'] <= end_date and item['deposit_paid'] != ''
		    and markets == market_input and item['bellhops_assigned'] != ''
		    and item['bellhops_assigned'] > '0'):
			unique_hops.append(item['captain'])
			working.add(item['captain'])
			wing_list = item['wingmen'].split()
			for i in wing_list:
				unique_hops.append(i)
				working.add(i)
	for it in working:
		print it, unique_hops.count(it)



def market_moves(market_input):
	vm_counter = Counter(item['charges_verified'] == "Yes" for item in order_file if item['move_date'] >= begin_date 
		and item['move_date'] <= end_date and item['deposit_paid'] != '' and item['market']+','+' '+item['state'] == market_input)
	verified_moves = float(vm_counter[True])
	external_counter = Counter(item['charges_verified'] == "Yes" for item in order_file if item['move_date'] >= begin_date 
		and item['move_date'] <= end_date and item['deposit_paid'] == '' and item['market']+','+' '+item['state'] == market_input)
	external_moves = float(external_counter[True])
	total_moves = int(verified_moves + external_moves)

	print "%d" % (total_moves)
	#print "Household: %.2f" % verified_moves
	#print "Externally Billed: %.2f" % external_moves
	#print "Total Moves: %.2f" % total_moves


def hop_data(market_in):
	em = []
	for bellhop in bellhops_file:
		if (bellhop['employment_status'] == 'approved' and market_in == bellhop['market']
			or bellhop['employment_status'] == 'terminated' and market_in == bellhop['market']):
			em.append(bellhop['user__email'])
	num_hops = len(em)
	print "%s %d" % (market_in, num_hops)


def market_list():
	mkts = set()
	hop_mkts = set()
	for item in order_file:
		mkts.add(item['market']+','+' '+item['state'])
	for bellhop in bellhops_file:
		hop_mkts.add(bellhop['market'])
	marks = sorted(hop_mkts)
	mark = sorted(mkts)
	for market in mark:
		#market_moves(market)
		two_movers(market)
		#hop_market_data(market)
	#for m in marks:
		#hop_data(m)
	

def main():
	market_list()
	#hop_market_data("Austin, TX")
	#hop_market_data("Auburn, AL")
	#hop_market_data("Athens, GA")

if __name__ == "__main__":
	main()
