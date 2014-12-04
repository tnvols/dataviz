from collections import Counter

import csv
import matplotlib.pyplot as plt
import numpy.numarray as na
import p1_parse as p
from call_data import CALL_DATA


def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%.2f'%float(height),
                ha='center', va='bottom')


def calls_by_csr():
	call_file = p.parse(CALL_DATA, ",")
	begin_date = raw_input("Start date (Month dd, yyyy): ")
	end_date = raw_input("End date( Month dd, yyyy): ")
	ice_hours = raw_input("Ice Hours: ")
	joey_hours = raw_input("Joey Hours: ")
	branton_hours = raw_input("Branton Hours: ")
	bj_hours = raw_input("BJ Hours: ")
	chuck_hours = raw_input("Chuck Hours: ")
	averyhart_hours = raw_input("Averyhart Hours: ")
	jacob_hours = raw_input("Jacob Hours: ")

	counter = Counter(item["Agent"] for item in call_file if item["Date/Time"] >= begin_date 
		and item["Date/Time"] <= end_date and item["Call Status"] == "Completed"
		and item["Minutes"] > "1")

	call_list = [
		(float(counter["Brent Gauthier"])/float(bj_hours)),
		(float(counter["Joey Doughty"])/float(joey_hours)),
		(float(counter["Matt Intemann"])/float(ice_hours)),
		(float(counter["Branton Phillips"])/float(branton_hours)),
		(float(counter["Matt Averyhart"])/float(averyhart_hours)),
		(float(counter["Jacob Ellis"])/float(jacob_hours)),
		(float(counter["Charles Marczynski"])/float(chuck_hours))
	]

	csr_list = tuple(["BJ", "Joey", "Iceman", "Branton", "Averyhart", "Jacob", "Chuck"])
	xlocations = na.array(range(len(csr_list))) + 0.5
	width = 0.5
	rects1 = plt.bar(xlocations, call_list, width, color='green')
	plt.xticks(xlocations + width / 2, csr_list, rotation=90)	
	plt.subplots_adjust(bottom=0.2)
	plt.rcParams['figure.figsize'] = 12, 12
	plt.suptitle("Inbound & Outboud Calls Per Hour Worked From " + begin_date + " to " + end_date, fontsize=12)
	plt.ylabel("Inbound & Outboud Calls Per Hour Worked > 1 min", fontsize=12)
	autolabel(rects1)
	plt.savefig("phone_calls_per_hour_graph.png")
	plt.clf()


def main():
	calls_by_csr()


if __name__ == "__main__":
	main()