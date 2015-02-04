import argparse
from __future__ import print_function

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('--giantbomb-api-key', required=True,
						help= 'API key provided by Giantbomb.com')
	#28bb3c0a49ee2124bc5e0ccdff40f32aadeec747
	parser.add_argument('--cpi-file',
						default=os.path.join(os.path.dirname(__file__),
											 'CPIAUCSL.txt'),
						help='Path to file containing the CPI data (also acts'
							 ' as target file if the data has to be downloaded'
							 'first).')
	parser.add_argument('--cpi-data-url', default=CPI_DATA_URL,
						help='URL which should be used as CPI data source')
	parser.add_argument('--debug', default=False, action='store_true',
						help='Increases the output level.')
	parser.add_argument('--csv-file',
						help='Path to CSV file which should contain the data'
							 'output')
	parser.add_argument('--plot-file',
						help='Path to the PNG file which should contain the'
							 'data output')
	parser.add_argument('--limit', type=int,
						help='Number of recent platforms to be considered')
	opts = parser.parse_args()
	if not (opts.plot_file or opts.csv_file):
		parser.error("You have to specify either a --csv-file or --plot-file!")
	return opts


def main():
	"""This function handles the actual logic of this script."""
	opts = parse_args()

	if opts.debug:
		logging.basicConfig(level=logging.DEBUG)
	else:
		logging.basicConfig(level=logging.INFO)

	cpi_data = CPIData()
	gb_api = GiantbombAPI(opts.giantbomb_api_key)

	print ("Disclaimer: This script uses data provided by FRED, Federal"
		   " Reserve Economic Data, form the federal Reserve Bank of St. Louis"
		   " and Giantbomb.com:\n- {0}\n- http://www.giantbomb.com/api/\n"
		   .format(CPI_DATA_URL))

	if os.path.exists(opts.cpi_file):
		with open(opts.cpi_file) as fp:
			cpi_data.load_from_file(fp)
	else:
		cpi_data.load_from_url(opts.cpi_data_url, save_as_file=opts.cpi_file)

	platforms = []
	counter = 0

	# Now that we have everything in place, fetch the platforms and calculate
	# their current price in relation to the CPI value.
	for platform in gb_api.get_platforms(sort='release_date:desc',
										 field_list=['release_date',
										 			 'original_price', 'name',
										 			 'abbreviation']):
		# Some platforms don't have a release date of price yet. These we have
		# to skip.
		if not is_valid_dataset(platform):
			continue
		year = int(platform['release_date'].split('-')[0])
		price = platform['original_price']
		adjusted_price = cpi_data.get_adjusted_price(price, year)
		platform['year'] = year
		platform['original_price'] = price
		platform['adjusted_price'] = adjusted_price
		platforms.append(platform)

		# We limit the resultset on this end siince we can only here check
		# if the dataset actually contains all the data we need and therefor
		# can't filter on the API level.
		if opts.limit is not None and counter + 1 >= opts.limit:
			break
		counter += 1

	if opts.plot_file:
		generate_plot(platforms, opts.plot_file)
	if opts.csv_file:
		generate_csv(platforms, opts.csv_file)


if __name__ == '__main__':
	main()
