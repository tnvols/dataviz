from collections import Counter

import re
import matplotlib.pyplot as plt
import numpy as na
import p1_parse as p

BELLHOP_ORDER = "../data/chart-300192.csv"
TICKETS_FILE = "../data/report-feed-export-2015-02-02-1331-429105ba40-v2.csv"
ZOPIMS_FILE = "../data/report592867-5j0ccic3ESQvL6Vl.csv"
PHONE_FILE = "../data/agent_availability.csv"

order_file = p.parse(BELLHOP_ORDER, ",")
ticket_file = p.parse(TICKETS_FILE, ",")
zopim_file = p.parse(ZOPIMS_FILE, ",")
phone_call_file = p.parse(PHONE_FILE, ",")
begin_date = raw_input("Start date (yyyy-mm-dd): ")
end_date = raw_input("End date (yyyy-mm-dd): ")


agts = []
point = []


def point_function(agent):
	agent_hours = float(raw_input("%s's hours: " % agent))
	thank_you_vids = []
	tix_sovled = []
	jobs_filled = []
	moves = []
	touches = []
	phones = []
	for item in ticket_file:
		solved_date = item['Solved at']
		agent_solved = item['Assignee']
		sub = item["Subject"]
		if solved_date >= begin_date and solved_date <= end_date and agent == agent_solved:
			tix_sovled.append(float(item['Summation column']))
		split_sub = re.split("\W+", sub)
		if range(len(split_sub)) > range(0):
			if (
				split_sub[0].lower() == 'thanks' and solved_date >= begin_date
				and solved_date <= end_date and agent == agent_solved):
				thank_you_vids.append(float(item['Summation column']))
			if(
				split_sub[0].lower() == 'hhhhhh' and solved_date >= begin_date
				and solved_date <= end_date and agent == agent_solved):
				vids = float(split_sub[1])
				thank_you_vids.append(float(item['Summation column']) * vids)
			if(
				split_sub[0].lower() == 'touches' and solved_date >= begin_date
				and solved_date <= end_date and agent == agent_solved):
				touch = float(split_sub[1])
				touches.append(float(item['Summation column']) * touch)

			if (
				split_sub[0].lower() == 'fill' and solved_date >= begin_date
				and solved_date <= end_date and agent == agent_solved):
				jobs_filled.append(float(item['Summation column']))

	for i in order_file:
		move_agent = i['First Name'] + ' ' + i['Last Name']
		if move_agent == agent:
			moves.append(float(i['Count of Reservations Order']))
		elif move_agent == 'Joseph Doughty' and agent == 'Joey Doughty':
			moves.append(float(i['Count of Reservations Order']))
		else:
			moves.append(0)

	for call in phone_call_file:
		phone_agent = call['\xef\xbb\xbfAgent']
		if phone_agent == agent:
			phones.append(float(call['Calls']))
		else:
			phones.append(0)

	counter2 = Counter(zop['agent_names'] for zop in zopim_file if zop['session_start_date (GMT+0)'] >= begin_date and zop['session_start_date (GMT+0)'] <= end_date)

	if agent == 'Matt Intemann':
		zops = counter2["Matt"]
	elif agent == 'Joey Doughty':
		zops = counter2["Joseph"]
	elif agent == 'Brent Gauthier':
		zops = counter2["BJ"]
	elif agent == 'Charles Marczynski':
		zops = counter2["Charles"]
	elif agent == 'Justin Smith':
		zops = counter2["Justin"]
	elif agent == 'Tisha Blankenship':
		zops = counter2["Tisha"]
	elif agent == 'Olivia Moye':
		zops = counter2["Olivia"]
	elif agent == 'Aaron Edmonson':
		zops = counter2["Aaron"]
	elif agent == 'Stacy Scerini':
		zops = counter2["Stacy S."]
	elif agent == 'Graham Hodge':
		zops = counter2["Graham"]
	elif agent == 'Matt Harb':
		zops = counter2["Matt H."]
	else:
		zops = 0

	thank_you_vid_pts = sum(thank_you_vids) * 2
	touch_pts = sum(touches) * .5
	tix_slv_pts = sum(tix_sovled) * .25
	fill_pts = sum(jobs_filled) * 2
	move_pts = sum(moves) * 2
	zop_pts = zops * .50
	phone_pts = sum(phones) * .25
	subtotal_pts = thank_you_vid_pts + tix_slv_pts + fill_pts + move_pts + zop_pts + phone_pts + touch_pts
	pph = subtotal_pts / agent_hours

	if pph >= 1.75:
		pph_bonus = 30
	else:
		pph_bonus = 0

	total_pts = subtotal_pts + pph_bonus

	agts.append(agent)
	point.append(total_pts)

	print "--------------------------------------"
	print "%s" % agent
	print "--------------------------------------"
	print "\tCustomer Information Points (.5 pts per deep convo): %.2f" % touch_pts
	print "\tPhone Call Points (.25 pts per call answered): %.2f" % phone_pts
	print "\tZopim Points (.5 pts per 1 zopim): %.2f" % zop_pts
	print "\tTickets Solved Points (.25 pts per 1 ticket): %.2f" % tix_slv_pts
	print "\tThank You Video Points(2 pts per 1 video): %.2f" % thank_you_vid_pts
	print "\tBooked Move Points(2 pts per booked move): %.2f" % move_pts
	print "\tJob Filled Points(2 pt per job filled): %.2f" % fill_pts
	print "\t\t Points Subtotal: %.2f" % subtotal_pts
	print "\t\t Points Per Hour Worked: %.2f pts/hr" % pph
	print "\t\t Points Per Hour Worked Bonus (30 pts if PPHW is >=1.75): %.2f" % pph_bonus
	print
	print "\t\t Total Points: %.2f" % total_pts


def agent_list():
	agents = set()
	for item in ticket_file:
		agents.add(item['Assignee'])
	agent_t = sorted(agents)
	for agent in agent_t:
		if (
			agent == "Ethan Buyer" or agent == "Gavyn Bridges"
			or agent == "Tanner Sexton" or agent == "Tanner Waters"
			or agent == "Joey Doughty" or agent == "Justin Smith"
			or agent == "Tisha Blankenship" or agent == "Olivia Moye"
			or agent == "Aaron Edmonson" or agent == "Stacy Scerini"
			or agent == "Brent Gauthier" or agent == "Charles Marczynski"
			or agent == "Graham Hodge" or agent == "Matt Harb"):
			point_function(agent)


def autolabel(rects):
	# attach some text labels
	for rect in rects:
		height = rect.get_height()
		plt.text(rect.get_x() + rect.get_width() / 2., 1.05 * height, '%d' % int(height), ha='center', va='bottom')


def point_leaderboard():
	agent_list()
	csr_list = tuple(agts)
	xlocations = na.array(range(len(csr_list))) + 0.5
	width = 0.5
	rects1 = plt.bar(xlocations, point, width, color='green')
	plt.xticks(xlocations + width / 2, csr_list, rotation=90)
	plt.subplots_adjust(bottom=0.3)
	plt.rcParams['figure.figsize'] = 19, 19
	plt.suptitle("Points to date since " + begin_date, fontsize=12)
	plt.ylabel("Points", fontsize=12)
	autolabel(rects1)
	plt.savefig("leaderboard.png")
	plt.clf()


def main():
	point_leaderboard()

if __name__ == "__main__":
	main()
