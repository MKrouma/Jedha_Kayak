""" docstring to make pylint happy.
"""

# import
import os 
import logging
import scrapy # type: ignore
from scrapy.crawler import CrawlerProcess # type: ignore


class bookingHotels(scrapy.Spider):
    # Name of your spider
    name = "booking_hotels"

    # Url to start your spider from 
    start_urls = [
        'https://www.booking.com/searchresults.fr.html?label=gen173nr-1FCAEoggI46AdIM1gEaE2IAQGYAQ24AQfIAQzYAQHoAQH4AQuIAgGoAgO4Arm1mo0GwAIB0gIkZjE3NDZhZDItOTUyYS00NjljLWE5N2ItNzUxZjIxMTdjNDdi2AIG4AIB&sid=a8d69dac58d2b76c1d2bb743d5182840&aid=304142&sb_lp=1&src=index&error_url=https%3A%2F%2Fwww.booking.com%2Findex.fr.html%3Flabel%3Dgen173nr-1FCAEoggI46AdIM1gEaE2IAQGYAQ24AQfIAQzYAQHoAQH4AQuIAgGoAgO4Arm1mo0GwAIB0gIkZjE3NDZhZDItOTUyYS00NjljLWE5N2ItNzUxZjIxMTdjNDdi2AIG4AIB%3Bsid%3Da8d69dac58d2b76c1d2bb743d5182840%3Bsb_price_type%3Dtotal%26%3B&ss=Bormes-les-Mimosas%2C+Provence-Alpes-C%C3%B4te+d%27Azur%2C+France&is_ski_area=&checkin_year=&checkin_month=&checkout_year=&checkout_month=&group_adults=2&group_children=0&no_rooms=1&b_h4u_keep_filters=&from_sf=1&ss_raw=bormes&ac_position=0&ac_langcode=fr&ac_click_type=b&dest_id=-1413801&dest_type=city&place_id_lat=43.1507&place_id_lon=6.34193&search_pageview_id=2cde989cc7530174&search_selected=true&search_pageview_id=2cde989cc7530174&ac_suggestion_list_length=5&ac_suggestion_theme_list_length=0&nflt=ht_id%3D204&offset=25',
    ]

    # Callback function that will be called when starting your spider
    # It will get text, author and tags of the first <div> with class="quote"
    def parse(self, response):
        hotel = response.css('a.fb01724e5b')
        # div.sr__card.js-sr-card

        print(f"\n\nHOTEL : {hotel}\n")
        return {
            'hotel_name': hotel.css('div.fde444d7ef._c445487e2::text').get(),
            # 'hotel_name': hotel.css('div._7192d3184 div div._29c344764 div div._f57705597 div div._29c344764 div h3 a div.fde444d7ef::text').get(),
            # 'author': quote.css('span small.author::text').get(),
            # 'tags': quote.css('div.tags a.tag::text').getall(),
        }


if __name__ == "__main__" :

    # Name of the file where the results will be saved
    booking_data_json = "../data/temp/scrape_booking.json"

    # delete filename if exists
    if os.path.exists(booking_data_json):
            os.remove(booking_data_json)

    # scrawler process
    process = CrawlerProcess(settings = {
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'LOG_LEVEL': logging.INFO,
        "FEEDS": {
            booking_data_json : {"format": "json"},
        }
    })

    # run scraling using spider
    process.crawl(bookingHotels)
    process.start()