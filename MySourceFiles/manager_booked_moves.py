from collections import Counter

import csv
import matplotlib.pyplot as plt
import numpy as na
import p1_parse as p

BELLHOP_ORDER = "../data/2014_10_27_1210_bellhops_order_export.csv"

def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
                ha='center', va='bottom')

def booked_moves_by_csr():
	order_file = p.parse(BELLHOP_ORDER, ",")
	begin_date = raw_input("Start date: ")
	end_date = raw_input("End date: ")

			
	counter = Counter(item["booked_by"] for item in order_file if item["booked_at_date"] >= begin_date 
		and item["booked_at_date"] <= end_date and item["deposit_paid"] != "" )

	booked_list = [
		counter["matt.averyhart@getbellhops.com"],
		counter["matt.graves@getbellhops.com"]
	]
		
	csr_list = tuple(["Averyhart", "Graves"])
	xlocations = na.array(range(len(csr_list))) + 0.5
	width = 0.5
	rects1 = plt.bar(xlocations, booked_list, width, color='green')
	plt.xticks(xlocations + width / 2, csr_list, rotation=90)	
	plt.subplots_adjust(bottom=0.2)
	plt.rcParams['figure.figsize'] = 12, 12
	plt.suptitle("Booked Moves from " + begin_date + " to " + end_date, fontsize=12)
	plt.ylabel("Moves Booked", fontsize=12)
	autolabel(rects1)
	plt.savefig("manager_booked_moves_bar_graph.png")
	plt.clf()



def main():
	booked_moves_by_csr()
	#truck_moves()

if __name__ == "__main__":
	main()