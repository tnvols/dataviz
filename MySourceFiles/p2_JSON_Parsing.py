import matplotlib.pylot as plt
import numpy as np
import tablib

def generate_plot(platforms, output_file):
	""" Generates a bar chart out of the given platforms and writes the
	output into the specified file as PNG image.
	"""
	# First off we need to convert the platforms in a format that can be
	# attached to the 2 axis of our bar chart. "labels" will become the 
	# x-axis and "values" the value of each label on the y-axis:
	labels = []
	values = []
	for platform in platforms:
		name = platform['name']
		adapted_price = platform['adjusted_price']
		price = platform['original_price']
		# skip prices higher than 2000 USD simply because it would make the
		# output unsuable.
		if price > 2000:
			continue

		# If the name of the platform is too long, replace it with the
		# abbreviation. list.insert(0,val) inserts val at the beginning of 
		# the list.
		if len(name) > 15:
			name = platform['abbreviation']
		labels.insert(0, u"{0}\n$ {1}\n$ {2}".format(name,price,
													 round(adjusted_price,2)))
		values.insert(0, adapted_price)

		# Let's define the width of each bar and the size of the resulting graph.
		width = 0.3
		ind = np.arange(len(values))
		fig = plt.figure(figsize=(len(labels) * 1.8, 10))

		# Generate a subplot and put our values onto it.
		ax = fig.add_subplot(1, 1, 1)
		ax.bar(ind, values, width, align='center')

		# Format the x and Y axis labels. Also set the ticks on the x-axis slightly
		# farther apart and give them a slight tilting effect.
		plt.ylabel('Adjusted price')
		plt.xlabel('Year/ Console')
		ax.set_xticks(ind + 0.3)
		ax.set_xtickslabels(labels)
		fig.autofmt_xdate()
		plt.grid(True)
		plt.savefig(output_file, dpi=72)


def generate_csv(platforms, output_file):
	""" Writes the given platforms into a CSV file specified by the output_file
	parameter.

	The output_file can either be the path to a file of a file-like object.

	"""
	dataset = tablib.Dataset(headers=['Abbreviation', 'Name', 'Year', 'Price',
									  'Adjusted price'])
	for p in platforms:
		dataset.append([p['abbreviation'], p['name'], p['year'],
						p['original_price'], p['adjusted_price']])

	# If the output_file is a string it represents a path to a file which
	# we will have to open first for writing. Otherwise we just assume that
	# it is already a file-like object and write the data into it.
	if isinstance(output_file, basestring):
		with open(output_file, 'w+') as fp:
			fp.write(dataset.csv)
	else:
		output_file.write(dataset.csv)