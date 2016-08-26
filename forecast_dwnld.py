# This script downloads weather forecast data given in XML format on weather.gov
# For Location: West Lafayette

# Extend this for three locations in USA and save data ini files with current time stamp

from lxml import html
import requests, pickle
from datetime import datetime
import time
import numpy as np

class data_tree:
    def __init__(self, tree):
        self.tree = tree 
        
    def date_time(self):
        # Each measurement is taken as the average equipment value over four minutes
        start_time = self.tree.xpath('//start-valid-time/text()')
        date = []
        time = []
        for element in start_time:
            date_time = element.split('T')
            date.append(date_time[0])
            time.append(date_time[1].split('-')[0])
        return date, time
        
    def temp_weather_data(self):
        dew_point_temp = self.tree.xpath('//temperature[@type="dew point"]//value/text()')
        hourly_temp = self.tree.xpath('//temperature[@type="hourly"]//value/text()')
        cloud_amount = self.tree.xpath('//cloud-amount[@type="total"]//value/text()')
        return dew_point_temp, hourly_temp, cloud_amount
    
    def save_data(self):
        date, time = self.date_time()
        dew_point_temp, hourly_temp, cloud_amount = self.temp_weather_data()
        
        # Save file with current hourly time stamp
        val = datetime.now()
        filename = str(val.year)+'_'+ str(val.month)+'_'+str(val.day)+'_'+str(val.hour)+'.pcl'
        f = open(filename, "wb")
        pickle.dump(date, f)
        pickle.dump(time, f)
        pickle.dump(np.asarray(dew_point_temp), f)
        pickle.dump(np.asarray(hourly_temp), f)
        pickle.dump(np.asarray(cloud_amount), f)
        f.close()
        return filename
        
        
        
    def read_data(self, filename = '2016_8_25_18.pcl'):
    # Just for reference and checking the stored data
        f = open(filename, "r")
        date = pickle.load(f)
        time = pickle.load(f)
        dew_point_temp = pickle.load(f)
        hourly_temp = pickle.load(f)
        cloud_amount = pickle.load(f)
        f.close()
        
        return date, time, dew_point_temp, hourly_temp, cloud_amount
       

page = requests.get('http://forecast.weather.gov/MapClick.php?lat=40.4447&lon=-86.9119&FcstType=digitalDWML')
tree = html.fromstring(page.content)
savedata = data_tree(tree)
print savedata.save_data()

# print savedata.read_data()
# Length testing for function output done

while True:
    page = requests.get('http://forecast.weather.gov/MapClick.php?lat=40.4447&lon=-86.9119&FcstType=digitalDWML')
    tree = html.fromstring(page.content)
    savedata = data_tree(tree)
    print savedata.save_data()
    time.sleep(24*60)