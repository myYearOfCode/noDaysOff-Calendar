#!/usr/bin/python
'''
This script will make and update a noDaysOff calendar. This is a calendar app 
designed to keep you doing things day after day simply because you dont 
want to break a streak.

TO DO 
//fix weekend code. its off by a day.
fix rollover periods, ie may to may, that has two febs in it, and I need to 
check for both.
add month names
add day dates
add stats (what others?)
/longest streak counter
/build hours tracking 
'''
from PIL import Image, ImageFont, ImageDraw
import calendar
import datetime
import csv 
import os
import json
import sys

def read_prefs():
    '''
    this reads prefs from a json file named config.json in the same dir as this
    file.
    '''
    pathname = os.path.dirname(sys.argv[0])    
    with open(os.path.abspath(pathname)+'/config.json', 'r') as f:
        config = json.load(f)
    return (config['csv_path'],config['jpg_path'])

def calc_day(year,month,day):
	"""
	returns a day# from the start of the year, to look into the csv by row#
	This should probably be replaced with an actual date lookup in the csv.
	"""
	i=1
	total_days=0
	while i<month:
		total_days=total_days+months_length[i]
		i+=1
	total_days=total_days+day
	return total_days	


width=1920
height=1080
year=2018
logging_string=""
days_worked=0
hours_worked=0
current_streak=0
longest_streak=0
box_size=int((width/31.1))
fill_color="black"
weekend_work="rgb(255,0,0)"
weekend_rest="rgb(50,50,50)"
weekday_work="rgb(220,20,20)"
weekday_rest="rgb(0,0,0)"
csv_path,jpg_path=read_prefs()

#set up a blank canvas for drawing in PIL
im = Image.new('RGB', (width,height), (0 ,0,0))
dr = ImageDraw.Draw(im)
fnt2 = ImageFont.truetype("/System/Library/Fonts/STHeiti Medium.ttc",40)
fnt3 = ImageFont.truetype("/System/Library/Fonts/STHeiti Medium.ttc",30)

#read in csv file from last run
try:
	with open(csv_path, 'r') as csvfile:
		csvFileArray = []
		for row in csv.reader(csvfile, delimiter=',', quotechar='|'):
			csvFileArray.append(row)
    # mark file as found
	file_found=1
except:
	print ("no csv file found")
    # mark file as not found
	file_found=0

# set days in month based on leap year
if calendar.isleap(year):
	months_length=[0,31,29,31,30,31,30,31,31,30,31,30,31]
	print ("leap year!")
else:
	months_length=[0,31,28,31,30,31,30,31,31,30,31,30,31]
	print ("not leap year!")

# iterate through the days looking at the text file (if found) for days worked 
for month in range(1,13):
    for day in range(1,months_length[month]+1):

        string_date="{:02d} {:02d} {}".format(month,day,year)
        datetime_object = datetime.datetime.strptime(string_date, '%m %d %Y')
#        print (datetime_object)

        if not file_found:
            #this must be the first run
            #build a blank text file that will allow user to enter in their practice.
            logging_string=logging_string+(datetime_object.strftime('%m.%d.%Y')+",None,None \n")

        if file_found:
            #lookup iterated entry from the csv file.
            day_data=(csvFileArray[calc_day(year,month,day)-1]) #
            if day_data[1]!='None': # if you worked
                #detect weekend
                if datetime.datetime.weekday(datetime_object) in [5,6]: 
                    fill_color=weekend_work
                    days_worked+=1
                # no weekend    
                else: 
                    fill_color=weekday_work
                    days_worked+=1
                hours_worked+=float(day_data[1])
                current_streak+=1
            else: # you didnt work
                if datetime.datetime.weekday(datetime_object) in [5,6]: #detect weekend
                    fill_color=weekend_rest #change box color for weekend.				
                else: # no weekend
                    fill_color=weekday_rest #change box color for weekday.				
                current_streak=0

            # Draw today's box
            dr.rectangle(  (( (day-1)*box_size , (month-1)*box_size ) , (  ((day-1)*box_size)+box_size  , month*box_size  )) , fill=fill_color, outline = "white")
          
            if day_data[1]!='None':
                #write hours worked in today's box
                dr.text( ((day-1)*box_size,(month-1)*box_size),str(day_data[1]),(255,255,255,10),font=fnt3)
            if current_streak>longest_streak:
                #update strak data
               longest_streak=current_streak 
if file_found:
	#this file found loop needed so we don't write this stuff 365 times.
    dr.text( (0,12*box_size),"DAYS WORKED: "+str(days_worked),(255,255,255),font=fnt2)
    dr.text( (0,12*box_size+45),"HOURS WORKED: "+str(hours_worked),(255,255,255),font=fnt2)
    dr.text( (0,12*box_size+90),"LONGEST STREAK: "+str(longest_streak),(255,255,255),font=fnt2)
    print (os.path.dirname(sys.argv[0])+jpg_path+datetime.datetime.today().strftime('%Y-%m-%d')+".jpg")
    im.save(os.path.dirname(sys.argv[0])+datetime.datetime.today().strftime('%Y-%m-%d')+".jpg")
    im.show()

if not file_found:
    # save a new file to disk.
    with open(csv_path, "w") as text_file:
        text_file.write(logging_string)
    print ('file generated at{}'.format(csv_path))

