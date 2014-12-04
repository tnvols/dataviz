from collections import Counter

import csv
import matplotlib.pyplot as plt
import numpy as na
import p1_parse as p
from bookedmoves import BELLHOP_ORDER


def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%.2f'%float(height),
                ha='center', va='bottom')

def moves_per_hour_worked_by_csr():
	order_file = p.parse(BELLHOP_ORDER, ",")
	begin_date = raw_input("Start date: ")
	end_date = raw_input("End date: ")
	ice_hours = raw_input("Ice Hours: ")
	joey_hours = raw_input("Joey Hours: ")
	bj_hours = raw_input("BJ Hours: ")
	chuck_hours = raw_input("Chuck Hours: ")
	jacob_hours = raw_input("Jacob Hours: ")
	justin_hours = raw_input("Justin Hours: ")
	tisha_hours = raw_input("Tisha Hours: ")
	olivia_hours = raw_input("Olivia Hours: ")
	aaron_hours = raw_input("Aaron Hours: ")
	stacy_hours = raw_input("Stacy Hours: ")

			
	counter = Counter(item["booked_by"] for item in order_file if item["booked_at_date"] >= begin_date 
		and item["booked_at_date"] <= end_date and item["deposit_paid"] != "" )

	booked_list = [
		(float(counter["matt.intemann@gmail.com"])/float(ice_hours)),
		(float(counter["joey.doughty@getbellhops.com"])/float(joey_hours)),
		(float(counter["bj@getbellhops.com"])/float(bj_hours)),
		(float(counter["charles.marczynski@getbellhops.com"])/float(chuck_hours)),
		(float(counter["jacob.ellis@getbellhops.com"])/float(jacob_hours)),
		(float(counter["justin.smith@getbellhops.com"])/float(justin_hours)),
		(float(counter["tisha.blankenship@getbellhops.com"])/float(tisha_hours)),
		(float(counter["olivia.moye@getbellhops.com"])/float(olivia_hours)),
		(float(counter["aaron.edmonson@getbellhops.com"])/float(aaron_hours)),
		(float(counter["stacy.scerini@getbellhops.com"])/float(stacy_hours))
	]
		
	csr_list = tuple(["Iceman", "Joey", "BJ", "Chuck", "Jacob", "Justin", "Tisha", "Olivia", "Aaron", "Stacy"])
	xlocations = na.array(range(len(csr_list))) + 0.5
	width = 0.5
	rects1 = plt.bar(xlocations, booked_list, width, color='green')
	plt.xticks(xlocations + width / 2, csr_list, rotation=90)	
	plt.subplots_adjust(bottom=0.2)
	plt.rcParams['figure.figsize'] = 12, 12
	plt.suptitle("Booked moves per hour worked from " + begin_date + " to " + end_date, fontsize=12)
	plt.ylabel("Booked Moves Per Hour Worked", fontsize=12)
	autolabel(rects1)
	plt.savefig("moves_per_hour_worked_by_csr.png")
	plt.clf()

def truck_moves():
	order_file = p.parse(BELLHOP_ORDER, ",")
	begin_date = raw_input("Start date: ")
	end_date = raw_input("End date: ")

	
	counter = Counter(item["truck_required"]for item in order_file if item["booked_at_date"] >= begin_date and item["booked_at_date"] <= end_date and item["cancelled"] != "Yes")
	counter2 = Counter(item["charges_verified"] for item in order_file if item["booked_at_date"] >= begin_date and item["booked_at_date"] <= end_date)
	
	truck_list = counter["Yes"]
	verified_moves = counter2["Yes"]

	print truck_list
	print verified_moves
	




def main():
	moves_per_hour_worked_by_csr()
	#truck_moves()

if __name__ == "__main__":
	main()