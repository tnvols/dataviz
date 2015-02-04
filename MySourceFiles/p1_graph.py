from collections import Counter

import csv
import matplotlib.pyplot as plt
import numpy.numarray as na
import p1_parse as prs

MY_FILE = "../data/sample_sfpd_incident_all.csv"

def visualize_days():
	"""Visualize data by day of week"""
	#grab our parsed data tha we parsed earlier
	data_file = prs.parse(MY_FILE, ",")

	#make a new variable, 'counter', from iterating through each
	#line of data in the parsed data, and count how many incidents 
	#happen on each day of the week
	counter = Counter(item["DayOfWeek"] for item in data_file)  #for item in data_file:
	#separate the x-axis data (the days of the week) from the    	#return counter
	#'counter' variable from the y-axis data (the number of 
	#incidents for each day)
	data_list = [
				 counter["Monday"],
				 counter["Tuesday"],
				 counter["Wednesday"],
				 counter["Thursday"],
				 counter["Friday"],
				 counter["Saturday"],
				 counter["Sunday"]
				 ]
	day_tuple = tuple(["Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun"])

	# with that y-axis data, assign it tho a matplotlib plot instance
	plt.plot(data_list)
	#create the amount of ticks needed for our x-axis, and assign 
	#the labels
	plt.xticks(range(len(day_tuple)), day_tuple)
	#save the plot
	plt.savefig("Days.png")
	#close plot file
	plt.clf()


def visualize_type():
	"""Visualize data by category in a bar graph"""
	data_file = prs.parse(MY_FILE, ",")

	counter = Counter(item["Category"] for item in data_file)
	labels = tuple(counter.keys())
	xlocations = na.array(range(len(day))) + 0.5
	width = 0.5
	plt.bar(xlocations, counter.values(), width=width)
	plt.xticks(xlocations + width / 2, labels, rotation=90)
	plt.subplots_adjust(bottom=0.4)
	plt.rcParams['figure.figsize'] = 12, 8
	plt.savefig("Type.png")
	plt.clf()

def main():
	#visualize_days()
	visualize_type()

if __name__ == "__main__":
	main()