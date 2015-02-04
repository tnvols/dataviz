from collections import Counter

import p1_parse as p
import numpy as np
from bookedmoves import BELLHOP_ORDER

TICKET_FILE = "../data/report-feed-export-2015-01-02-1334-429105d638-v2.csv"

ticket_data = p.parse(TICKET_FILE, ",")
order_file = p.parse(BELLHOP_ORDER, ",")
begin_date = "2014-10-17"
end_date = "2014-12-15"


def difficult_moves():
	""" Creates lists of order numbers for each difficult move """
	diff_move = []
	bedroom_3plus_app_true = []
	bedroom_2_app_true = []
	bedroom_1_app_true = []
	app_true = []
	app_false = []
	bedroom_3plus_app_true_duration = []
	bedroom_2_app_true_duration = []
	bedroom_1_app_true_duration = []
	app_true_duration = []
	app_false_duration = []
	diff_move_dura = []
	diff_move_total_dura = []
	with_app_dura = []
	without_app_dura = []
	three_plus_hops_no_assigned = []
	three_plus_app_hops_assigned = []
	diff_move_hops_assigned = []
	all_move_durations =[]
	all_move_hops = []

	for ticket in ticket_data:
		split_sub = ticket['Subject'].split()
		if range(len(split_sub)) > range(0, 2):
			if (split_sub[0] + ' ' + split_sub[1]) == 'Difficult Move:':
				diff_move.append(split_sub[2])
				if split_sub[5] == 'True':
					app_true.append(split_sub[2])
					if split_sub[8] == '2':
						bedroom_2_app_true.append(split_sub[2])
					elif split_sub[8] == '1':
						bedroom_1_app_true.append(split_sub[2])
					elif split_sub[8] == '3+':
						bedroom_3plus_app_true.append(split_sub[2])
					else:
						pass
				elif split_sub[5] == 'False':
					app_false.append(split_sub[2])
	
	for item in order_file:
		if (
			item['charges_verified'] == "Yes" and item['move_date'] >= begin_date
			and item['move_date'] <= end_date and item['deposit_paid'] != '' and item['actual_duration'] != '' and item['bellhops_assigned'] != ''):
			difference = (float(item['actual_duration']) / float(item['bellhops_assigned'])) - float(item['estimated_duration'])
			act_dura = float(item['actual_duration']) / float(item['bellhops_assigned'])
			all_move_durations.append(act_dura)
			all_move_hops.append(float(item['bellhops_assigned']))
			if difference > 0:
				if item['number'] in diff_move:
					diff_move_dura.append(difference)
					diff_move_total_dura.append(act_dura)
					diff_move_hops_assigned.append(float(item['bellhops_assigned']))
				if item['number'] in app_true:
					app_true_duration.append(difference)
				if item['number'] in app_false:
					app_false_duration.append(difference)
					without_app_dura.append(act_dura)
					three_plus_hops_no_assigned.append(float(item['bellhops_assigned']))
				if item['number'] in bedroom_3plus_app_true:
					bedroom_3plus_app_true_duration.append(difference)
					with_app_dura.append(act_dura)
					three_plus_app_hops_assigned.append(float(item['bellhops_assigned']))
				if item['number'] in bedroom_2_app_true:
					bedroom_2_app_true_duration.append(difference)
				if item['number'] in bedroom_1_app_true:
					bedroom_1_app_true_duration.append(difference)

	bedroom_3plus_app_true_avg_duration = np.average(bedroom_3plus_app_true_duration)
	bedroom_2_app_true_avg_duration = np.average(bedroom_2_app_true_duration)
	bedroom_1_app_true_avg_duration = np.average(bedroom_1_app_true_duration)
	app_true_avg_duration = np.average(app_true_duration)
	app_false_avg_duration = np.average(app_false_duration)
	diff_move_total_avg_dura = np.average(diff_move_total_dura) / 60
	with_app_avg_dura = np.average(with_app_dura) / 60
	without_app_avg_dura = np.average(without_app_dura) / 60
	avg_hops_no = np.average(three_plus_hops_no_assigned)
	avg_hops_yes = np.average(three_plus_app_hops_assigned)
	avg_hops_diff = np.average(diff_move_hops_assigned)
	all_move_avg_dura = np.average(all_move_durations) / 60
	all_move_avg_hops = np.average(all_move_hops)

	vm_counter = Counter(item['charges_verified'] == "Yes" for item in order_file if item['move_date'] >= begin_date and item['move_date'] <= end_date and item['deposit_paid'] != '' and item['number'] in diff_move)
	verified_moves = float(vm_counter[True])

	vm_app_true_counter = Counter(item['charges_verified'] == "Yes" for item in order_file if item['move_date'] >= begin_date and item['move_date'] <= end_date and item['deposit_paid'] != '' and item['number'] in app_true)
	verified_app_moves = float(vm_app_true_counter[True])

	print verified_moves
	print len(diff_move)

	per_diff_move = (len(diff_move_dura) / verified_moves) * 100
	per_app_true = (len(app_true_duration) / verified_app_moves) * 100

	print "----------" * 5
	print "Underestimates From %s to %s: " % (begin_date, end_date)
	print "----------" * 5
	print "Percent of moves underestimated with difficult move ticket: %.2f%%" % (per_diff_move)
	print "Percent of moves underestimated with appliance on the move: %.2f%%" % (per_app_true)
	print "Average underestimate of difficult moves: %.2f" % (np.average(diff_move_dura))
	print "Difficult Moves with Appliances: %.2f minutes" % (app_true_avg_duration)
	print "Difficult Moves without Appliances: %.2f minutes" % (app_false_avg_duration)
	print "----------" * 5
	print "3+ Bedrooms / With Appliances: %.2f minutes" % (bedroom_3plus_app_true_avg_duration)
	print "2 Bedrooms / With Appliances: %.2f minutes" % (bedroom_2_app_true_avg_duration)
	print "1 Bedroom / With Appliances: %.2f minutes" % (bedroom_1_app_true_avg_duration)
	print "----------" * 5
	print "Actual duration all moves: %.2f hours" % all_move_avg_dura
	print "Average Hops for all moves: %.2f" % all_move_avg_hops
	print "Actual duration of all diff. moves: %.2f hours with %.2f hops" % (diff_move_total_avg_dura, avg_hops_diff)
	print "Actual duration of 3+ bed diff. moves with appliances: %.2f hours with %.2f hops" % (with_app_avg_dura, avg_hops_yes)
	print "Actual duration of 3+ bed diff. moves without appliances: %.2f hours with %.2f hops" % (without_app_avg_dura, avg_hops_no)


def main():
	difficult_moves()


if __name__ == "__main__":
	main()
