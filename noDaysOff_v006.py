#!/usr/bin/python
'''
This script will make and update a nodaysoff calendar. This is a calendar app designed to keep you doing things
day after day simply because you dont want to break a streak.

TO DO 
fix weekend code. its off by a day.
fix rollover periods, ie may to may, that has two febs in it, and I need to check for both.
add month names
add day dates
add stats
longest streak counter
build hours tracking 
'''
from PIL import Image, ImageFont, ImageDraw
import calendar
import datetime
import csv 

width=1920
height=1080
year=2018
logging_string=""
days_worked=0
box_size=int((width/31.1))
fill_color="black"
weekend_work="rgb(255,0,0)"
weekend_rest="rgb(50,50,50)"
weekday_work="rgb(220,20,20)"
weekday_rest="rgb(0,0,0)"

def calc_day(year,month,day):
	i=1
	d=1
	total_days=0
	while i<month:
		total_days=total_days+months_length[i]
		i+=1
	total_days=total_days+day
	return total_days	

#set up a blank canvas for drawing
im = Image.new('RGB', (width,height), (0 ,0,0))
dr = ImageDraw.Draw(im)

#read in csv file from last run
try:
	with open("path/to/txt_file.txt", 'r') as csvfile:
		csvFileArray = []
		for row in csv.reader(csvfile, delimiter=',', quotechar='|'):
			csvFileArray.append(row)

	file_found=1
except:
	print ("no csv file found")
	file_found=0

# set days in month based on leap year
if calendar.isleap(year):
	months_length=[0,31,29,31,30,31,30,31,31,30,31,30,31]
	print ("leap year!")
else:
	months_length=[0,31,28,31,30,31,30,31,31,30,31,30,31]
	print ("not leap year!")

# iterate through the days of the year looking at the text file (if found) for days worked 
for month in range(1,13):
	for day in range(1,months_length[month]+1):
		string_date="{:02d} {:02d} {}".format(month,day,year)
		datetime_object = datetime.datetime.strptime(string_date, '%m %d %Y')
		day_data=(csvFileArray[calc_day(year,month,day)-1])

		#the line below is building a blank text file that will allow you to enter in your practice if this is the first run
		logging_string=logging_string+(datetime_object.strftime('%m.%d.%Y')+",None,None \n")
		
		if day_data[1]!='None': # if you worked
			if datetime.datetime.weekday(datetime_object) in [0,6]: #detect weekend
				fill_color=weekend_work
			else: # no work
				fill_color=weekday_work
			days_worked+=1

		else: # you didnt work
			if datetime.datetime.weekday(datetime_object) in [0,6]: #detect weekend
				fill_color=weekend_rest #change box color for weekend.				
			else: # no work
				fill_color=weekday_rest #change box color for weekday.				
		# Draw the box
		dr.rectangle(  (( (day-1)*box_size , (month-1)*box_size ) , (  ((day-1)*box_size)+box_size  , month*box_size  )) , fill=fill_color, outline = "white")

fnt2 = ImageFont.truetype("/System/Library/Fonts/STHeiti Medium.ttc",40)
dr.text( (0,12*box_size),"DAYS WORKED: "+str(days_worked),(255,255,255),font=fnt2)

im.save("path/to/test4.jpg")
im.show()

# save a new file if one was not found.
if file_found==0:
	with open("path/to/txt_file.txt", "w") as text_file:
		text_file.write(logging_string)

