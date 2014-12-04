from collections import Counter
import datetime
import csv
import p1_parse as p
from bookedmoves import BELLHOP_ORDER

order_database = p.parse(BELLHOP_ORDER, ",")


def pay_structure():
	for item in order_database:
		booked_datetime = (datetime.datetime.strptime(item['booked_at_date']
						   +' '+item['booked_at_time'], '%Y-%m-%d %I:%M:%S %p %Z'))
		move_datetime = (datetime.datetime.strptime(item['move_date']
						 +' '+item['move_time'], '%Y-%m-%d %I:%M:%S %p %Z'))
		captain_claim_datetime = (datetime.datetime.strptime(item['captain_claim_time']
						 		  +' '+item['captain_claim_time'], '%Y-%m-%d %I:%M:%S %p %Z')
		wingman_claim_datetime = (datetime.datetime.strptime(item['wingman_claim_time']
						 		  +' '+item['captain_claim_time'], '%Y-%m-%d %I:%M:%S %p %Z')
		if booked_datetime - move_datetime <= datetime.timedelta(hours=12):
			#Captain and Wingman for same day jobs
			captain_pay = 18.0
			wingman_pay = 16.0
			return (captain_pay, wingman_pay)
		if (booked_datetime - move_datetime <= datetime.timedelta(days=7) and 
			booked_datetime - move_datetime > datetime.timedelta(hours=12)):
			pay_decrease_interval = (booked_datetime - move_datetime)/6
