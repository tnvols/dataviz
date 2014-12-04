from collections import Counter
import csv
import numpy as np
import p1_parse as p
from bookedmoves import BELLHOP_ORDER

#first tip 2014-03-08
#2014-05-01 when refund data occured
order_file = p.parse(BELLHOP_ORDER, ",")
begin_date = '2014-09-01' #raw_input("Start date: ")
end_date = '2014-10-01'#raw_input("End date: ")
vm_counter = Counter(item['charges_verified'] == "Yes" for item in order_file if 
		     item['move_date'] >= begin_date and item['move_date'] <= end_date
			 and item['deposit_paid'] != '')
verified_moves = float(vm_counter[True])

print verified_moves


def bellhops_assigned():
	hops = []
	for item in order_file:
		if (item['charges_verified'] == "Yes" and item['move_date'] >= begin_date 
			and item['move_date'] <= end_date and item['deposit_paid'] != '' and item['bellhops_assigned'] != "0"):
			hops.append(float(item['bellhops_assigned']))
	avg_hops_per_job = np.average(hops)
	print "Average Bellhops Per Move: %.2f" % avg_hops_per_job
	return avg_hops_per_job
a_hops = bellhops_assigned()


def avg_bill_duration():
	duration = []
	for item in order_file:
		if (item['charges_verified'] == "Yes" and item['move_date'] >= begin_date 
			and item['move_date'] <= end_date and item['deposit_paid'] != '' and item['bellhops_assigned'] != "0"
			and item['billable_duration'] != ''):
			duration.append(float(item['billable_duration'])/float(item['bellhops_assigned']))
	avg_duration = np.average(duration)/60
	print "Average Billable Duration Per Move: %.2f" % avg_duration



def avg_profit():
	profit = []
	for item in order_file:
		if (item['charges_verified'] == "Yes" and item['move_date'] >= begin_date 
			and item['move_date'] <= end_date and item['deposit_paid'] != ''):
			profit.append(float(item['total_profit']))
	avg_profit = np.average(profit)
	print "Average Profit is: %.2f" % avg_profit




def avg_tip():
	tips = []
	for item in order_file:
		if (item['charges_verified'] == "Yes" and item['move_date'] >= begin_date 
		and item['move_date'] <= end_date and item['deposit_paid'] != '' and item['total_tips'] != "0"):
			tips.append(float(item['total_tips']))
	avg_dollar_tip = np.average(tips)
	print "Average Tip Per Hop: $%.2f" % (avg_dollar_tip/a_hops)


def orders_with_tip():
	tip_counter = Counter(item['charges_verified'] == "Yes" for item in order_file if 
				 item['move_date'] >= begin_date and item['move_date'] <= end_date
				 and item['deposit_paid'] != '' and item['total_tips'] != '0')
	orders_with_tips = float(tip_counter[True])
	tip_order_percentage = ((orders_with_tips/verified_moves) * 100)
	print "Percent of Orders with Tips: %.2f%%" % tip_order_percentage

def orders_with_deep_discount():
	#deep discoung defined as >40% off
	deep_discount_list = []
	for item in order_file:
		if (item['charges_verified'] == "Yes" and item['move_date'] >= begin_date 
		and item['move_date'] <= end_date and item['deposit_paid'] != ''):
			should_pay = float(item['total_payouts_to_bellhops']) * 2.85 #gives us amount we should have charged (we charge $40, but pay and avg of $14)
			total_paid = float(item['total_paid_by_customer']) - float(item['total_refunded'])
			if (should_pay - total_paid) > 0.0 and ((should_pay - total_paid)/ should_pay) > .40:
				dp = (float(should_pay) - float(total_paid))/ float(should_pay)
				deep_discount_list.append(dp)
	over_40_off_perc = ((len(deep_discount_list)/verified_moves) * 100)
	print "Percent of Verified Moves With More Than 40%% Off: %.2f%%" % over_40_off_perc


