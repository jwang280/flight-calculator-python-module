"""
Title: "Flight Travel Calculator"
Author: Jiangwei Wang
Student ID: 19364744
Date: 29/05/2020
"""

"""This program builds an user interface, it is called "Flight travel 
Cauculator". The user choose departing country from the combobox first, then 
there will be a list of airport deports available to choose from the departing 
airport combobox, it is a list of deport names  belongs to that country user 
just selected. Choose an departing airport as a following step. Then choose the 
arriving country from the destination section, the list of airport deport names 
will available to be selected from the arriving airport combobox. Finally, click 
the "calculate" button to show the distance in kilometres and fly time duration 
between the selected two airports.
"""


import math
import numpy as np
from tkinter import *
from tkinter.ttk import *



class AviationGui(object):
    """A class for the GUI interface to calculate distance and fly duration time 
    between two airports selected by user. The calculation is based on a 
    datatbase, which contains information about the airports' name, country, and 
    their specified longitudes and latitudes, arround the world.
    """
    
    
    def __init__(self, window, file):
        """Define the database and pass it onto other functions to use. Setup 
        the interface window with widget set, determine their lay out and event 
        binding. This window has 9 labels, two of them are linked to event 
        respond. It also has 4 scrollbars and 1 button to trigger the 
        calculation method.
        """ 
        self.file = file
        self.label = Label(window, text="Flight Travel Calculator", 
                           font=("Arial", 22))
        self.label.grid(row=0, column=0, columnspan=3, padx=(50, 0), 
                        pady=(30, 20))
        self.label_depart = Label(window, text="Departure", font=("Arial", 18))
        self.label_depart.grid(row=1, column=1, columnspan=1, pady=10)  
        country_names = self.country_list()[4:]
        self.country_depart_combobox = Combobox(window, values=country_names, 
                                                width=25, font=("Arial", 15))
        self.country_depart_combobox.grid(row=2, column=0, padx=(50, 0), 
                                          pady=10)
        self.country_depart_combobox.bind('<<ComboboxSelected>>', 
                                          self.show_city_depart)
        self.label_country_depart = Label(window, text="Country", 
                                          font=("Arial", 15))
        self.label_country_depart.grid(row=2, column=1, sticky=W, pady=10)        
        self.city_depart_combobox = Combobox(window, 
                                             values="Choose_country_first", 
                                             width=25, font=("Arial", 15))
        self.city_depart_combobox.grid(row=2, column=2, pady=10)
        self.label_airport_depart = Label(window, text="Airport", 
                                          font=("Arial", 15))
        self.label_airport_depart.grid(row=2, column=3, sticky=W, padx=(0, 50), 
                                       pady=10) 
        self.label_dest = Label(window, text="Destination", font=("Arial", 18))
        self.label_dest.grid(row=3, column=1, pady=10)  
        self.country_arrive_combobox = Combobox(window, values=country_names, 
                                                width=25, font=("Arial", 15))
        self.country_arrive_combobox.grid(row=4, column=0, padx=(50, 0), 
                                          pady=10)
        self.country_arrive_combobox.bind('<<ComboboxSelected>>', 
                                          self.show_city_arrive)
        self.label_country_arrive = Label(window, text="Country", 
                                          font=("Arial", 15))
        self.label_country_arrive.grid(row=4, column=1, sticky=W, pady=10)        
        self.city_arrive_combobox = Combobox(window, 
                                             values="Choose_country_first", 
                                             width=25, font=("Arial", 15))
        self.city_arrive_combobox.grid(row=4, column=2, pady=10)
        self.label_airport_arrive = Label(window, text="Airport", 
                                          font=("Arial", 15))
        self.label_airport_arrive.grid(row=4, column=3, sticky=W, padx=(0, 50), 
                                       pady=10)
        self.label_distance = Label(window, text="Please choose depots first.", 
                                    font=("Arial", 15))
        self.label_distance.grid(row=5, column=0, padx=(50, 0), pady=10, 
                                 columnspan=3)
        template_label = "Then click the button to view distance and duration."
        self.label_time = Label(window, text=template_label, 
                                font=("Arial", 15))
        self.label_time.grid(row=6, column=0, pady=10, padx=(50, 0), 
                             columnspan=3)
        frame_button = Frame(window, borderwidth=8, relief=RIDGE)
        frame_button.grid(row=7, column=1, pady=(10, 30))       
        self.button = Button(frame_button, text="Calculate", command=self.
                             show_distance)
        self.button.grid(row=7, column=1)       
        for i in range(0, 4):
            window.columnconfigure(i, weight=1)
        for i in range(0, 8):
            window.rowconfigure(i, weight=1)
        
        
        
    def country_list(self):
        """Collect a list of country names from the given database, which have 
        one or more airports. It is for the use of country selection scrollbars 
        from both departure and destination sections.
        """
        country_names = set()
        for line in self.datafile(self.file):
            country_names.add(line.split(',')[3].strip('""'))
        return sorted(country_names)
    
    
    def show_city_depart(self, event_depart):
        """This is an event respond fuction. It generates a list of airports 
        name of the coutry, which selected by the user from the country 
        scrollbar in the departure section, to define the departing airport.
        """
        country_depart = self.country_depart_combobox.get()
        self.city_depart = set()
        for line in self.datafile(self.file):
            if line.split(',')[3].strip('""') == country_depart:
                self.city_depart.add(line.split(',')[2].strip('""'))
        airport_depart = sorted(self.city_depart)
        self.city_depart_combobox['values'] = airport_depart
        self.city_depart_combobox.selection_clear()
    
    
    def show_city_arrive(self, event_arrive):
        """This is an event respond fuction. It generates a list of airports 
        name of the coutry, which selected by the user from the country 
        scrollbar in the destination section, to define the arrival airport.
        """        
        country_arrive = self.country_arrive_combobox.get()
        self.city_arrive = set()
        for line in self.datafile(self.file):
            if line.split(',')[3].strip('""') == country_arrive:
                self.city_arrive.add(line.split(',')[2].strip('""'))
        airport_arrive = sorted(self.city_arrive)
        self.city_arrive_combobox['values'] = airport_arrive
        self.city_arrive_combobox.selection_clear()    
        
        
    def show_distance(self):
        """Pass both selected departing and arrival airport names to other 
        functions to caculate the distance inbetween. Show the distance on the 
        window by changing the label message. It also calculate the flight 
        duration time by assume the avarage flying speed is 835 kilometres per 
        hour, and show the time on the label message too.
        """
        city_depart = self.city_depart_combobox.get()
        city_arrive = self.city_arrive_combobox.get()
        distance = self.distance(city_depart, city_arrive)
        flght_time = distance / 835
        template_distance = "Distance: {:.2f} kilometers"
        self.label_distance['text'] = template_distance.format(distance)
        template_time = "Fly time: {0:02.0f} hour(s) {1:02.0f} minute(s)"
        self.label_time['text'] = (template_time).format(*divmod(float
                                                                 (flght_time) 
                                                                 * 60, 60))
        self.city_depart_combobox.selection_clear()
        self.city_arrive_combobox.selection_clear()        


    def radian(self, d):
        """Calculate radian by given number.
        """
        return d * math.pi / 180.0
    

    def distance_calculator(self, lat1, lng1, lat2, lng2):
        """Calculate distance from a to b by given latitudes and longitudes.
        """
        earth_redius = 6378.137
        radlat1 = AviationGui.radian(self, lat1)
        radlat2 = AviationGui.radian(self, lat2)
        a = radlat1 - radlat2
        b = AviationGui.radian(self, lng1) - AviationGui.radian(self, lng2)
        n = 2 * math.asin(np.sqrt(math.pow(np.sin(a/2), 2) + 
                                    np.cos(radlat1) * np.cos(radlat2) 
                                    * math.pow(np.sin(b/2), 2)))
        s = n * earth_redius
        return s


    def datafile(self, filename):
        """Open and read the contents from given database.
        """
        infile = open(filename)
        lines = infile.readlines()
        infile.close()
        result = set()
        for line in lines:
            result.add(line)
        return result  
    

    def distance(self, city_depart, city_arrive):
        """Return distance from one given city to another by lookup their 
        longitudes and latitudes parametres from given database, then pass them 
        to other functions to calculate.
        """ 
        for line in AviationGui.datafile(self, self.file):
            if line.split(',')[2].strip('""') == city_depart:
                lat_depart = float(line.split(',')[6])
                lng_depart = float(line.split(',')[7])
            if line.split(',')[2].lstrip('"').rstrip('"') == city_arrive:
                lat_arrive = float(line.split(',')[6])
                lng_arrive = float(line.split(',')[7])
        distance = AviationGui.distance_calculator(self, lat_depart, lng_depart, 
                                                   lat_arrive, lng_arrive)
        return distance   


def main():
    """Define the database name, find it and call the function and window for 
    this program to run.
    """
    file = 'airports.dat.txt'
    window = Tk()
    aviation_gui = AviationGui(window, file)
    window.mainloop()


if __name__ == '__main__':
    main()
