﻿#!/usr/bin/python

import json
import requests
import re
import logging

logger = logging.getLogger(__name__)

"""api_caller module

This module formats information for API calls and then
makes the call to the respective API.

"""
# API Keys
weather_api_key = '6c0b081fbb4411e1fc3d6836fe090fed'
place_api_key = 'AIzaSyDUichhgIGA_Tmc8i_yz-Rb3gmmSiuTZxQ'
news_api_key = 'c743d7069e6a4f4b95e800e6915f2612'
directions_api_key = 'AIzaSyChHK_pRbyKc3BrrpqIp4MvCzcHPimfrDQ'

#Making API call to weather API.
def weather_call(query):
	logger.debug('Weather query: %s' % query)
	payload = {'appid':weather_api_key,'q':query,'units':'metric'}
	data = requests.get('http://api.openweathermap.org/data/2.5/weather', params=payload).json()

	if (str(data['cod']) == "200"):
		_title1 = "Current Weather---"
		_cityName = "City Name: " + (data["name"])
		_clouds = ("Condition: " + data["weather"][0]["description"])
		_temp = "Temperature: " + str(data["main"]["temp"]) + "C"
		_humidity = "Humidity: " + str(data["main"]["humidity"]) + "%"
		_cityID = data["id"]
		payload = {'appid':weather_api_key,'q':query,'units':'metric'}
		data = requests.get('http://api.openweathermap.org/data/2.5/forecast', params=payload).json()
		_title2 = "3 Day Forecast---"
		_date1 = str(data['list'][3]['dt_txt']) + "\n"
		_date1, g1 = _date1.split(" ")
		_day1 = "Temp: " + str(data['list'][3]['main']['temp_min']) + "C \n Condition: " + str(data['list'][3]['weather'][0]['description'])
		_date2 = str(data['list'][11]['dt_txt']) + "\n"
		_day3 = "Temp: " + str(data['list'][11]['main']['temp_min']) + "C \n Condition: " + str(data['list'][11]['weather'][0]['description'])
		_date2, g2 = _date2.split(" ")
		_day2 = "Temp: " + str(data['list'][19]['main']['temp_min']) + "C \n Condition: " + str(data['list'][19]['weather'][0]['description'])
		_date3 = str(data['list'][19]['dt_txt']) + "\n"
		_date3, g3 = _date3.split(" ")
		output = (_cityName + "\n" + _title1 + "\n" + _clouds + "\n" + _temp + "\n" + _humidity  + "\n" + _title2 + "\n" + _date1 + " " + _day1
				+ "\n" + _date2 + " " + _day2 + "\n" + _date3 + " " + _day3)
		logger.debug('Results found')
		return output
	else:  #if no results found
		logger.debug('ERROR with news query')
		output = "Unable to return results for weather at this time."
		return output

#Making API Call to news api
def news_call(source):
	logger.debug('News query: %s' % source)

	payload = {'source':source,'apiKey':news_api_key}
	data = requests.get('https://newsapi.org/v1/articles', params=payload).json()

	#if results are found
	if (str(data['status']) == "ok"):
		count = len(data['articles'])
		for i in range (3):
			_title = "Title: " + data['articles'][i]['title']
			_desc =  "Description: " + data['articles'][i]['description']
			output = "\n" + _title + "\n" + _desc
	else:
		output = "Unable to return results for news at this time."
		logger.debug('ERROR with news query')
	logger.debug('Results found')
	return output

