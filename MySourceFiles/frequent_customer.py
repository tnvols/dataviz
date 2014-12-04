from collections import Counter

import csv
import matplotlib.pyplot as plt
import numpy as na
import p1_parse as p

BELLHOP_ORDER = "../data/2014_11_10_1323_bellhops_order_export.csv"

def frequent_customer():
	order_file = p.parse(BELLHOP_ORDER, ",")
	customer_em = []
	ems = set()

	for item in order_file:
		if (item['charges_verified'] == "Yes" and item['deposit_paid'] != ''):
			customer_em.append(item['customer_email'])
		for email in customer_em:
			if (customer_em.count(email) > 2 and item['customer_email'] == email
				and item['move_date'] > "2014-11-10" and item['customer_review_score'] > 4.8):
				ems.add(email)
	e = list(ems)
	for i in e:
		print i


def main():
	frequent_customer()

if __name__ == "__main__":
	main()
