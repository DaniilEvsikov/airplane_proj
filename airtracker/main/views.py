from django.shortcuts import render
from FlightRadar24.api import FlightRadar24API
from django.urls import path
from pprint import pprint

fr_api = FlightRadar24API()

def main(request):
    answer = {}
    if request.method == "POST":
        answer = {}
        if "find" in request.POST:
            try:
                name = request.POST['name']
                try:
                    list=fr_api.get_airports()
                    for i in list:
                        if i['name']==name:
                            airport_icao=i['icao']
                    lukla_airport = fr_api.get_airport(airport_icao)

                    answer = {
                        'airport_name': lukla_airport['name'],
                        'airport_icao': lukla_airport['code']['icao'],
                        'country_name': lukla_airport['position']['country']['name'],
                        'airport_latitude': lukla_airport['position']['latitude'],
                        'airport_longitude': lukla_airport['position']['longitude'],
                        'airport_city': lukla_airport['position']['region']['city'],
                        'airport_offsetHours': lukla_airport['timezone']['offsetHours']
                    }
                except:
                    print("name")
            except:
                answer = {"error", True}
        if "find_plane" in request.POST:
            answer = {}
            try:
                name = request.POST['namepl']
                flight = fr_api.get_flights(registration=name)
                print(flight)
                print(flight[0])
                details = fr_api.get_flight_details(flight[0].id)

                answer = {
                    'plane_1': details['airport']['destination']['name'],
                    'plane_2': details['airport']['destination']['code']['icao'],
                    'plane_3': details['airport']['origin']['name'],
                    'plane_4': details['airport']['origin']['code']['icao'],
                    'plane_5': details['airline']['name'],
                    'plane_6': details['aircraft']['images']['medium'][0]['src']
                    }
            except:
                print("lol")
    return render(request, "main/index.html", answer)


def index(request):
    return render(request, 'main/index.html')

def about(request):
    return render(request, 'main/about.html')

def info(request):
    for flight in fr_api.get_flights():
        details = fr_api.get_flight_details(flight.id)
        flight.set_flight_details(details)
        return (f"Flying (id {flight.id}) is to {flight.destination_airport_name}")

def time(request):
    return ('время')