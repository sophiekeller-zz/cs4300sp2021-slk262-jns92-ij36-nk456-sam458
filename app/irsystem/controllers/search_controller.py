from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.search import *
import app.irsystem.models.vectorizer as vecPy
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
	print('fun' in vecPy.reverse_dict['dubai']['attraction'])
	if request.args.get('city') is not None and request.args.get('city') != 'none':
		city = request.args.get('city')
		restaurants = get_matchings_cos_sim(city, "restaurant", restaurant_query) #replace w svd_cos_sim
		accommodations = get_matchings_cos_sim(city, "accommodation", accommodation_query)
		attractions = get_matchings_cos_sim(city, "attraction", attraction_query)
		# svd_results_rests = LSI_SVD(restaurant_query, vecPy.vec_arr_dict, city, 'restaurant', vecPy.reverse_dict, vecPy.svd_dict)
		# svd_results_accoms = LSI_SVD(accommodation_query, vecPy.vec_arr_dict, city, 'accommodation', vecPy.reverse_dict, vecPy.svd_dict)
		# svd_results_attracts = LSI_SVD(attraction_query, vecPy.vec_arr_dict, city, 'attraction', vecPy.reverse_dict, vecPy.svd_dict)
	else:
		#ADD POP UP MESSAGE TO SELECT A CITY
		city = ''
		restaurants = []
		accommodations = []
		attractions = []
		# svd_results_rests = []
		# svd_results_accoms = []
		# svd_results_attracts = []
	# print(attractions)
	# print(svd_results_rests)
	# print(svd_results_accoms)
	# print(svd_results_attracts)
	r = request.args.get('distance')
	radius = 10000 if r is None or r == '' else int(r)
	#rad = within_rad(city, [x[0] for x in y[0]], [x[0] for x in y[1]], [x[0] for x in y[2]], radius)
	rad = within_rad(city, [x[0] for x in accommodations], [x[0] for x in restaurants], [x[0] for x in attractions], radius)

	output_message =""# "Your itinerary options"
	data = []

	accommodations = list(filter(lambda x: rad[x[0]]['restaurants'] or rad[x[0]]['attractions'], accommodations))  # filters out accommodations w no restaurants

	
	for i, a in enumerate(accommodations[:6]): #gets top 6 itineraries
		data.append({"city": city, "title": f"Itinerary #{i + 1}", "accommodation": rad[a[0]]['accommodation'], "restaurants": rad[a[0]]['restaurants'][:10], "attractions": rad[a[0]]['attractions'][:10]})



	return render_template('./listing/index.html', name=project_name, netid=net_id, output_message=output_message, data=data)
