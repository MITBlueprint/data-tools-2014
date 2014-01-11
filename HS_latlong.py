# -*- coding: utf-8 -*-
# search for high school locations on Google

highschools = []
highschool_locations = {}
areacodes = []
fancy_words = ["best", "excellence", "specialized", "magnet", "premier", "recognition", "top-performing"]

import csv, re, wikipedia, bs4

# gather a list of high schools from Wufoo CSV form data
with open('blueprint.csv', 'rb') as csvfile:
		registrationreader = csv.reader(csvfile, delimiter=",", quotechar="|")
		for row in registrationreader:
				highschoolname = row[5]
				if highschoolname not in highschools:
					if re.match(r' (school|SCHOOL|School)[ ]?$', highschoolname):
						highschools.append(row[5])
					else:
						highschools.append('"' + row[5][1:-1] + ' School"')
				# areacode = re.sub("[^0-9]", "", row[4])
				# if areacode[:1] == "1":
				# 	areacode = areacode[1:4]
				# else:
				# 	areacode = areacode[0:3]
				# areacodes.append(areacode)

# scrape high school info off Wikipedia:
# 1. location
# 2. "excellence" level -- let's see how many times it says "best" or "excellence" vs "growing" and "improvement"

for highschool in highschools[10:11]:
	try:
		print highschool
		wikisearch = wikipedia.search(highschool)
		print wikisearch
		wikipage = wikipedia.page(wikisearch[0]).html()
	except:
		continue
	try:
		latlong = re.findall(r'[0-9]{2}\.[0-9]{3,10}', wikipage)
		highschool_locations[highschool] = latlong[0] + "N," + latlong[1] + "W"
		print(highschool + " // " + latlong[0] + ", " + latlong[1])
	except AttributeError:
		try:			
			zipcode = re.findall(r' [0-9]{5}', wikiparse.prettify())[0][1:]
			highschool_locations[highschool] = zipcode
			print(highschool + " // " + zipcode)
		except:
			try:
				wikiparse = bs4.BeautifulSoup(wikipage)
				locality = wikiparse.find('span', attrs={'class': 'locality'}).text
				region = wikiparse.find('span', attrs={'class': 'region'}).text
				highschool_locations[highschool] = locality + " " + region
				print(highschool + " // " + locality + " " + region)
			except:
				print("Couldn't find " + highschool + " on Wikipedia.")

print("\n\n\n=================\nHigh school locations: \n\n")
print highschool_locations