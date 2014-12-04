from collections import Counter
from operator import truediv
import csv
import p1_parse as p
import numpy as np
from bookedmoves import BELLHOP_ORDER

TICKET_FILE = "../data/report-feed-export-2014-10-20-1657-429105d970-v2.csv"

ticket_data = p.parse(TICKET_FILE, ",")
order_file = p.parse(BELLHOP_ORDER, ",")
begin_date = raw_input("Start date: ")
end_date = raw_input("End date: ")

def difficult_moves():
	""" Creates lists of order numbers for each difficult move """
	bedroom_3plus_app_false = []
	bedroom_3_app_false = []
	bedroom_3plus_app_true = []
	bedroom_3_app_true = []
	bedroom_2_app_true = []
	app_true = []
	app_false = []
	bedroom_3plus_app_false_duration = []
	bedroom_3_app_false_duration = []
	bedroom_3plus_app_true_duration = []
	bedroom_3_app_true_duration = []
	bedroom_2_app_true_duration = []
	app_true_duration = []
	app_false_duration = []

	for ticket in ticket_data:
		split_sub = ticket['Subject'].split()
		if range(len(split_sub)) > range(0,2):
			if (split_sub[0] +' '+ split_sub[1]) == 'Difficult Move:':
				if split_sub[5] == 'True':
					app_true.append(split_sub[2])
					if split_sub[8] == '2':
						bedroom_2_app_true.append(split_sub[2])
					elif split_sub[8] == '3':
						bedroom_3_app_true.append(split_sub[2])
					elif split_sub[8] == '3+':
						bedroom_3plus_app_true.append(split_sub[2])
				elif split_sub[5] == 'False':
					app_false.append(split_sub[2])
					if split_sub[8] == '3':
						bedroom_3_app_false.append(split_sub[2])
					elif split_sub[8] == '3+':
						bedroom_3plus_app_false.append(split_sub[2])
	print app_true
	for item in order_file:
		if (item['charges_verified'] == "Yes" and item['move_date'] >= begin_date 
			and item['move_date'] <= end_date and item['deposit_paid'] != '' and item['bellhops_assigned'] != "0"
			and item['billable_duration'] != ''):
			if item['number'] in bedroom_3plus_app_false:
				bedroom_3plus_app_false_duration.append(float(item['billable_duration'])/float(item['bellhops_assigned']))
			elif item['number'] in bedroom_3_app_false:
				bedroom_3_app_false_duration.append(float(item['billable_duration'])/float(item['bellhops_assigned']))
			elif item['number'] in bedroom_3plus_app_true:
				bedroom_3plus_app_true_duration.append(float(item['billable_duration'])/float(item['bellhops_assigned']))
			elif item['number'] in bedroom_3_app_true:
				bedroom_3_app_true_duration.append(float(item['billable_duration'])/float(item['bellhops_assigned']))
			elif item['number'] in bedroom_2_app_true:
				bedroom_2_app_true_duration.append(float(item['billable_duration'])/float(item['bellhops_assigned']))
			elif item['number'] in app_true:
				app_true_duration.append(float(item['billable_duration'])/float(item['bellhops_assigned']))
			elif item['number'] in app_false:
				app_false_duration.append(float(item['billable_duration'])/float(item['bellhops_assigned']))

	print app_true_duration
	bedroom_3plus_app_false_avg_duration = np.average(bedroom_3plus_app_false_duration)
	bedroom_3_app_false_avg_duration = np.average(bedroom_3_app_false_duration)
	bedroom_3plus_app_true_avg_duration = np.average(bedroom_3plus_app_true_duration)
	bedroom_3_app_true_avg_duration = np.average(bedroom_3_app_true_duration)
	bedroom_2_app_true_avg_duration = np.average(bedroom_2_app_true_duration)
	app_true_avg_duration = np.average(app_true_duration)
	app_false_avg_duration = np.average(app_false_duration)

	print app_true_avg_duration

	print "----------"*5
	print "Average Durations From %s to %s: " % (begin_date, end_date)
	print "----------"*5
	print "Difficult Moves with Appliances: %.2f minutes" % (app_true_avg_duration)
	print "Difficult Moves without Appliances: %.2f minutes" % (app_false_avg_duration)
	print "----------"*5
	print "3+ Bedrooms / No Appliances: %.2f minutes" % (bedroom_3plus_app_false_avg_duration)
	print "3+ Bedrooms / With Appliances: %.2f minutes" % (bedroom_3plus_app_true_avg_duration)
	print "3 Bedrooms / No Appliances: %.2f minutes" % (bedroom_3_app_false_avg_duration)
	print "3 Bedrooms / With Appliances: %.2f minutes" % (bedroom_3_app_true_avg_duration)
	print "2 Bedrooms / With Appliances: %.2f minutes" % (bedroom_2_app_true_avg_duration)


def main():
	difficult_moves()


if __name__ == "__main__":
	main()
