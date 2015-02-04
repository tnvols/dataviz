import geojson as g

import p1_parse as p 

def create_map(data_file):
	""" Creates a GeoJSON file.

	Returns a GeoJSON file that can be rendered in GitHub
	Gist at gist.github.com. Just copy the output file and 
	paste into a new Gist, then create either a public or 
	private gist. GitHub will automatically render the GeoJSON
	file as a map.
	"""
	geo_map = {"type": "FeatureCollection"}

	item_list = []
	for index, line in enumerate(data_file):
		if line['X'] == "0" or line['Y'] == "0":
			continue
		data = {}
		data['type'] = 'Feature'
		data['id'] = index
		data['properties'] = {'title': line['Category'],
							  'description': line['Descript'],
							  'date': line['Date']}
		data['geometry'] = {'type': 'Point',
							'coordinates': (line['X'], line['Y'])}
		# Add data dictionary to our item_list
		item_list.append(data)

	for point in item_list:
		geo_map.setdefault('features', []).append(point)
	 # Now that all data is parsed in GeoJSON write to a file so we
	 # can upload it to gist.github.com
	with open('file_sf.geojson', 'w') as f:
		f.write(g.dumps(geo_map))

def main():
	data = p.parse(p.MY_FILE, ",")

	return create_map(data)

if __name__ == "__main__":
	main()





