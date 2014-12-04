from collections import Counter

import csv
import matplotlib.pyplot as plt
import numpy.numarray as na
import p1_parse as p

CHAMBLISS_FILE = "../data/DMP20-Table 1.csv"

chambliss = p.parse(CHAMBLISS_FILE, ",")

def vol_report():
	bus = []
	num_vol_hours_bus = []
	num_vols_bus = []
	chruch = []
	foundation = []
	individual = []
	organization = []
	school = []
	for item in chambliss:
		if item['ContactType'] == "Business":
			if item['Company'] not in bus:
				bus.append(item['Company'])
			for item in bus:
				num_vols_bus.append(sum(int(item['Number of volunteers involved'])))

	print bus
	print num_vols_bus

	#bus_sort = sorted(bus)
		#elif item['ContactType'] == "Church":
		#	church.append(item['Company'])
		#elif item['ContactType'] == "Foundation":
		#	foundation.append(item['Company'])
		#elif item['ContactType'] == "Individual":
		#	individual.append(item['First']+''+item['Last'])
		#elif item['ContactType'] == "Organization":
		#	organization.append(item['Company'])
		#elif item['ContactType'] == "School":
		#	individual.append(item['Company'])
vol_report()

