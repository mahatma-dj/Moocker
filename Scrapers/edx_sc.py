# coding=utf8

from bs4 import BeautifulSoup
import urllib
import re
import math
import json

# **************************
# Scrape edX courses
# **************************

# make the basic soup
url = 'https://www.edx.org/course-list/allschools/allsubjects/allcourses'
htmlfile = urllib.urlopen(url)
htmltext = htmlfile.read()
soup = BeautifulSoup(htmltext)

# Get the number of pages, which
# is the total number of courses / 15 and rounded up
navs = soup.find_all('nav')
counter_div = navs[1].find('div','counter')
num_courses = float(soup.find('nav', 'courses-header clearfix').input['value'])
num_pages = math.ceil(num_courses/15)

# Now to scrape the courses. The following loops create a list of dictionaries, containing the details of each course.
# Still need to convert the date into a workable format.

course_list = {}
for p in range(int(num_pages)):
	if p != 0:
		url = 'https://www.edx.org/course-list/allschools/allsubjects/allcourses' + '?page=' + str(p)
		htmlfile = urllib.urlopen(url)
		htmltext = htmlfile.read()
		soup = BeautifulSoup(htmltext)
		courses = soup.find_all('article')
		for c in range(len(courses)):
			course = {}
			course['subtitle'] = courses[c].find('div', 'subtitle').get_text()
			course['date'] = courses[c].find('div', 'detail').find('li').contents[1].strip()
			course['uni'] = courses[c].find('li', 'school-list').get_text()
			course['link'] = 'http://www.edx.org'+courses[c].find('div', 'course-link')['href']
			course_list[courses[c].find('h1').get_text()] = course # creates a key:value pair in dictionary course_list, the key of which is the title of the course and the value of which is a dictionary with all the other data about the course
	else:
		courses = soup.find_all('article')
		for c in range(len(courses)):
			course = {}
			course['subtitle'] = courses[c].find('div', 'subtitle').get_text()
			course['date'] = courses[c].find('div', 'detail').find('li').contents[1]
			course['uni'] = courses[c].find('li', 'school-list').get_text()
			course['link'] = 'http://www.edx.org'+courses[c].find('div', 'course-link')['href']
			course_list[courses[c].find('h1').get_text()] = course # see comment above

# Next, I need to convert course_list (a list of dicts) into a proper file format - JSON i think! I've done it as follows:

with open('edx.json', mode='w') as f:
	json.dump(course_list, f, indent=2)





