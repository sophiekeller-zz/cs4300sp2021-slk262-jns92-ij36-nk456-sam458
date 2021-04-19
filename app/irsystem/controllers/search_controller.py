from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.search import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder

project_name = "Itinerary Planner"
net_id = "Sophie Keller: slk262, Jordana Socher: jns92, Ishika Jain: ij36,  Samantha Meakem: sam458, Nithish Kalpat: nk456 "

@irsystem.route('/', methods=['GET'])
def search():
	restaurant_query = request.args.get('restaurant')
	accommodation_query = request.args.get('accommodation')
	city = 'london' # THIS NEEDS TO BE MODIFIED TO CONTAIN CITY THAT USER IS SEARCHING
	restaurants = [f"{x[0]} - Score:{x[1]}" for x in getMatchings(city, "restaurant", restaurant_query)]
	accommodations = [f"{x[0]} - Score:{x[1]}" for x in getMatchings(city, "accommodation", accommodation_query)]
	output_message = "Your itinerary"
	if restaurants or accommodations: 
		data = ["Restaurants"] + restaurants + ["", "Accommodations"] + accommodations
	else:
		data = []
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)



