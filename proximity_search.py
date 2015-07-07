from generate_data import generate_datum
from geopy.distance import great_circle
from functools import cmp_to_key
def main():
	home = generate_datum()
	data = []
	for i in range (0,10000):
		data.append(generate_datum())
	n = 10
	similarList = find_similar(home,data,n)
	print similarList
	
def find_similar(home,data,n):
	# add distance and sort by it 
	data = add_distance(home,data)
	data = sorted(data,key=lambda x: x[1])
	# reduce to n 
	data = data[:n]
	# out of the n homes find sort by similarity 
	data = similarity(home,data)
	data = sorted(data,key=lambda x:x[2])
	return data

def similarity(home,data):
	# difference in bedroom + bathroom + stories + pool_diff + dwelling_type_diff 
	# the larger the number, the less similar
	newlist = []
	for (idx,each) in enumerate(data):
		newhome = each[0]
		bedroom_diff = abs(home.num_bedrooms - newhome.num_bedrooms)
		bathroom_diff = abs(home.num_bathrooms - newhome.num_bathrooms)
		stories_diff = abs(home.exterior_stories - newhome.exterior_stories) 
		score = bedroom_diff + bathroom_diff + stories_diff
		if(home.pool != newhome.pool):
			score += 1
		if(home.dwelling_type != home.dwelling_type):
			score += 1
		newlist.append((newhome,each[1],score))
	return newlist

def add_distance(home,data):
	home_lat_lon = (home.lat, home.lon)
	newlist = []
	for (idx,each) in enumerate(data):
		curr_lat_lon = (each.lat, each.lon)
		newlist.append((each,great_circle(home_lat_lon, curr_lat_lon).miles))
	return newlist

if __name__ == '__main__':
	main()