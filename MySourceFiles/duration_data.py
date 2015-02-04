from collections import Counter

import numpy as na
import p1_parse as p

BELLHOP_ORDER = "../data/2014_12_15_1316_bellhops_order_export.csv"
TICKET_FILE = "../data/report-feed-export-2015-01-02-1334-429105d638-v2.csv"

ticket_data = p.parse(TICKET_FILE, ",")
order_file = p.parse(BELLHOP_ORDER, ",")
begin_date = "2014-10-01"
end_date = "2014-12-15"


def one_hop_one_hour():
	one_hop_one_hr = []
	for item in order_file:
		if (
			item['charges_verified'] == "Yes" and item['move_date'] >= begin_date
			and item['move_date'] <= end_date and item['billable_duration'] == '60'
			and item['bellhops_assigned'] == '1'):

			one_hop_one_hr.append(item['number'])
	print one_hop_one_hr
	short_moves = len(one_hop_one_hr)

	vm_counter = Counter(item['charges_verified'] == "Yes" for item in order_file if item['move_date'] >= begin_date and item['move_date'] <= end_date and item['deposit_paid'] != '')
	verified_moves = float(vm_counter[True])
	external_counter = Counter(item['charges_verified'] == "Yes" for item in order_file if item['move_date'] >= begin_date and item['move_date'] <= end_date and item['deposit_paid'] == '')
	external_moves = float(external_counter[True])

	total_moves = verified_moves + external_moves

	per_short_moves = (short_moves / total_moves) * 100

	print '%d, %d, %.2f%%' % (short_moves, total_moves, per_short_moves)


def over_estimated_orders():
	total_estimation_difference = []
	totals_order_number = []
	phone_estimation = []
	online_estimation = []
	contested_orders = []

	for item in order_file:
		if (
			item['charges_verified'] == "Yes" and item['move_date'] >= begin_date
			and item['move_date'] <= end_date and item['deposit_paid'] != '' and item['actual_duration'] != '' and item['bellhops_assigned'] != ''):
			difference = (float(item['actual_duration']) / float(item['bellhops_assigned'])) - float(item['estimated_duration'])
			if difference > 30.0:
				total_estimation_difference.append(difference)
				totals_order_number.append(item['number'])
			if item['booked_by'] != '' and difference > 30.0:
				phone_estimation.append(difference)
			if item['booked_by'] == '' and difference > 30.0:
				online_estimation.append(difference)

	for ticket in ticket_data:
		split_sub = ticket["Subject"].split()
		if range(len(split_sub)) > range(0, 3) and ticket["Created at"] > "2014-10-01 08:00":
			if split_sub[0] == 'Contested:':
				contested_orders.append(split_sub[1])
			elif split_sub[3] == 'contesting':
				contested_orders.append(split_sub[7])

	avg_under_estimate = na.average(total_estimation_difference)
	avg_phone_estimate = na.average(phone_estimation)
	avg_online_estimate = na.average(online_estimation)

	vm_counter = Counter(item['charges_verified'] == "Yes" for item in order_file if item['move_date'] >= begin_date and item['move_date'] <= end_date and item['deposit_paid'] != '')
	verified_moves = float(vm_counter[True])

	phone_vm_counter = Counter(item['charges_verified'] == "Yes" for item in order_file if item['move_date'] >= begin_date and item['move_date'] <= end_date and item['deposit_paid'] != '' and item['booked_by'] != '')
	phone_verified_moves = float(phone_vm_counter[True])

	online_vm_counter = Counter(item['charges_verified'] == "Yes" for item in order_file if item['move_date'] >= begin_date and item['move_date'] <= end_date and item['deposit_paid'] != '' and item['booked_by'] == '')
	online_verified_moves = float(online_vm_counter[True])

	contested_vm_counter = Counter(item['charges_verified'] == "Yes" for item in order_file if item['move_date'] >= begin_date and item['move_date'] <= end_date and item['deposit_paid'] != '' and item['number'] in contested_orders)
	contested_verified_moves = float(contested_vm_counter[True])

	contested_est_vm_counter = Counter(item['charges_verified'] == "Yes" for item in order_file if item['move_date'] >= begin_date and item['move_date'] <= end_date and item['deposit_paid'] != '' and item['number']in contested_orders and item['number'] in totals_order_number)
	contested_est_verified_moves = float(contested_est_vm_counter[True])

	per_move_underestimated = (len(total_estimation_difference) / verified_moves) * 100
	per_phone_order_underestimate = (len(phone_estimation) / phone_verified_moves) * 100
	per_online_order_underestimate = (len(online_estimation) / online_verified_moves) * 100
	per_contested_verified_moves = (contested_est_verified_moves / contested_verified_moves) * 100
	
	print '%.2f, %.2f%%, %.2f, %.2f%%, %.2f, %.2f%%, %.2f%%' % (avg_under_estimate, per_move_underestimated, avg_phone_estimate, per_phone_order_underestimate, avg_online_estimate, per_online_order_underestimate, per_contested_verified_moves)
	print '%.2f, %.2f, %.2f, %d, %d, %d' % (verified_moves, contested_verified_moves, contested_est_verified_moves, len(total_estimation_difference), len(phone_estimation), len(online_estimation))


def main():
	#one_hop_one_hour()
	over_estimated_orders()


if __name__ == "__main__":
	main()