def orders_breaking_even_or_losing():
	loss_list = []
	for item in order_file:
		if (item['charges_verified'] == "Yes" and item['move_date'] >= begin_date 
		and item['move_date'] <= end_date and item['deposit_paid'] != ''):
			if (((float(item['total_paid_by_customer']) - float(item['total_refunded'])) - 
				 float(item['total_payouts_to_bellhops'])) <= 0.0):
				loss_list.append(float(item['total_profit']))
	even_or_loss_orders = ((len(loss_list)/verified_moves) * 100)
	print "Percent of Verified Moves We Have Lost Money Or Broke Even On: %.2f%%" % even_or_loss_orders



def orders_with_refund():
	refund_counter = Counter(item['charges_verified'] == "Yes" for item in order_file if 
				 item['move_date'] >= begin_date and item['move_date'] <= end_date
				 and item['deposit_paid'] != '' and item['total_refunded'] != '0.00')
	orders_with_refunds = float(refund_counter[True])
	refund_order_percentage = ((orders_with_refunds/verified_moves) * 100)
	print "Percent of Orders with refunds: %.2f%%" % refund_order_percentage


def orders_with_tip_by_booked():
	tip_csr_counter = Counter(item['charges_verified'] == "Yes" for item in order_file if 
				 item['move_date'] >= begin_date and item['move_date'] <= end_date
				 and item['deposit_paid'] != '' and item['total_tips'] != '0'
				 and item['booked_by'] != '')
	tip_online_counter = Counter(item['charges_verified'] == "Yes" for item in order_file if 
				 item['move_date'] >= begin_date and item['move_date'] <= end_date
				 and item['deposit_paid'] != '' and item['total_tips'] != '0'
				 and item['booked_by'] == '')
	orders_with_tips_by_csr = float(tip_csr_counter[True])
	orders_with_tips_online = float(tip_online_counter[True])
	csr_tip_order_percentage = ((orders_with_tips_by_csr/verified_moves) * 100)
	online_tip_order_percentage = ((orders_with_tips_online/verified_moves) * 100)
	print "Percent of Phone Orders with tips: %.2f%%" % csr_tip_order_percentage
	print
	print "Percent of Online Orders with tip: %.2f%%" % online_tip_order_percentage


def orders_with_refund_by_booked():
	refund_csr_counter = Counter(item['charges_verified'] == "Yes" for item in order_file if 
				 item['move_date'] >= begin_date and item['move_date'] <= end_date
				 and item['deposit_paid'] != '' and item['total_refunded'] != '0.00'
				 and item['booked_by'] != '')
	refund_online_counter = Counter(item['charges_verified'] == "Yes" for item in order_file if 
				 item['move_date'] >= begin_date and item['move_date'] <= end_date
				 and item['deposit_paid'] != '' and item['total_refunded'] != '0.00'
				 and item['booked_by'] == '')
	orders_with_refunds_by_csr = float(refund_csr_counter[True])
	orders_with_refunds_online = float(refund_online_counter[True])
	csr_refund_order_percentage = ((orders_with_refunds_by_csr/verified_moves) * 100)
	online_refund_order_percentage = ((orders_with_refunds_online/verified_moves) * 100)
	print "Percent of Phone Orders with refunds: %.2f%%" % csr_refund_order_percentage
	print
	print "Percent of Online Orders with refunds: %.2f%%" % online_refund_order_percentage


