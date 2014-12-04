from collections import Counter
from operator import truediv
import datetime
import csv
import p1_parse as p
from bookedmoves import BELLHOP_ORDER

BELLHOP_PROFILES = "../data/2014_10_31_1752_bellhops_export.csv"

order_file = p.parse(BELLHOP_ORDER, ",")
bellhops_file = p.parse(BELLHOP_PROFILES, ',')


def time_before_first_job(hop_email):
	start_date = []
	moves = []
	unique_hops = []
	for item in order_file:
		if (item['charges_verified'] == "Yes" and item['deposit_paid'] != ''
		    and item['bellhops_assigned'] != '' and item['bellhops_assigned'] > '0'):
			unique_hops.append(item['captain'])
			wing_list = item['wingmen'].split()
			for i in wing_list:
				unique_hops.append(i)
	for bellhop in bellhops_file:
		if bellhop['user__email'] == hop_email:
			start_date.append(datetime.datetime.strptime(bellhop['created_at'], "%Y-%m-%d %H:%M:%S"))
	for item in order_file:
		if hop_email == item['captain'] or hop_email in item['wingmen']:
			moves.append(datetime.datetime.strptime(item['move_date'], "%Y-%m-%d"))
	sort_move = sorted(moves)
	if unique_hops.count(hop_email) >= 1:
		if len(sort_move) == 1 and len(start_date) > 0:
			td = sort_move[0] - start_date[0]
			print hop_email, unique_hops.count(hop_email), td.days
		if len(sort_move) == 2 and len(start_date) > 0:
			td = sort_move[0] - start_date[0]
			two = sort_move[1] - sort_move[0]
			print hop_email, unique_hops.count(hop_email), td.days, two.days
		if len(sort_move) == 3 and len(start_date) > 0:
			td = sort_move[0] - start_date[0]
			two = sort_move[1] - sort_move[0]
			three = sort_move[2] - sort_move[1]
			print hop_email, unique_hops.count(hop_email), td.days, two.days, three.days
		if len(sort_move) == 4 and len(start_date) > 0:
			td = sort_move[0] - start_date[0]
			two = sort_move[1] - sort_move[0]
			three = sort_move[2] - sort_move[1]
			four = sort_move[3] - sort_move[2]
			print hop_email, unique_hops.count(hop_email), td.days, two.days, three.days, four.days
		if len(sort_move) >= 5 and len(start_date) > 0:
			td = sort_move[0] - start_date[0]
			two = sort_move[1] - sort_move[0]
			three = sort_move[2] - sort_move[1]
			four = sort_move[3] - sort_move[2]
			five = sort_move[4] - sort_move[3]
			print hop_email, unique_hops.count(hop_email), td.days, two.days, three.days, four.days, five.days
		

			
				
					
						



def hops_who_have_worked():
	unique_hops = []
	workers = set()
	for item in order_file:
		if (item['charges_verified'] == "Yes" and item['deposit_paid'] != ''
		    and item['bellhops_assigned'] != '' and item['bellhops_assigned'] > '0'):
			unique_hops.append(item['captain'])
			wing_list = item['wingmen'].split()
			for i in wing_list:
				unique_hops.append(i)
	for i in unique_hops:
		if unique_hops.count(i) >= 1:
			workers.add(i)

	num_worked = len(workers)
	email_list = list(workers)

	for i in email_list:
		time_before_first_job(i)


def main():
	hops_who_have_worked()



if __name__ == "__main__":
	main()
