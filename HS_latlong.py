# Scrape high school lats/longs from Wikipedia

# Edit to your exported Wufoo form CSV
CSVDATA = "../blueprint.csv"
# JSON output file
OUTPUTFILE = "highschools.js"

# Vars
totalrows = 0
errorcount = 0
highschools = []
highschool_locations = {}
highschool_count = {}
# areacodes = []
# fancy_words = ["best", "excellence", "specialized", "magnet", "premier", "recognition", "top-performing"]

# Depedencies
import csv, re, wikipedia, bs4


# Get list of high schools, with sanitization
with open(CSVDATA, 'rb') as csvfile:
		registrationreader = csv.reader(csvfile, delimiter=",", quotechar='"')
		for row in registrationreader:
				totalrows = totalrows + 1
				highschoolname = row[5]

				# make sure it's not homeschool
				homeschool = re.findall(r'[.]*(homeschool|Home school|Home School|Homeschool)[.]*', highschoolname)
				if homeschool:
					continue

				if highschoolname not in highschools:
					highschool_count[highschoolname] = 1
					
					school = re.findall(r'[.]*(school|School|Highschool|Academy|College|Institute)[.]*', highschoolname)
					if school:
						highschools.append(row[5])
					else:
						highschools.append('"' + row[5][1:-1] + ' School"')

				else:
					highschool_count[highschoolname] = highschool_count.get(highschoolname) + 1
				# areacode = re.sub("[^0-9]", "", row[4])
				# if areacode[:1] == "1":
				# 	areacode = areacode[1:4]
				# else:
				# 	areacode = areacode[0:3]
				# areacodes.append(areacode)


# Scrape high school info off Wikipedia
for highschool in highschools[2:]:
	try:
		wikisearch = wikipedia.search(highschool)
		wikipage = wikipedia.page(wikisearch[0]).html()
	except:
		continue
	try:
		latitude = re.findall(r'[3-5][0-9]\.[0-9]{3,10}', wikipage)
		longitude = re.findall(r'[7-9,1][0-9]{1,2}\.[0-9]{3,10}', wikipage)
		try:
			highschool_locations[highschool] = latitude[0] + ",-" + longitude[0]
			print(highschool + " // " + latitude[0] + ", " + longitude[1])
		except:
			errorcount = errorcount + 1
			print("Uh oh, no lat or long found for " + highschool + ". Continuing...")
			continue
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
				errorcount = errorcount + 1
				print("Couldn't find " + highschool + " on Wikipedia.")


# Print formatted json for Goog Maps

# highschools['High School Name'] = {
# center: new google.maps.LatLng(LATITUDE, LONGITUDE),
# count: COUNT	
# };

print("Scraping finished. Writing file...")

outputfile = open(OUTPUTFILE, 'w')

outputfile.write("var highschools = {};\n\n")

for highschool, count in highschool_count.items():
	if highschool_locations.get(highschool):
		outputfile.write("highschools['" + str(highschool.replace("'", "")) + "'] = { center: new google.maps.LatLng(" + str(highschool_locations.get(highschool)) + "), count: " + str(count) + " };\n")

outputfile.close()

print("\nDone!")
print("Total registrants = " + totalrows)
print("Total errors = " + errorcount)
# print("\n\n\n=================\nHigh school locations: \n\n")
# print highschool_locations