def tip_as_percent_of_cost():
	one_thou_costs = []
	one_thou_tips = []
	high_costs = []
	high_tips = []
	mid_costs = []
	mid_tips = []
	ml_costs = []
	ml_tips = []
	l_costs = []
	l_tips = []
	vl_costs = []
	vl_tips =  []
	for item in order_file:
		if (item['charges_verified'] == "Yes" and item['move_date'] >= begin_date 
		and item['move_date'] <= end_date and item['deposit_paid'] != '' and item['total_tips'] != "0"):
			if float(item['total_paid_by_customer']) >= 1000.0:
				one_thou_costs.append(float(item['total_paid_by_customer']))
				one_thou_tips.append(float(item['total_tips']))
			if float(item['total_paid_by_customer']) < 1000.0 and float(item['total_paid_by_customer']) >= 750.0:
				high_costs.append(float(item['total_paid_by_customer']))
				high_tips.append(float(item['total_tips']))
			if float(item['total_paid_by_customer']) < 750.0 and float(item['total_paid_by_customer']) >= 500.0:
				mid_costs.append(float(item['total_paid_by_customer']))
				mid_tips.append(float(item['total_tips']))
			if float(item['total_paid_by_customer']) < 500.0 and float(item['total_paid_by_customer']) >= 250.0:
				ml_costs.append(float(item['total_paid_by_customer']))
				ml_tips.append(float(item['total_tips']))		
			if float(item['total_paid_by_customer']) < 250.0 and float(item['total_paid_by_customer']) >= 100.0:
				l_costs.append(float(item['total_paid_by_customer']))
				l_tips.append(float(item['total_tips']))
			if float(item['total_paid_by_customer']) < 100.0:
				vl_costs.append(float(item['total_paid_by_customer']))
				vl_tips.append(float(item['total_tips']))

	one_thou_tip_percent = (((sum(one_thou_tips)/a_hops) / sum(one_thou_costs)) * 100)
	a_ot_tip = np.average(one_thou_tips)/a_hops
	high_tip_percent = (((sum(high_tips)/a_hops) / sum(high_costs)) * 100)
	a_ht_tip = np.average(high_tips)/a_hops
	mid_tip_percent = (((sum(mid_tips)/a_hops) / sum(mid_costs)) * 100)
	avg_m_tip = np.average(mid_tips)/a_hops
	ml_tip_percent = (((sum(ml_tips)/a_hops) / sum(ml_costs)) * 100)
	avg_ml_tip = np.average(ml_tips)/a_hops
	l_tip_percent = (((sum(l_tips)/a_hops) / sum(l_costs)) * 100)
	avg_l_tip = np.average(l_tips)/a_hops
	vl_tip_percent = (((sum(vl_tips)/a_hops) / sum(vl_costs)) * 100)
	avg_vl_tip = np.average(vl_tips)/a_hops
	print 
	print"Of the moves that tipped online:"
	print
	print "For Moves Costing $1000 or More: Average Tip Per Hop Was Was $%.2f and was %.2f%% of Move Cost" % (a_ot_tip, one_thou_tip_percent)
	print "For Moves Costing Between $750 and $999: Average Tip Per Hop Was $%.2f and was %.2f%% of Move Cost" % (a_ht_tip, high_tip_percent)
	print "For Moves Costing Between $500 and $749: Average Tip Per Hop Was $%.2f and was %.2f%% of Move Cost" % (avg_m_tip, mid_tip_percent)
	print "For Moves Costing Between $250 and $499: Average Tip Per Hop Was $%.2f and was %.2f%% of Move Cost" % (avg_ml_tip, ml_tip_percent)
	print "For Moves Costing Between $100 and $249: Average Tip Per Hop Was $%.2f and was %.2f%% of Move Cost" % (avg_l_tip, l_tip_percent)
	print "For Moves Costing Less than $100: Average Tip Per Hop Was $%.2f and was %.2f%% of Move Cost" % (avg_vl_tip, vl_tip_percent)


def main():
	print "---" * 20
	print "For Moves Performed From %s to %s " % (begin_date, end_date)
	print "---" * 20
	bellhops_assigned()
	print "---" * 20
	avg_tip()
	print "---" * 20
	orders_with_tip()
	print "---" * 20
	orders_with_tip_by_booked()
	#print "---" * 20
	#orders_with_refund_by_booked()
	print "---" * 20
	tip_as_percent_of_cost()
	print "---" * 20
	orders_with_deep_discount()
	print "---" * 20
	print orders_breaking_even_or_losing()
	print "---" * 20
	avg_profit()
	avg_bill_duration()


if __name__ == "__main__":
	main()