import p1_parse as p

BELLHOP_ORDER = "../data/2014_12_02_1440_bellhops_order_export.csv"

order_file = p.parse(BELLHOP_ORDER, ",")
begin_date = raw_input("Start date: ")
end_date = raw_input("End date: ")


def man_hours_worked():
	dura = []
	for item in order_file:
		if item["charges_verified"] == 'Yes' and item["move_date"] >= begin_date and item["move_date"] <= end_date:
			dura.append(item['actual_duration'])
	hours =sum(dura)
	hour = hours / 60
	print hour


def main():
	man_hours_worked()

if __name__ == "__main__":
	main()
