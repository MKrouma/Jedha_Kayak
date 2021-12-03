""" docstring to make pylint happy.
"""

# import
import os
import json
import time
import pandas as pd
from IPython.display import display

# utils functions
# clean some text
def clean_text(text) :
    return text.replace("\n", "")


# run scrapy bash code as : booking.sh
def run_scrapy_bash() :
    os.chdir("./booking")
    cmd = "sh booking.sh"
    os.system(cmd)
    os.chdir("..")

# clean dataset
def explore_dataset(hotels_file, export_file) : 
    """ explore & clean dataset.
    """

    # file to json
    hotels_json = json.load(open(hotels_file))

    # json to df
    hotels_df = pd.json_normalize(hotels_json)

    # clean name, scrore, description
    hotels_df["name"] = hotels_df["name"].apply(lambda x : clean_text(x))
    hotels_df["score"] = hotels_df["score"].apply(lambda x : clean_text(x))
    hotels_df["description"] = hotels_df["description"].apply(lambda x : clean_text(x))

    # transform score object to float
    hotels_df["score"] = hotels_df["score"].astype(float)

    # save
    hotels_df.to_csv(export_file)

    # display
    display(hotels_df.columns)
    display(hotels_df.sample(3))


if __name__ == "__main__" : 
    hotels_file = "../data/temp/hotels_booking.json"
    export_hotels_csv = "../data/temp/hotels_booking.csv"

    if not os.path.exists(export_hotels_csv) : 
        run_scrapy_bash()
        explore_dataset(hotels_file, export_hotels_csv)

    else : 
        print(f"{export_hotels_csv} exists!")
        print("DONE !")