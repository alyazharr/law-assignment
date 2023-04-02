import json
import requests

def get_today_weather_by_province(provinsi: str) -> dict:
    url = "https://cuaca-gempa-rest-api.vercel.app/weather"
    url = url+"/"+provinsi
    response = requests.get(url)

    final_response = {}

    json_resp = json.loads(response.text)["data"]
    time_data = json_resp["issue"]["day"]+"-"+json_resp["issue"]["month"]+"-"+json_resp["issue"]["year"]

    final_response["waktu"] = time_data
    final_response["kota"] = []

    # iterasi per daerah
    for area in json_resp["areas"]:
        cuaca_per_kota = {}
        cuaca_per_kota['nama'] = area["description"]

        if "params" in area:
            for type_data in area["params"]:
                if type_data["id"] == "weather":
                    cuaca_per_kota['cuaca'] = []
                    weather = type_data["times"] # akses per waktu

                    dawn = weather[0]['name']
                    morning = weather[1]['name']
                    afternoon = weather[2]['name']
                    evening = weather[3]['name']

                    date = weather[0]['datetime'][:8]
                    formatted_date = f"{date[6:]}-{date[4:6]}-{date[:4]}"
                        
                    cuaca_per_kota['cuaca'].append({
                        'tanggal': formatted_date,
                        'waktu': {
                            'dini_hari': dawn,
                            'pagi': morning,
                            'siang': afternoon,
                            'sore': evening
                        }
                    })
        final_response["kota"].append(cuaca_per_kota)

    return final_response

def get_weather_forecast_by_province(provinsi: str) -> dict:
    url = "https://cuaca-gempa-rest-api.vercel.app/weather"
    url = url+"/"+provinsi
    
    response = requests.get(url)
    final_response = {}
    json_resp = json.loads(response.text)["data"]
    time_data = json_resp["issue"]["day"]+"-"+json_resp["issue"]["month"]+"-"+json_resp["issue"]["year"]

    final_response["waktu"] = time_data
    final_response["kota"] = []

    # iterasi per daerah
    for area in json_resp["areas"]:
        cuaca_per_kota = {}
        cuaca_per_kota['nama'] = area["description"]

        if "params" in area:
            for type_data in area["params"]:
                if type_data["id"] == "weather":
                    cuaca_per_kota['cuaca'] = []
                    weather = type_data["times"] # akses per waktu

                    for cnt in range(0, len(weather), 4):
                        dawn = weather[cnt]['name']
                        morning = weather[cnt+1]['name']
                        afternoon = weather[cnt+2]['name']
                        evening = weather[cnt+3]['name']

                        date = weather[cnt]['datetime'][:8]
                        formatted_date = f"{date[6:]}-{date[4:6]}-{date[:4]}"
                        
                        cuaca_per_kota['cuaca'].append({
                            'tanggal': formatted_date,
                            'waktu': {
                                'dini_hari': dawn,
                                'pagi': morning,
                                'siang': afternoon,
                                'sore': evening
                            }
                        })
        final_response["kota"].append(cuaca_per_kota)

    return final_response

def get_today_weather_by_city(provinsi:str, city: str) -> dict:
    url = "https://cuaca-gempa-rest-api.vercel.app/weather/"
    url = url+"/"+provinsi+"/"+city

    response = requests.get(url)

    final_response = {}
    json_resp = json.loads(response.text)["data"]

    final_response['nama'] = json_resp["description"]
    final_response['lokasi_geografi'] = json_resp["latitude"]+","+json_resp["longitude"]
    final_response['tanggal'] = None
    final_response['cuaca'] = {}

    if "params" in json_resp:
        for type_data in json_resp["params"]:
            if type_data["id"] == "weather":  
                weather = type_data["times"] # akses per waktu
                date = weather[0]['datetime'][:8]
                formatted_date = f"{date[6:]}-{date[4:6]}-{date[:4]}"
                final_response['tanggal'] = formatted_date

                dawn = weather[0]['name']
                morning = weather[1]['name']
                afternoon = weather[2]['name']
                evening = weather[3]['name']

                final_response['cuaca']['dini_hari'] = dawn
                final_response['cuaca']['pagi'] = morning
                final_response['cuaca']['siang'] = afternoon
                final_response['cuaca']['sore'] = evening
    return final_response

