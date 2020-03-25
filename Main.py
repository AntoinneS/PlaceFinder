import googlemaps
import json
from tkinter import *
import tkinter.messagebox
import pprint
import xlsxwriter
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

global latitude
global longitude
global tkvar
longitude = 0
latitude = 0

#add database window class
def getCurrentLocation():
    global latitude
    global longitude
    options = Options()
    options.add_argument("--use-fake-ui-for-media-stream")
    timeout = 20
    driver = webdriver.Chrome(executable_path = 'chromedriver.exe', options=options)
    driver.get("https://mycurrentlocation.net/")
    wait = WebDriverWait(driver, timeout)
    time.sleep(3)
    longitude = driver.find_elements_by_xpath('//*[@id="longitude"]')
    longitude = [x.text for x in longitude]
    longitude = str(longitude[0])
    latitude = driver.find_elements_by_xpath('//*[@id="latitude"]')
    latitude = [x.text for x in latitude]
    latitude = str(latitude[0])
    driver.quit()
    return (latitude, longitude)


class SearchWindow:
    def __init__(self):
        top = Tk()
        top.configure(bg='#434774')
        top.title('Seacher')
        global tkvar
        # Add a grid
        mainframe = Frame(top)
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)
        mainframe.pack(pady=100, padx=100)

        # Create a Tkinter variable
        tkvar = StringVar(top)

        # Dictionary with options
        choices = {'accounting','airport','amusement_park','aquarium','art_gallery','atm','bakery','bank','bar','beauty_salon','bicycle_store','book_store','bowling_alley','bus_station','cafe','campground','car_dealer','car_rental','car_repair','car_wash','casino','cemetery','church','city_hall','clothing_store','convenience_store','courthouse','dentist','department_store','doctor', 'drugstore','electrician','electronics_store','embassy','fire_station','florist','funeral_home','furniture_store','gas_station','grocery_or_supermarket','gym','hair_care','hardware_store','hindu_temple','home_goods_store','hospital','insurance_agency','jewelry_store','laundry', 'lawyer','library','light_rail_station','liquor_store','local_government_office','locksmith','lodging','meal_delivery','meal_takeaway','mosque','movie_rental','movie_theater','moving_company','museum','night_club','painter','park','parking','pet_store','pharmacy','physiotherapist','plumber','police','post_office','primary_school','real_estate_agency','restaurant','roofing_contractor','rv_park','school','secondary_school','shoe_store','shopping_mall','spa','stadium','storage','store','subway_station','supermarket','synagogue','taxi_stand','tourist_attraction','train_station','transit_station','travel_agency','university','veterinary_care','zoo',
}
        tkvar.set('doctor')  # set the default option

        popupMenu = OptionMenu(mainframe, tkvar, *choices)
        Label(mainframe, text="What do you Want").grid(row=1, column=1)
        popupMenu.grid(row=2, column=1)

        # on change dropdown value
        def change_dropdown(*args):
            print(tkvar.get())

        # link function to change dropdown
        tkvar.trace('w', change_dropdown)
        B1 = Button(top,text="Accept", fg='#D5D9FE', bg='#37394C', command = getPlaces)
        B1.place(x=240, y=150)
        top.geometry("500x300+20+20")
        top.mainloop()

def getPlaces():
    global latitude
    global longitude
    global tkvar
    place = tkvar.get()
    # Define the API Key.
    API_KEY = ''

    # Define the Client
    gmaps = googlemaps.Client(key=API_KEY)

    # Do a simple nearby search where we specify the location
    # in lat/lon format, along with a radius measured in meters
    places_result = gmaps.places_nearby(location=(latitude, longitude), radius=40000, open_now=True,
                                        type= place)

    time.sleep(3)

    # place_result = gmaps.places_nearby(page_token=places_result['next_page_token'])

    stored_results = []

    # loop through each of the places in the results, and get the place details.
    for place in places_result['results']:
        # define the place id, needed to get place details. Formatted as a string.
        my_place_id = place['place_id']

        # define the fields you would liked return. Formatted as a list.
        my_fields = ['name', 'formatted_phone_number', 'price_level', 'website', 'rating']

        # make a request for the details.
        places_details = gmaps.place(place_id=my_place_id, fields=my_fields)

        # print the results of the details, returned as a dictionary.
        pprint.pprint(places_details['result'])

        # store the results in a list object.
        stored_results.append(places_details['result'])

    # -------------- DUMPING VALUES IN EXCEL -----------------------

    # define the headers, that is just the key of each result dictionary.
    row_headers = stored_results[0].keys()

    # create a new workbook and a new worksheet.
    workbook = xlsxwriter.Workbook(r'D:\FoodFinderInfo.xlsx')
    worksheet = workbook.add_worksheet()

    # populate the header row
    col = 0
    for header in row_headers:
        worksheet.write(0, col, header)
        col += 1

    row = 1
    col = 0
    # populate the other rows

    # get each result from the list.
    for result in stored_results:

        # get the values from each result.
        result_values = result.values()

        # loop through each value in the values component.
        for value in result_values:
            worksheet.write(row, col, value)
            col += 1

        # make sure to go to the next row & reset the column.
        row += 1
        col = 0

    # close the workbook
    workbook.close()



#Main window class
class MainWindow:
    def __init__(self, win1):
        self.B3 = Button(win1, bg='#37394C', text = "Google Api Searcher", fg = '#D5D9FE',  command = self.dsearch)
        self.B3.place(x = 150,y = 140)

# Display diagnosis window
    def dsearch(self):
        getCurrentLocation()
        SearchWindow()

#Displays main window
top1=Tk()
mywin1=MainWindow(top1)
top1.title('Main Menu')
top1.configure(bg='#434774')
top1.geometry("400x300+20+20")
top1.mainloop()
