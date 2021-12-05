""" dockstring to make pylin happy.
"""


# import
import os
import uuid
import requests
import numpy as np
import pandas as pd
import plotly.express as px
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

# plot function
def plot(df, lat_col, lon_col, color_col, mapbox_token_file, figname, zoom=5) :
    # read token file
    px.set_mapbox_access_token(open(mapbox_token_file).read())

    # fig
    fig = px.scatter_mapbox(df, lat=lat_col, lon=lon_col,     
                        color=color_col, size=color_col,
                        color_continuous_scale=px.colors.cyclical.IceFire, 
                        size_max=15, zoom=zoom)

    # save fig
    fig.write_image(figname)
    # fig.show()

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

    # fetch best destinations
    top_5_destinations = weather_df.sort_values(by=['volume_rain_7days'])[:5]
    top_20_destinations = weather_df.sort_values(by=['volume_rain_7days'])[:20]
    display(top_5_destinations.sample(2))
    display(top_20_destinations.sample(2))

    # rename volume col
    top_5_destinations = top_5_destinations.rename(columns={"volume_rain_7days": "Volume of rain"})
    top_20_destinations = top_20_destinations.rename(columns={"volume_rain_7days": "Volume of rain"})

    # plot var
    # cols
    lat_col = "latitude"
    lon_col = "longitude"
    color_col = "Volume of rain"
    # token
    mapbox_token_file = "../.mapbox_token"

    # plot
    plot(top_5_destinations, lat_col, lon_col, color_col, 
        mapbox_token_file, "../data/temp/top_5_destinations.png")
    plot(top_20_destinations, lat_col, lon_col, color_col, 
        mapbox_token_file, "../data/temp/top_20_destinations.png", zoom=3.5)




