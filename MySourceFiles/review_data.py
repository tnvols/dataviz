from collections import Counter

import p1_parse as p

BELLHOP_ORDER = '../data/2014_12_15_1316_bellhops_order_export.csv'

order_file = p.parse(BELLHOP_ORDER, ",")
begin_date = '2014-11-01' #raw_input("Start date: ")
end_date = '2014-11-20' #raw_input("End date: ")
thank_you_vids_complete = raw_input('Videos Complete: ')

great_reviews = []
all_reviews = []
tm = []


def market_moves():

	vm_counter = Counter(i['charges_verified'] == "Yes" for i in order_file if i['move_date'] >= begin_date
				         and i['move_date'] <= end_date and i['deposit_paid'] != '')

	verified_moves = float(vm_counter[True])

	external_counter = Counter(i['charges_verified'] == "Yes" for i in order_file if i['move_date'] >= begin_date
							   and i['move_date'] <= end_date and i['deposit_paid'] == '')

	external_moves = float(external_counter[True])
	total_moves = int(verified_moves + external_moves)
	tm.append(total_moves)


def moves_with_5star_reviews():
	for i in order_file:
		review = i['customer_review_score']
		if review == '5.0' and i['move_date'] >= begin_date and i['move_date'] <= end_date:
			great_reviews.append(float(review))
		if review > '0.0' and i['move_date'] >= begin_date and i['move_date'] <= end_date:
			all_reviews.append(float(review))


def percentages_of_reviews():
	market_moves()
	moves_with_5star_reviews()

	num_great_reviews = float(len(great_reviews))
	num_all_reviews = float(len(all_reviews))
	moves = sum(tm)
	thank_you_vids = float(thank_you_vids_complete)

	per_total_with_review = (num_all_reviews / moves) * 100
	per_total_great_review = (num_great_reviews / moves) * 100
	per_vids_total_reviews = (thank_you_vids / num_all_reviews) *100
	per_vids_to_total_moves = (thank_you_vids / moves) * 100
	
	print "Data from %s to %s" % (begin_date, end_date)
	print '----------' * 5
	print "Number of moves: %d" % moves
	print "Number of reviews: %.2f" % num_all_reviews
	print "Number of 5.0 reviews: %.2f " % num_great_reviews
	print "Number of videos sent: %.2f " % thank_you_vids
	print "Percent of total moves with a review: %.2f %%" % per_total_with_review
	print "Percent of total moves with a 5.0 rating: %.2f %%" % per_total_great_review
	print "Percent of total moves that were sent a video: %.2f %%" % per_vids_to_total_moves
	print "Percent of total reviews that were sent a video: %.2f %%" % per_vids_total_reviews


def main():
	percentages_of_reviews()

if __name__ == "__main__":
	main()