def get_weather_forecast_by_city(provinsi:str, city: str) -> dict:
    url = "https://cuaca-gempa-rest-api.vercel.app/weather/"
    url = url+"/"+provinsi+"/"+city
    response = requests.get(url)

    final_response = {}
    json_resp = json.loads(response.text)["data"]

    final_response['nama'] = json_resp["description"]
    final_response['cuaca'] = []

    if "params" in json_resp:
        for type_data in json_resp["params"]:
            if type_data["id"] == "weather":  
                weather = type_data["times"] # akses per waktu

                for cnt in range(0, len(weather), 4):                   
                    dawn = weather[cnt]['name']
                    morning = weather[cnt+1]['name']
                    afternoon = weather[cnt+2]['name']
                    evening = weather[cnt+3]['name']

                    date = weather[cnt]['datetime'][:8]
                    formatted_date = f"{date[6:]}-{date[4:6]}-{date[:4]}"
                        
                    final_response['cuaca'].append({
                            'tanggal': formatted_date,
                            'waktu': {
                                'dini_hari': dawn,
                                'pagi': morning,
                                'siang': afternoon,
                                'sore': evening
                            }
                        })                

    return final_response

# fungsi tambahan: rekomendasi berdasarkan cuaca yang tepat
def recommendation_togo_by_weather(cuaca:str, location:str, amount:int)-> dict:
    HUJAN = "art_gallery|restaurant|bakery|beauty_salon|clothing_store|department_store|amusement_park|bowling_alley" #segala macam jenis hujan
    CERAH = "amusement_park|park|beach|zoo|tourist_attraction" #cerah: cerah, cerah berawan, 
    BERAWAN = "museum|art_gallery|shopping_mall|movie_theater|cafe|park|department_store" #berawan: berawan, berawan tebal
    KABUT = "viewpoint|point_of_interest|locality|neighborhood" #kabut = asap/kabut 

    chosen_type = ''
    if cuaca.lower() in ["hujan ringan", "hujan lebat", "hujan sedang", "hujan lokal", "hujan lokal", "hujan petir"]:
        chosen_type=HUJAN
    elif cuaca.lower() in ["cerah", "cerah berawan"]:
        chosen_type=CERAH
    elif cuaca.lower() in ["berawan", "berawan tebal"]:
        chosen_type=BERAWAN
    else:
        chosen_type=KABUT

    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    API_KEY = "AIzaSyDNHerQ0w6zm4FxEnCbYfOUMXdYUZWLCwo"
    params = {
        "location": location,
        "radius":50000,
        "key":API_KEY,
        "type":chosen_type,
        "maxresults":10
    }

    response = requests.get(url, params=params) # dapet datanya

    final_response = {}
    json_resp = json.loads(response.text)["results"]
    final_response['cuaca'] = cuaca
    final_response['rekomendasi'] = []

    num_iter = 0
    if len(json_resp) > amount:
        num_iter = amount
    else:
        num_iter = len(json_resp)

    print("-- [START] pemanggilan --")
    for cnt in range(num_iter):
        print("**iterasi ke-",cnt)
        each_place = {}

        url = "https://maps.googleapis.com/maps/api/place/details/json"
        params = {
            "place_id":json_resp[cnt]["place_id"],
            "key":API_KEY
        }

        response_detail = requests.get(url, params=params) # dapet datanya
        json_resp_detail = json.loads(response_detail.text)["result"]

        each_place['nama'] = json_resp_detail['name']
        each_place['lokasi'] = json_resp_detail['formatted_address']
        each_place['id_tempat'] = json_resp[cnt]["place_id"]
        each_place['url_lokasi'] = json_resp_detail['url']
        each_place['tipe_wisata'] = json_resp_detail['types']
        final_response['rekomendasi'].append(each_place)
    print("-- [END] pemanggilan --")
    return final_response

def recommendation_togo_by_city_weather(provinsi:str, city:str, amount:int) -> dict:
    weather_data = get_today_weather_by_city(provinsi=provinsi, city=city)
    location = weather_data['lokasi_geografi']
    cuaca_pagi = weather_data['cuaca']['pagi']
    cuaca_siang = weather_data['cuaca']['siang']
    cuaca_sore = weather_data['cuaca']['sore']

    rekomendasi_pagi = recommendation_togo_by_weather(cuaca_pagi, location, amount)
    rekomendasi_siang = recommendation_togo_by_weather(cuaca_siang, location, amount)
    rekomendasi_sore = recommendation_togo_by_weather(cuaca_sore, location, amount)

    final_response = {}
    final_response['nama'] = weather_data['nama']
    final_response['rekomendasi_pagi'] = rekomendasi_pagi['rekomendasi']
    final_response['rekomendasi_siang'] = rekomendasi_siang['rekomendasi']
    final_response['rekomendasi_sore'] = rekomendasi_sore['rekomendasi']
    
    return final_response