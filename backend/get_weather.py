""" dockstring to make pylin happy.
"""


# import
import os
import uuid
import requests
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from IPython.display import display
from geopy.geocoders import Nominatim

## Utils functions
# coordinates of cities
def cities_to_coords(city_name) :
    """ get cities coordiniates.
    """

    # geocoder
    geolocator = Nominatim(user_agent="app")
    location = geolocator.geocode(city_name)

    # full_address, latitude, longitude
    full_address = location.address
    latitude = location.latitude
    longitude = location.longitude

    # return 
    return pd.Series([full_address, latitude, longitude])

# volume rain from oepn weather
def volume_rain(lat, lon, exclude, appid) :
    """ volume of rain in each city over 7 next days.
    """

    # open weather one call api
    params = (
        ('lat', lat),
        ('lon', lon),
        ('exclude', exclude),
        ('appid', appid)
    )

    response = requests.get('https://api.openweathermap.org/data/2.5/onecall', params=params)

    # normalize reponse
    open_weather_7days = pd.json_normalize(response.json()["daily"])

    # clean rain column
    open_weather_7days["rain"] = open_weather_7days["rain"].apply(lambda x : 0 if np.isnan(x) else x) 

    # calculate volumn 
    n_days = open_weather_7days.shape[0]
    volume_rain_7days =  np.sum(open_weather_7days["rain"] * open_weather_7days["pop"]) / n_days

    # return 
    return round(volume_rain_7days,3)


## Workflow
# env variables
load_dotenv()
OPEN_WEATHER_TOKEN = os.getenv('Open_weather_token')

# french top 35 cities
french_top_35 = ["Mont Saint Michel", "St Malo", "Bayeux", "Le Havre",
                "Rouen", "Paris", "Amiens", "Lille", "Strasbourg",
                "Chateau du Haut Koenigsbourg", "Colmar", "Eguisheim",
                "Besancon", "Dijon", "Annecy", "Grenoble", "Lyon",
                "Gorges du Verdon", "Bormes les Mimosas", "Cassis",
                "Marseille", "Aix en Provence", "Avignon", "Uzes", "Nimes",
                "Aigues Mortes", "Saintes Maries de la mer", "Collioure",
                "Carcassonne", "Ariege", "Toulouse", "Montauban", "Biarritz",
                "Bayonne", "La Rochelle"]

# dataset
weather_data = "../data/temp/weather_data.csv"
overwrite = True 

if not os.path.exists(weather_data) or overwrite==True:

    # init dataframe
    weather_df = pd.DataFrame(french_top_35, columns=["cities"])
    display(weather_df.sample(2))

    # cities to coords
    if not "full_address" in weather_df.columns :
        weather_df[["full_address", "latitude", "longitude"]] = weather_df["cities"].apply(cities_to_coords)
        display(weather_df.sample(2))

    else : 
        display(weather_df.sample(2))
        print("full_address, latitude & longitude columns exists !")

    # fill weather_df
    exclude = 'current,minutely,hourly,alerts'
    appid = OPEN_WEATHER_TOKEN
    if not "volume_rain_7days" in weather_df.columns :
        weather_df["volume_rain_7days"] = weather_df[["latitude", "longitude"]].transpose().apply(lambda x : volume_rain(x[0], x[1], exclude, appid))

    display(weather_df.sample(2))

    # unique identifier (uuid)
    if not "uuid" in weather_df.columns :
        weather_df['uuid'] = weather_df.index.to_series().map(lambda x: uuid.uuid4())

    display(weather_df.sample(2))

    # reorder columns
    keep_col = ['uuid', 'cities', 'full_address', 'latitude', 'longitude', 'volume_rain_7days']
    weather_df = weather_df[keep_col]

    display(weather_df.sample(2))

    # save dataframe
    weather_df.to_csv(weather_data)

    # plot best destinations
    top_5_destinations = weather_df.sort_values(by=['volume_rain_7days'])[:5]
    display(top_5_destinations)


