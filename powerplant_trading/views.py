from django.shortcuts import render
from django.http import JsonResponse
import json
import math
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def getproductionplan(request):
	if request.method == 'POST':
		payloads = json.loads(request.body)
	else:
		with open('powerplant_trading/example.json') as json_file:
			payloads = json.load(json_file)

	#compute MWh cost for each station
	merit_order = []
	for idx, powerplant in enumerate(payloads['powerplants']):
		if powerplant['type'] == 'windturbine':
			cost_per_hour = 0
			#taking wind power into account
			powerplant['pmax'] = math.floor((payloads['fuels']["wind(%)"] * powerplant['pmax'])/10) / 10
		if powerplant['type'] == 'turbojet':
			cost_per_hour = payloads['fuels']["kerosine(euro/MWh)"] / powerplant['efficiency']
		if powerplant['type'] == 'gasfired':
			#taking CO2 emission into account
			cost_per_hour = payloads['fuels']["gas(euro/MWh)"] / powerplant['efficiency'] + 0.3 * payloads['fuels']["co2(euro/ton)"]
		merit_order.append((cost_per_hour ,idx))
	payload_response = []
	load = payloads['load']
	#start from cheapest power station to the most expensive one
	for cost,idx in sorted(merit_order):
		if load - payloads['powerplants'][idx]['pmax'] > 0:
			p = payloads['powerplants'][idx]['pmax']
		elif (payloads['powerplants'][idx]['pmin'] > load) and (load > 0):
			p = payloads['powerplants'][idx]['pmin']
			payload_response[-1]['p'] -= ( p - load)
			load += ( p - load)
		else:
			p = load
		load -= p
		payload_response.append({"name":payloads['powerplants'][idx]['name'],"p":p})
	return JsonResponse(payload_response,safe=False)