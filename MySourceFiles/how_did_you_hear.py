from collections import Counter
import csv
import numpy as np
import p1_parse as p
from bookedmoves import BELLHOP_ORDER

order_file = p.parse(BELLHOP_ORDER, ",")
order_num = raw_input("Enter order_id (Stop to end): ")
 
def how_did_you_hear(order_id):
	for item in order_file:
		if item['number'] == order_id:
			return (item['number'], item['how_did_you_hear'])


def main():
	print how_did_you_hear(order_num)

 
if __name__ == "__main__":
	main()

