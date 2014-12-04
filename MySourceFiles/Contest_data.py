from collections import Counter
from operator import truediv
import csv
import p1_parse as p
from bookedmoves import BELLHOP_ORDER


TICKET_FILE = "../data/report-feed-export-2014-10-11-1802-429105d99e-v2.csv"

order_file = p.parse(BELLHOP_ORDER, ",")
begin_date = raw_input("Start date (yyyy-mm-dd): ")
end_date = raw_input("End date (yyyy-mm-dd): ")


def create_contested_order_list():
	contest_file = p.parse(TICKET_FILE, ",")
	contested_orders = []
	for ticket in contest_file:
		split_sub = ticket["Subject"].split()
		if range(len(split_sub)) > range(0,3) and ticket["Created at"] > "2014-10-01 08:00":	
			if split_sub[0] == 'Contested:':
				contested_orders.append(split_sub[1])
			elif split_sub[3] == 'contesting':
				contested_orders.append(split_sub[7])
	return contested_orders

contested_order_list = create_contested_order_list()


def verified_moves_count():
	counter2 = Counter(item["charges_verified"] for item in order_file if item["move_date"] >= begin_date 
		and item["move_date"] <= end_date)
	moves_verified = counter2["Yes"]
	return float(moves_verified)


def moves_booked_online():
	counter = Counter(item["booked_by"] == '' for item in order_file if item["booked_at_date"] >= begin_date 
		and item["booked_at_date"] <= end_date and item['deposit_paid'] != '')
	online_moves = counter[True]
	return float(online_moves)


def num_online_orders_contested():
	counter2 = Counter(item["booked_by"] == '' for item in order_file if item['deposit_paid'] != '' and item["number"] in contested_order_list)
	ol_contest = float(counter2[True])
	return ol_contest


def online_moves_contested():
	counter2 = Counter(item["booked_by"] == '' for item in order_file if item['deposit_paid'] != '' and item["number"] in contested_order_list)
	counter = Counter(item["booked_by"] == '' for item in order_file if item["move_date"] >= begin_date 
		and item["move_date"] <= end_date and item['deposit_paid'] != '' and item["charges_verified"] == "Yes")
	online_moves = counter[True]
	online_contest = counter2[True]
	online_contest_percentage = (float(float(online_contest) / float(online_moves)) * 100)
	return float(online_contest_percentage)


def truck_moves():
	counter = Counter(item["truck_required"] == "Yes" for item in order_file if item['move_date'] >= begin_date 
		and item['move_date'] <= end_date and item['deposit_paid'] != '' and item["charges_verified"] == 'Yes'
		and item['state'] == 'NM')
	truck_list = float(counter[True])

	return truck_list


def truck_move_contests():
	counter = Counter(item["truck_required"] == "Yes" for item in order_file if item["booked_at_date"] >= begin_date 
		and item["booked_at_date"] <= end_date and item['deposit_paid'] != '' and item["charges_verified"] == "Yes"
		and item["number"] in contested_order_list)
	contested_truck_moves = float(counter[True])
	return contested_truck_moves


def moves_booked_by_csr():
	counter = Counter(item["booked_by"] == '' for item in order_file if item["booked_at_date"] >= begin_date 
		and item["booked_at_date"] <= end_date and item['deposit_paid'] != '')
	csr_moves = counter[False]
	return float(csr_moves)


def contested_moves_per_csr():
	counter2 = Counter(item["booked_by"] for item in order_file if item['deposit_paid'] != '' and item["number"] in contested_order_list)
	counter = Counter(item["booked_by"] for item in order_file if item["booked_at_date"] >= begin_date 
		and item["booked_at_date"] <= end_date and item['deposit_paid'] != '' and item["charges_verified"] == "Yes")

	booked_list = [
					counter["matt.intemann@gmail.com"],
					counter["joey.doughty@getbellhops.com"],
					counter["branton.phillips@getbellhops.com"],
					counter["bj@getbellhops.com"],
					counter["charles.marczynski@getbellhops.com"],
					]

	contest_count = [
					 counter2["matt.intemann@gmail.com"],
					 counter2["joey.doughty@getbellhops.com"],
					 counter2["branton.phillips@getbellhops.com"],
					 counter2["bj@getbellhops.com"],
					 counter2["charles.marczynski@getbellhops.com"],
					 ]

	csr_contest_percentage = map(truediv, contest_count, booked_list)
	return csr_contest_percentage


def main():
	online_moves_booked = float(moves_booked_online())
	verified_moves = float(verified_moves_count())
	contested_orders = float(len(create_contested_order_list()))
	percent_of_orders_contested = 100 * float(float(contested_orders) / float(verified_moves))
	num_csr_moves = float(moves_booked_by_csr())
	csr_contest = contested_moves_per_csr()
	num_ol_contest = float(num_online_orders_contested())
	online_contest = float(online_moves_contested())
	number_of_truck_moves = float(truck_moves())
	truck_moves_contested = float(truck_move_contests())
	num_csr_contest = float(contested_orders - num_ol_contest)
	print
	print
	print "---" * 20
	print "CONTESTED MOVE DATA FROM %s TO %s " % (begin_date, end_date)
	print "---" * 20
	print
	print "Number of Verified Orders:    	  %.2f " % verified_moves
	print "Number of Contested Orders:        %.2f " % contested_orders
	print "Percent of Total Orders Contested: %.2f " % percent_of_orders_contested
	print 
	print "---" * 20
	print "CSR DATA"
	print "---" * 20
	print
	print "PERCENT OF MOVES BOOKED THAT ARE CONTESTED:"
	print "\tIce Contest Percentage:     %.2f " % float(csr_contest[0] * 100)
	print "\tJoey Contest Percentage:    %.2f " % float(csr_contest[1] * 100)
	print "\tBranton Contest Percentage: %.2f " % float(csr_contest[2] * 100)
	print "\tBJ Contest Percentage:      %.2f " % float(csr_contest[3] * 100)
	print "\tChuck Contest Percentage:   %.2f " % float(csr_contest[4] * 100)
	print
	print "Number of Moves Booked Over the Phone (not online): %.2f " % num_csr_moves
	print "Number of CSR Bookings Contested: %.2f " % num_csr_contest
	print "Percent of Verified Orders Booked Over the Phone: %.2f " % float((num_csr_moves / verified_moves) * 100)
	print "Percent of Orders Contested"
	print "\tWhen Booked by CSR: %.2f " % float((num_csr_contest / num_csr_moves) * 100)
	print "Phones- Percent of Total Contested Orders: %.2f " % float((num_csr_contest / contested_orders) *100)
	print
	print "---" * 20
	print "ONLINE DATA"
	print "---" * 20
	print 
	print "Number of Orders Booked Online: %.2f " % online_moves_booked
	print "Number of Contested Orders Booked Online: %.2f " % num_ol_contest
	print "Percent of Verified Orders Booked Online: %.2f " % float((online_moves_booked / verified_moves) * 100)
	print "Percent of Orders Contested When Booked Online: %.2f " % online_contest
	print "Online- Percent of Total Contested Orders: %.2f " % float((num_ol_contest / contested_orders) *100)



if __name__ == "__main__":
	main()

