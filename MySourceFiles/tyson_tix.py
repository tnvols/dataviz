from collections import Counter
from operator import truediv
import datetime
import csv
import re
import p1_parse as p
from bookedmoves import BELLHOP_ORDER

TICKET_FILE = "../data/report-feed-export-2014-12-01-1626-429105ca2f-v2.csv"

order_file = p.parse(BELLHOP_ORDER, ",")
ticket_file = p.parse(TICKET_FILE, ",")
begin_date = raw_input("Start date (yyyy-mm-dd): ")
end_date = raw_input("End date (yyyy-mm-dd): ")


def job_fills_per_tyson(agent):
	jobs_filled = []
	markets_filled = []
	agent_hours = float(raw_input("%s's hours: " % agent))
	for item in ticket_file:
		solved_date = item['Solved at']
		agent_solved = item['Assignee']
		sub = item["Subject"]
		split_sub = re.split("\W+",sub)
		if range(len(split_sub)) > range(0):
			if (split_sub[0].lower() == 'fill' and solved_date >= begin_date
				and solved_date <= end_date and agent == agent_solved):
				jobs_filled.append(float(item['Summation column']))
				if (split_sub[2] == 'San' or split_sub[2] == 'College' or
					split_sub[2] == 'Baton' or split_sub[2] == 'Boca' or
					split_sub[2] == 'Long' or split_sub[2] == 'Los' or
					split_sub[2] == 'Fort' or split_sub[2] == 'Iowa' or
					split_sub[2] == 'West' or split_sub[2] == 'New' or
					split_sub[2] == 'Ann' or split_sub[2] == 'East' or
					split_sub[2] == 'Mt.' or split_sub[2] == 'Chapel' or
					split_sub[2] == 'State' or split_sub[2] == 'Salt' or
					split_sub[2] == 'El' or split_sub[2] == 'Saint' or
					split_sub[2] == 'Cape' or split_sub[2] == 'Kansas'):
					markets_filled.append(split_sub[2]+' '+split_sub[3]+','+' '+split_sub[1])
				else:
					markets_filled.append(split_sub[2]+','+' '+split_sub[1])
	filled = sum(jobs_filled)
	fills_per_hour = filled / agent_hours
	print "%s:" % agent
	print "\tTotal Jobs Filled: %d" % filled
	print "\tJobs Filled Per Hour Worked: %.2f" % fills_per_hour
	print "\tMarkets Filled: %s" % markets_filled
	print
	print



def agent_list():
	agents = set()
	for item in ticket_file:
		agents.add(item['Assignee'])
	agent_t = sorted(agents)
	print "----------"*10
	print "Jobs filled from %s to %s" % (begin_date, end_date)
	print "----------"*10
	for agent in agent_t:
		if ( agent == "Ethan Buyer" or agent == "Gavyn Bridges"
			or agent == "Tanner Sexton" or agent == "Tanner Waters"):
			job_fills_per_tyson(agent)
	


def orders_booked_three_days():
	""" Finds orders that were booked three days in advance of the
	move date.
	"""
	order_id_list = []
	for item in order_file:
		booking = datetime.datetime.strptime(item['booked_at_date'], "%Y-%m-%d")
		moving = datetime.datetime.strptime(item['move_date'], "%Y-%m-%d")
		if (item['booked_at_date'] >= begin_date and item['booked_at_date'] <= end_date
			and moving - booking > datetime.timedelta(days=2)
			and item['deposit_paid'] != '' and item['charges_verified'] == 'Yes'):
			order_id_list.append(item['number'])
	return order_id_list

