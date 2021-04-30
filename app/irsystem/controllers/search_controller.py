from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.search import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder

project_name = "Itinerary Planner"
net_id = "Sophie Keller: slk262, Jordana Socher: jns92, Ishika Jain: ij36,  Samantha Meakem: sam458, Nithish Kalpat: nk456 "

# @irsystem.route('/', methods=['GET'])
# def search():
# 	restaurant_query = request.args.get('restaurant')
# 	accommodation_query = request.args.get('accommodation')
# 	city = 'london' # THIS NEEDS TO BE MODIFIED TO CONTAIN CITY THAT USER IS SEARCHING
# 	restaurants = [f"{x[0]} - Score:{x[1]}" for x in getMatchings(city, "restaurant", restaurant_query)]
# 	accommodations = [f"{x[0]} - Score:{x[1]}" for x in getMatchings(city, "accommodation", accommodation_query)]
# 	output_message = "Your itinerary"
# 	if restaurants or accommodations:
# 		data = ["Restaurants"] + restaurants + ["", "Accommodations"] + accommodations
# 	else:
# 		data = []
# 	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)


@irsystem.route('/', methods=['GET'])
def search():
	restaurant_query = request.args.get('restaurant')
	accommodation_query = request.args.get('accommodation')
	attraction_query = request.args.get('attraction')
	print(request.args.get('city'))
	if request.args.get('city') != 'none':
		city = request.args.get('city')
		restaurants = cosineSim(city, "restaurant", restaurant_query)
		accommodations = cosineSim(city, "accommodation", accommodation_query)
		attractions = cosineSim(city, "attraction", attraction_query)
	else:
		#ADD POP UP MESSAGE TO SELECT A CITY
		return render_template('./listing/index.html', name=project_name, netid=net_id, output_message="Please enter a city.", data=[])

		city = ''
		restaurants = []
		accommodations = []
		attractions = []

	# if request.args.get('preference') is 'attractions':
	# 	y = [attractions, restaurants, accommodations]
	# elif request.args.get('preference') is 'restaurants':
	# 	y = [restaurants, accommodations, attractions]
	# else:
	# 	y = [accommodations, restaurants, attractions]

	r = request.args.get('distance')
	radius = 10000 if r is None or r == '' else int(r)
	#rad = within_rad(city, [x[0] for x in y[0]], [x[0] for x in y[1]], [x[0] for x in y[2]], radius)
	rad = within_rad(city, [x[0] for x in accommodations], [x[0] for x in restaurants], [x[0] for x in attractions], radius)

	output_message =""# "Your itinerary options"
	data = []
	# if request.args.get('preference') == 'attractions':
	# 	order = ['attraction', 'accommodation','attraction']
	# 	rad = within_rad(city, [x[0] for x in attractions], [x[0] for x in restaurants], [x[0] for x in accommodations],
	# 					 radius, order)
	# 	results = list(filter(lambda x: rad[x[0]]['restaurants'] or rad[x[0]]['attractions'], accommodations))
	# 	for i, a in enumerate(results[:5]):
	# 		data.append([f"Itinerary #{i + 1}"])
	# 		data.append(f"Attraction: {a[0]}")
	# 		data.append("Restaurants:")
	# 		data += rad[a[0]]['restaurants'][:10]
	# 		data.append("Accommodations:")
	# 		data += rad[a[0]]['attractions'][:10]
	# 		data.append("")
	# elif request.args.get('preference') == 'restaurants':
	# 	order = ['restaurant', 'accommodation', 'attraction']
	# 	rad = within_rad(city, [x[0] for x in restaurants], [x[0] for x in accommodations], [x[0] for x in attractions],
	# 					 radius)
	# 	results = list(filter(lambda x: rad[x[0]]['restaurants'] or rad[x[0]]['attractions'], accommodations))
	# 	for i, a in enumerate(results[:5]):
	# 		data.append([f"Itinerary #{i + 1}"])
	# 		data.append(f"Restaurant: {a[0]}")
	# 		data.append("Accommodations:")
	# 		data += rad[a[0]]['restaurants'][:10]
	# 		data.append("Attractions:")
	# 		data += rad[a[0]]['attractions'][:10]
	# 		data.append("")
	# else:
	# 	rad = within_rad(city, [x[0] for x in accommodations], [x[0] for x in restaurants], [x[0] for x in attractions],
	# 					 radius)
	# 	results = list(filter(lambda x: rad[x[0]]['restaurants'] or rad[x[0]]['attractions'], accommodations)) #filters out accommodations w no restaurants
	# 	for i, a in enumerate(results[:5]):
	# 		data.append([f"Itinerary #{i + 1}"])
	# 		data.append(f"Accommodation: {a[0]}")
	# 		data.append("Restaurants:")
	# 		data += rad[a[0]]['restaurants'][:10]
	# 		data.append("Attractions:")
	# 		data += rad[a[0]]['attractions'][:10]
	# 		data.append("")

	accommodations = list(filter(lambda x: rad[x[0]]['restaurants'] or rad[x[0]]['attractions'], accommodations))  # filters out accommodations w no restaurants

	for i, a in enumerate(accommodations[:6]): #gets top 6 itineraries
		data.append({"city": city, "title": f"Itinerary #{i + 1}", "accommodation": a[0], "restaurants": rad[a[0]]['restaurants'][:10], "attractions": rad[a[0]]['attractions'][:10]})
		# data.append([f"Itinerary #{i + 1}"])
		# data.append(f"Accommodation: {a[0]}")
		# data.append("Restaurants:")
		# data += rad[a[0]]['restaurants'][:10]
		# data.append("Attractions:")
		# data += rad[a[0]]['attractions'][:10]
		# data.append("")

	if data == []:
		data = []

	return render_template('./listing/index.html', name=project_name, netid=net_id, output_message=output_message, data=data)
