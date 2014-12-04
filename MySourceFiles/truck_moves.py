from collections import Counter
from operator import truediv
import csv
import p1_parse as p
from bookedmoves import BELLHOP_ORDER

order_file = p.parse(BELLHOP_ORDER, ",")
begin_date = raw_input("Start date: ")
end_date = raw_input("End date: ")

def residential_truck_moves():
	counter = Counter(item["truck_required"] == "Yes" for item in order_file if item['move_date'] >= begin_date 
		and item['move_date'] <= end_date and item['deposit_paid'] != '' and item["charges_verified"] == 'Yes')
	truck_list = float(counter[True])

	print truck_list


def main():
	residential_truck_moves()


if __name__ == "__main__":
	main()