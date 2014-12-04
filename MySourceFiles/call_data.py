from collections import Counter

import csv
import matplotlib.pyplot as plt
import numpy as na
import p1_parse as p

CALL_DATA = "../data/call-history-2014-08-01-to-2014-08-31.csv"

def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
                ha='center', va='bottom')


def calls_by_csr():
	call_file = p.parse(CALL_DATA, ",")
	begin_date = "August 1, 2014"
	end_date = "August 31, 2014"

	counter = Counter(item["Agent"] for item in call_file if item["Date/Time"] >= begin_date 
		and item["Date/Time"] <= end_date and item["Call Status"] == "Completed"
		and item["Minutes"] > "1")

	call_list = [
		counter["Brent Gauthier"],
		counter["Joey Doughty"],
		counter["Matt Intemann"],
		counter["Branton Phillips"],
		counter["Matt Averyhart"],
		counter["Jacob Ellis"],
		counter["Charles Marczynski"]
	]

	csr_list = tuple(["BJ", "Joey", "Iceman", "Branton", "Averyhart", "Jacob", "Chuck"])
	xlocations = na.array(range(len(csr_list))) + 0.5
	width = 0.5
	rects1 = plt.bar(xlocations, call_list, width, color='green')
	plt.xticks(xlocations + width / 2, csr_list, rotation=90)	
	plt.subplots_adjust(bottom=0.2)
	plt.rcParams['figure.figsize'] = 12, 12
	plt.suptitle("Inbound & Outboud Calls Per Rep From " + begin_date + " to " + end_date, fontsize=12)
	plt.ylabel("Number of Inbound & Outbound Calls > 1 min", fontsize=12)
	autolabel(rects1)
	plt.savefig("phone_calls_graph.png")
	plt.clf()


def total_inbound_calls():
	inbounds = []
	completed = []
	abandoned_queue = []
	left_voicemail = []
	abandoned_unknown = []
	abandoned_voicemail = []
	call_file = p.parse(CALL_DATA, ",")
	begin_date = "August 1, 2014"
	end_date = "August 31, 2014"
	for item in call_file:
		if item['Wait Time'] != '':
			inbounds.append(float(item['Wait Time']))
			if item['Call Status'] == "Completed" and item['Agent'] == "Voicemail":
				left_voicemail.append(float(item['Wait Time']))
			elif item['Call Status'] == "Abandoned In Queue":
				abandoned_queue.append(float(item['Wait Time']))
			elif item['Call Status'] == "Completed" and item['Agent'] != "Voicemail":
				completed.append(float(item['Wait Time']))
			elif item['Call Status'] == "Abandoned Unknown" or item['Call Status'] == "Abandoned":
				abandoned_unknown.append(float(item['Wait Time']))
			elif item['Call Status'] == "Abandoned In Voicemail":
				abandoned_voicemail.append(float(item['Wait Time']))

	total_inbound = float(len(inbounds))
	aw_in = float(na.average(inbounds))
	voicemails = float(len(left_voicemail))
	per_vm = (voicemails/total_inbound) * 100
	aw_vm = float(na.average(left_voicemail))
	hangup_voicemail = float(len(abandoned_voicemail))
	per_hvm = (hangup_voicemail/total_inbound) * 100
	aw_hvm = float(na.average(abandoned_voicemail))
	complete_calls = float(len(completed))
	per_cc = (complete_calls/total_inbound) * 100
	aw_cc = float(na.average(completed))
	hangup_queue = float(len(abandoned_queue))
	per_hq = (hangup_queue/total_inbound) * 100
	aw_hq = float(na.average(abandoned_queue))
	aban_un = float(len(abandoned_unknown))
	aw_un = float(na.average(abandoned_unknown))
	per_un = (aban_un/total_inbound) * 100

	print "---------"*8
	print "Inbound Call Data from %s to %s" % (begin_date, end_date)
	print "---------"*8
	print "Total Inbound Calls: %.2f" % total_inbound
	print "Avg Wait For All Inbound: %.2f seconds" % aw_in
	print "---------"*8
	print "\tCalls Completed (%.2f%% of Total Inbound): %.2f" % (per_cc, complete_calls)
	print "\t\tAvg. Wait: %.2f seconds" % aw_cc
	print "\tVoicemails Left (%.2f%% of Total Inbound): %.2f" % (per_vm, voicemails)
	print "\t\tAvg. Wait: %.2f seconds" % aw_vm
	print "\tHung up in Voicemail (%.2f%% of Total Inbound): %.2f" % (per_hvm, hangup_voicemail)
	print "\t\tAvg. Wait: %.2f seconds" % aw_hvm
	print "\tHung up in Queue (%.2f%% of Total Inbound): %.2f" % (per_hq, hangup_queue)
	print "\t\tAvg. Wait: %.2f seconds" % aw_hq
	print "\tAbandoned Unknown (%.2f%% of Total Inbound): %.2f" % (per_un, aban_un)
	print "\t\tAvg. Wait: %.2f seconds" % aw_un




def main():
	calls_by_csr()
	#total_inbound_calls()


if __name__ == "__main__":
	main()