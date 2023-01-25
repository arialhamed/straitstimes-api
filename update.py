import os, sys, time, datetime
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen


# go british (init the dataframe)
df = pd.DataFrame()

# get how much pages are there in straitstimes.com/sitemap.xml
total_sitemap_pages = len([x for x in BeautifulSoup(urlopen("https://www.straitstimes.com/sitemap.xml"),'lxml').get_text().split('\n') if "page=" in x])

#full_raw_name = f"{os.getcwd()}/straitstimes_sitemap.xml_full-raw.csv"
full_raw_name = "../tfjs-aap/assets/stnews.csv"

if not(os.path.isfile(full_raw_name)):
	for i in range(total_sitemap_pages):
		# assert i == 0 # for debugging
		url = "https://www.straitstimes.com/sitemap.xml?page="+str(i+1)
		html = urlopen(url)

		# note that using 'lxml' may not be available if you're running this
		# notebook on a local runtime, which i would not recommend imo, as
		# there could be a chance that straitstimes would time you out
		soup = BeautifulSoup(html, 'lxml') 
		soup_as_text = soup.get_text()
		soup_url = [x for x in soup_as_text.split("\n") if "https://" in x]
		soup_datetime = [x for x in soup_as_text.split("\n") if "+08:00" in x]

		# first row in first page does not have datetime, hence remove url
		# (which is just straitstimes.com)
		if i == 0:
			soup_url.remove(soup_url[0])
			# in the first page, soup_datetime has the length of 4999, so soup_url will add up with soup_datetime

		# appending to df
		df = pd.concat([df, pd.DataFrame(
			{"url": soup_url, "datetime": soup_datetime}
		)], ignore_index=True)

		# pretty printing
		if i == total_sitemap_pages - 1:
			sys.stdout.write("\rSaved all %i pages!" % (i+1))
		else:
			sys.stdout.write("\rSaving page %i" % (i+1))
		sys.stdout.flush()

	# backup to runtime if error in notebook occurs
	df.to_csv(full_raw_name)
else:
	df = pd.read_csv(full_raw_name)
	print("Already got the data, proceeding..")

print()
#months = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
#ctime = time.ctime(os.path.getctime(full_raw_name)).split()
#ifile = full_raw_name[22:] if full_raw_name[20:22] == "]_" else full_raw_name
#os.system(f'mv \"{full_raw_name}\"  \"[{ctime[4]}-{months[ctime[1]]}-{ctime[2].zfill(2)}_{ctime[3].replace(":","-")}]_{ifile}\"')

os.system("notify-send \"straitstimes.com/sitemap.xml scraping is complete\" \"update.py found in `pwd`\"")
#os.system("bash repospec.sh")
os.system("git pull && git add . && git commit -m {time.time()} && git push")
