from django.shortcuts import render
from django.http import JsonResponse
import json
import math
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def getproductionplan(request):
	#Get JSON from POST request
	if request.method == 'POST':
		payloads = json.loads(request.body)
	#load example JSON from filesystem
	else:
		with open('powerplant_trading/example.json') as json_file:
			payloads = json.load(json_file)

	#compute MWh cost per hour for each station
	merit_order = []
	for idx, powerplant in enumerate(payloads['powerplants']):
		if powerplant['type'] == 'windturbine':
			#MWh cost per hour for wind turbines is always 0
			cost_per_hour = 0
			#using this condition to modify Pmax for windturbines to takes wind into account 
			#Formula for windturbines is : Pmax = Pmax * Wind(%)
			#This makes windturbines having the same behaviour as the other powerstations for computing P later on
			powerplant['pmax'] = math.floor((payloads['fuels']["wind(%)"] * powerplant['pmax'])/10) / 10
		elif powerplant['type'] == 'turbojet':
			cost_per_hour = payloads['fuels']["kerosine(euro/MWh)"] / powerplant['efficiency']
		elif powerplant['type'] == 'gasfired':
			#taking CO2 emission into account (optional)
			cost_per_hour = payloads['fuels']["gas(euro/MWh)"] / powerplant['efficiency'] + 0.3 * payloads['fuels']["co2(euro/ton)"]
		#handles bad powerstation type
		else:
			return JsonResponse({'error':'The JSON provided does not contains correct type for powerplants'}, status=500)
		#Stores MWh cost for each station. Tuple used for sorting latter
		merit_order.append((cost_per_hour ,idx))
	payload_response = []
	#store load value locally 
	load = payloads['load']
	#start from cheapest power station to the most expensive one
	for cost,idx in sorted(merit_order):
		# if the load left to produce is bigger than current station Pmax
		if load - payloads['powerplants'][idx]['pmax'] > 0:
			#makes the station power equals to Pmax
			p = payloads['powerplants'][idx]['pmax']
		#if the load left to produce is not bigger than Pmax and is smaller then Pmin
		#also makes sure there is still load left to be produced, otherwise Pmin is always bigger than 0
		elif (payloads['powerplants'][idx]['pmin'] > load) and (load > 0):
			#makes the station power equals to Pmin
			p = payloads['powerplants'][idx]['pmin']
			#Reduce power of previous station by the difference between current Pmin and load left to produce
			payload_response[-1]['p'] -= ( p - load)
			#add power reduced to last station to power left to produce
			load += ( p - load)
		#if load left to produce is between Pmin and Pmax
		else:
			#make station produce load left to produce
			p = load
		#reduce total power to produce by power produced by current station
		load -= p
		#add station name and power produced to JSON response
		payload_response.append({"name":payloads['powerplants'][idx]['name'],"p":p})
	#checks if there is still load to be produced
	if load !=0:
		return JsonResponse({'error':'Unable to compute a balanced load for each stations'}, status=500)
	return JsonResponse(payload_response,safe=False)