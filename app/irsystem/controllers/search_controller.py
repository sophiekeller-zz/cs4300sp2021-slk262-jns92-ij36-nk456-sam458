from . import *
from app.irsystem.models.search import *

project_name = "Itinerary Planner"
net_id = "Sophie Keller: slk262, Jordana Socher: jns92, Ishika Jain: ij36,  Samantha Meakem: sam458, Nithish Kalpat: nk456 "

@irsystem.route('/', methods=['GET'])
def search():
	restaurant_query = request.args.get('restaurant')
	accommodation_query = request.args.get('accommodation')
	attraction_query = request.args.get('attraction') 

	if request.args.get('city') is not None and request.args.get('city') != 'none':
		city = request.args.get('city')
		restaurants = cosineSim(city, "restaurant", restaurant_query) #replace w svd_cos_sim
		accommodations = cosineSim(city, "accommodation", accommodation_query)
		attractions = cosineSim(city, "attraction", attraction_query)
	else:
		city = ''
		restaurants = []
		accommodations = []
		attractions = []

	r = request.args.get('distance')
	radius = 10000 if r is None or r == '' else int(r)
	rad = within_rad(city, [x[0] for x in accommodations], [x[0] for x in restaurants], [x[0] for x in attractions], radius)

	output_message =""# "Your itinerary options"
	data = []

	accommodations = list(filter(lambda x: rad[x]['restaurants'] or rad[x]['attractions'], rad.keys()))  # filters out accommodations w no restaurants

	
	for i, a in enumerate(accommodations[:6]): #gets top 6 itineraries
		data.append({"city": city, "title": f"Itinerary #{i + 1}", "accommodation": rad[a]['accommodation'], "restaurants": rad[a]['restaurants'][:10], "attractions": rad[a]['attractions'][:10]})
	


	return render_template('./listing/index.html', name=project_name, netid=net_id, output_message=output_message, data=data)