def percent_booked_less_24_hrs():
	"""Percent of orders booked with less than 1 day notice"""
	order_id_list = []
	vm_counter = Counter(item['charges_verified'] == "Yes" for item in order_file if item['move_date'] >= begin_date 
		and item['move_date'] <= end_date and item['deposit_paid'] != '')
	verified_moves = float(vm_counter[True])
	for item in order_file:
		booking = datetime.datetime.strptime(item['booked_at_date'], "%Y-%m-%d")
		moving = datetime.datetime.strptime(item['move_date'], "%Y-%m-%d")
		if (item['booked_at_date'] >= begin_date and item['booked_at_date'] <= end_date
			and moving - booking <= datetime.timedelta(days=1)
			and item['deposit_paid'] != '' and item['charges_verified'] == 'Yes'):
			order_id_list.append(item['number'])
	per_under_24 = (float(len(order_id_list))/verified_moves) * 100

	print "Jobs booked under 24 hours from %s to %s" % (begin_date, end_date)
	print per_under_24



def unclaimed_notices_by_market():
	""" unclaimed notifications sent for moves that were booked more
	three days in advance.
	"""
	three_days_notice = orders_booked_three_days()
	markets = []
	for ticket in ticket_file:
		split_sub = ticket["Subject"].split()
		re_split = re.split("\W+",ticket["Subject"])
		if (range(len(split_sub)) == range(0,17) and ticket["Created at"] > begin_date 
			and ticket["Created at"] < end_date):
			if split_sub[0]+ ' '+split_sub[1] == "Unclaimed Order" and split_sub[16] in three_days_notice:
				markets.append(split_sub[5]+' '+split_sub[6]+", "+split_sub[3])
		if (range(len(split_sub)) == range(0,16) and ticket["Created at"] > begin_date 
			and ticket["Created at"] < end_date):
			if split_sub[0]+ ' '+split_sub[1] == "Unclaimed Order" and split_sub[15] in three_days_notice:
				markets.append(split_sub[5]+", "+split_sub[3])
		if (range(len(re_split)) > range(0,6) and ticket["Created at"] > begin_date 
			and ticket["Created at"] < end_date):
			if re_split[0].lower() == 'fill':
				if re_split[3] in three_days_notice:
					markets.append(re_split[2]+','+' '+re_split[1])
				if re_split[4] in three_days_notice:
					markets.append(re_split[2]+' '+re_split[3]+','+' '+re_split[1])
				if re_split[5] in three_days_notice:
					markets.append(re_split[2]+' '+re_split[3]+' '+re_split[4]+','+' '+re_split[1])

	return dict(Counter(markets))


def totals_by_market():
	"""total moves booked and verified per market """
	market_totals = []
	for item in order_file:
		booking = datetime.datetime.strptime(item['booked_at_date'], "%Y-%m-%d")
		moving = datetime.datetime.strptime(item['move_date'], "%Y-%m-%d")
		if (item['booked_at_date'] >= begin_date and item['booked_at_date'] <= end_date
			and moving - booking > datetime.timedelta(days=2)
			and item['deposit_paid'] != '' and item['charges_verified'] == 'Yes'):
			market_totals.append(item['market']+', '+item['state'])
	return dict(Counter(market_totals))


def percent_of_unclaimed():
	"""percentage of orders (with more than three days notice)
	that are unclaimed within 24 hours
	"""
	tm = totals_by_market()
	um = unclaimed_notices_by_market()
	unclaimed_percent = {k: "{0:.2f}".format(float(um[k])/tm[k] * 100) for k in um.viewkeys() & tm.viewkeys()}
	t = list()
	for key, val in unclaimed_percent.items():
		t.append((key, val))
	t.sort(reverse=False)
	for key, val in t:
		print key, val


def unclaimed_percent_all():
	""" Gives unclaimed percentage for all markets"""
	us = []
	ts= []
	tms = totals_by_market()
	ums = unclaimed_notices_by_market()
	for k in ums.viewkeys() & tms.viewkeys():
		us.append(ums[k])
	for k in tms.keys():
		ts.append(tms[k])
	
	total_unclaimed = "{0:.2f}".format(float(sum(us))/float(sum(ts)) * 100)
	print total_unclaimed


def main():
	#unclaimed_notices_by_market()
	#percent_of_unclaimed()
	#unclaimed_percent_all()
	agent_list()
	#orders_booked_three_days()
	#percent_booked_less_24_hrs()

if __name__ == "__main__":
	main()