def places_call(place_type, address):
	logger.debug('Places query: %s at %s' % (place_type, address))
	place_types_dict = {'hospital','atm', 'food', 'restaurant','hindu_temple', 'university', 'veterinary_care',
		'travel_agency', 'transit_station', 'train_station', 'taxi_stand', 'subway_station', 'store',
		'storage', 'stadium', 'spa', 'shopping_mall', 'shoe_store', 'school' ,'rv_park', 'roofing_contractor',
		'real_estate_agency', 'post_office', 'police', 'plumber', 'physiotherapist', 'pharmacy','car_rental',
		'car_repair', 'car_wash', 'casino', 'cemetry', 'pet_store', 'parking', 'park', 'painter', 'night_club',
		'museum', 'moving_company', 'movie_theatre', 'mosque', 'meal_takeaway', 'meal_delivery', 'lodging',
		'locksmith', 'local_government_office', 'liquor_store', 'library', 'lawyer', 'laundry', 'jewelry_store',
		'insuarance_agency','accounting', 'amusement_park', 'art_gallery', 'bakery', 'bank', 'bar', 'beauty_salon',
		'book_store', 'bowling_alley', 'bus_station', 'cafe', 'campground', 'car_dealer','clothing_store',
		'convenience_store', 'courthouse', 'dentist', 'department_store', 'doctor', 'electrician',
		'electronics_store', 'embassy', 'florist', 'funeral_home' ,'furniture_store', 'gas_station',
		'gym','hair_care', 'hardware_store'}

	payload = {'query':place_type+address,'key':place_api_key}
	r = requests.get('https://maps.googleapis.com/maps/api/place/textsearch/json', params=payload).json()
	output = ''
	
	if (str(r['status']) == "OK"): #if results are found
		count=len(r['results'])
		if (count > 3):
			count = 3

		for i in range(count):
			if ('permanently_closed' not in r['results'][i]):
				_name = "Name: " + r['results'][i]['name']
				_address = "Address: " + r['results'][i]['formatted_address']
				#query to get phone number
				place_id = r['results'][i]['place_id']
				payload = {'placeid':place_id,'key':place_api_key}
				r2 = requests.get('https://maps.googleapis.com/maps/api/place/details/json', params=payload).json()
			
	
				#store phone number into variable
				_phone = "Phone No: " +  r2['result']['formatted_phone_number']

				if (place_type in place_types_dict):
					output = output + "\n" + _name + "\n" + _address + "\n" + _phone
				else:   #for names not in dictionary
					_rating = "Rating: " + str(r['results'][i]['rating'])
					#_openStatus =  "Open: " + str(r['results'][i]['opening_hours']['open_now'])
					output = output + "\n" + _name + "\n" + _address + "\n" + _rating + "\n" + _phone
			elif ('permanently_closed' in r['results'][i]):
				output = 'Place searched for is permanently closed.'
				return output
		if (output == ''):
			logger.debug('No Results found')
			output = 'No results found.'
			
		else:
			logger.debug('Results found')
			return output
	#if no results found
	else:
		logger.debug('ERROR with places query')
		output = "Unable to return results for places at this time."
		return output

#Making API call to directions API.
def directions_call(start, end):
	logger.debug('Directions query start: %s and end: %s' % (start, end))
	output = ''
	start = start.replace(" ", "+");
	end = end.replace(" ", "+");
	payload = {'origin':start,'destination':end,'key':directions_api_key}
	r = requests.get('https://maps.googleapis.com/maps/api/directions/json', params=payload).json()

	#if results are found
	if (str(r['status']) == "OK"):
		#store start, end, total distance, and total time into variables
		_start = "Start: " + r['routes'][0]['legs'][0]['start_address']
		_end = "End: " + r['routes'][0]['legs'][0]['end_address']
		_totalDist = "Total distance: " + r['routes'][0]['legs'][0]['distance']['text']
		_totalTime = "Total time: " + r['routes'][0]['legs'][0]['duration']['text']

		#Counts the number of steps towards destination
		stepCount = len(r['routes'][0]['legs'][0]['steps'])
		#display step by step directions

		for i in range(stepCount):
			instruction = str(r['routes'][0]['legs'][0]['steps'][i]['html_instructions'])
			#adds spacing to XML tags to avoid format errors
			instruction = instruction.replace("><", "> <")
			instruction = instruction.replace(")<", ") <")
			#deletes everything between <> in relation to XML tags
			instruction = re.sub(r'<.*?>', '', instruction)
			#store time and distance into variables
			time = str(r['routes'][0]['legs'][0]['steps'][i]['duration']['text'])
			distance = str(r['routes'][0]['legs'][0]['steps'][i]['distance']['text'])
			#concatenate the steps to output
			stepString = "Step " + str(i+1) + ": "+ instruction + "  [" + time + " (" + distance + ")]\n"
			output = output + stepString
		#concatenate start,end,total distance, and total time to final output
		output = "\n" + _start + "\n" + _end + "\n" + _totalDist + "\n" + _totalTime + "\n" + output
		logger.debug('Results found')
		return output
	else: #if no results found
		output = "Unable to return results for places at this time."
		logger.debug('ERROR with directions query')
		return output

def gas_call(address):
	logger.debug('Gas prices query at: %s' % address)
	gas_buddy_url = "https://www.gasbuddy.com/Home/Search"
	payload = {"s":address}
	r = requests.post(gas_buddy_url, payload)
	output = ''
	if (r.status_code == 200):
		r = r.json()
		count = len(r['stations'])
		if (count > 4):
			count = 4
		for i in range(count):
			name = "Name: " + r['stations'][i]['Name']
			address = "Address: " + r['stations'][i]['CrossSt']
			if (r['stations'][i]['CheapestFuel']['CreditPrice'] is not None):
				price = "Price: $" + str(r['stations'][i]['CheapestFuel']['CreditPrice']['Amount'])
			else:
				price = "Price: $" + str(r['stations'][i]['CheapestFuel']['CashPrice']['Amount'])
			output += (name + '\n' + address + '\n' + price + '\n')
		logger.debug('Results found')
		return output
	else:
		logger.debug('ERROR with gas prices query')
		output = "Unable to return results for gas prices at this time."
		return output
