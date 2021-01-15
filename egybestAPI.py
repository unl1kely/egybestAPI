from bs4 import BeautifulSoup as bs
from JskPy import encodeUrl, best_match
from requests import get
domainEgyBest = "https://egybest.online"
dataUrlScript = "https://cdn-static.egybest.net/packed/G78uOQIvP42dDsB.js"
egyResponse = str(get(domainEgyBest))
if "200" not in egyResponse:
	print(f"[!] - Couldn't reach {domainEgyBest}")
	input("Press Enter to exit...")
	exit()

class Serie:
	def __init__(self, title):
		self.title = title
		self.search_url = f"{domainEgyBest}/explore/?q={encodeUrl(self.title)}"
		self.search_page = get(self.search_url).text
		self.search_soup = bs(self.search_page, "html.parser")
		self.result_div = self.search_soup.find(id="movies")
		if self.result_div==None:
			self.found = 0
			self.message = f"Incorrect input : {self.title}"
		else:
			self.result_list = self.result_div.find_all("a")
			if len(self.result_list)==0:
				self.found = 0
				self.message = f"{self.title} - Serie not found."
			else:
				self.title_link = False
				self.series = [ ]
				for a_tag in self.result_list:
					if "/series/" in a_tag.get("href"):
						# is serie
						self.series.append(a_tag)
				######################################
				if not self.series:
					self.found = 0
					self.message = f'Nothing found by "{self.title}".'
				else:
					self.titles = [a_tag.find(class_="title").text for a_tag in self.series]
					self.result_index = best_match(self.title, self.titles)
					if not self.result_index in range(len(self.titles)):
						self.found = 0
						self.message = f"{self.title} - Serie not found."
					else:
						self.name = self.titles[self.result_index]
						self.title_link = self.series[self.result_index].get("href")
						self.title_page = get(self.title_link).text
						self.title_soup = bs(self.title_page, "html.parser")
						self.lastEpLink = self.title_soup.find_all(class_="movies_small")[1].find("a").get("href") ##############
						self.end_index = self.lastEpLink.index("-season-")
						self.start_index = self.lastEpLink.index("episode/") + 8 # len("episode/") = 8
						self.show_id = self.lastEpLink[self.start_index:self.end_index]
						self.found = 1
						self.message = "Found serie : "+self.name
				###################################
				'''
				for a_tag in self.series:
					if self.title.casefold().replace(" ", "") in a_tag.find(class_="title").text.casefold().replace(" ", ""):
						# desired serie
						self.title_link = a_tag.get("href")
						self.name = a_tag.find(class_="title").text
						break
				if not self.title_link:
					self.found = 0
					self.message = f"{self.title} - Serie not found.")
				else:
					self.title_page = get(self.title_link).text
					self.title_soup = bs(self.title_page, "html.parser")
					#<serie>
					self.lastEpLink = self.title_soup.find_all(class_="movies_small")[1].find("a").get("href") ##############
					self.end_index = self.lastEpLink.index("-season-")
					self.start_index = self.lastEpLink.index("episode/") + 8 # len("episode/") = 8
					self.show_id = self.lastEpLink[self.start_index:self.end_index]
					#</serie>
					self.found = 1
					self.message = "Found serie : "+self.name)'''
	@staticmethod
	def define(title):
		global current_
		current_ = Serie(title)
	def watch(self, season, episode, quality="Auto"):
		self.season = season
		self.episode = episode
		self.page_link = "{0}/episode/{1}-season-{2}-ep-{3}".format(domainEgyBest, self.show_id, self.season, self.episode)
		self.page_soup = bs(get(self.page_link).text, "html.parser")
		self.watch_quality = quality
		if self.watch_quality=="Auto": #iframe
			self.watch_link = domainEgyBest + self.page_soup.find("iframe").get("src")
		else:
			self.tbody = self.page_soup.find(class_="dls_table")
			self.watch_links = self.tbody.find_all(class_="nop btn b dl _open_window")
			if len(self.watch_links)==4:
				if self.watch_quality=="240p":
					print("[!] - 240p not available for this episode. Using 360p instead...")
					self.watch_quality = "360p"
			self.vidstream_link = domainEgyBest + self.watch_links[qualities_dict[self.watch_quality]].get("data-url")
			print(self.vidstream_link,3*"\n")
			self.vidstream_page = bs(get(self.vidstream_link).text, "html.parser")
			self.vidstream_source = self.vidstream_page.find("source")
			self.watch_link = self.vidstream_source.get("src")
			print("self vidstream source",self.vidstream_source)
		if __name__ != '__main__':
			self.message = f"{self.name} S{self.season}E{self.episode} link copied to clipboard"
		else:
			self.message = self.watch_link
		return self.message
	def download(self, season, episode, quality="720p"):
		return 0
		self.season = season
		self.episode = episode
		self.page_link = "{0}/episode/{1}-season-{2}-ep-{3}".format(domainEgyBest, self.show_id, self.season, self.episode)
		self.page_soup = bs(get(self.page_link).text, "html.parser")
		self.download_quality = quality
		if self.download_quality=="Auto":
			self.download_quality = "720p"
		self.tbody = self.page_soup.find(class_="dls_table")
		self.download_links = self.tbody.find_all(class_="nop btn g dl _open_window")
		if len(self.download_links)==4:
			if self.download_quality=="240p":
				print("[!] - 240p not available for this episode. Using 360p instead...")
				self.download_quality = "360p"
		self.vidstream_link = domainEgyBest + self.download_links[qualities_dict[self.download_quality]].get("data-url")
		#print(self.vidstream_link,3*"\n")
		self.vidstream_page = bs(get(self.vidstream_link).text, "html.parser")
		self.vidstream_bigbuttons = self.vidstream_page.find("p").find_all(class_="bigbutton")
		#print(self.vidstream_bigbuttons)
		self.download_link = self.vidstream_bigbuttons[0].get("href")
		#print(self.vidstream_link)
		if __name__ != '__main__':
			self.message = f"{self.name} S{self.season}E{self.episode} download link copied to clipboard"
		else:
			self.message = self.download_link
		return self.message
# download:g0;watch:b1

class Film:
	def __init__(self, title):
		# ==============================
		self.title = title
		self.search_url = f"{domainEgyBest}/explore/?q={self.title.replace(' ', '%20')}"
		self.search_page = get(self.search_url).text
		self.search_soup = bs(self.search_page, "html.parser")
		self.result_div = self.search_soup.find(id="movies")
		if self.result_div==None:
			self.found = 0
			self.message = f"Incorrect input : {self.title}"
		else:
			self.result_list = self.result_div.find_all("a")
			if len(self.result_list)==0:
				self.found = 0
				self.message = f"{self.title} - Film not found."
			else:
				self.title_link = False
				self.films = [ ]
				for a_tag in self.result_list:
					if "/movie/" in a_tag.get("href"): # is film
						self.films.append(a_tag)
				if not self.films:
					self.found = 0
					self.message = f'Nothing found by "{self.title}".'
				else:
					self.titles = [a_tag.find(class_="title").text for a_tag in self.films]
					self.result_index = best_match(self.title, self.titles)
					if not self.result_index in range(len(self.titles)):
						self.found = 0
						self.message = f"{self.title} - Film not found."
					else:
						self.name = self.titles[self.result_index]
						self.title_link = self.films[self.result_index].get("href")
						self.title_page = get(self.title_link).text
						self.title_soup = bs(self.title_page, "html.parser")
						self.found = 1
						self.message = "Found film : "+self.name
	@staticmethod
	def define(title):
		global current_
		current_ = Film(title)
	def watch(self, quality="Auto"):
		self.watch_quality = quality
		if self.watch_quality=="Auto": #iframe
			self.watch_link = domainEgyBest + self.title_soup.find("iframe").get("src")
		else:
			self.tbody = self.title_soup.find(class_="dls_table")
			self.watch_links = self.tbody.find_all(class_="nop btn b dl _open_window")
			if len(self.watch_links)==4:
				if self.watch_quality=="240p":
					print("[!] - 240p not available for this episode. Using 360p instead...")
					self.watch_quality = "360p"
			self.vidstream_link = domainEgyBest + self.watch_links[qualities_dict[self.watch_quality]].get("data-url")
			#print(self.vidstream_link,3*"\n")
			self.vidstream_page = bs(get(self.vidstream_link).text, "html.parser")
			self.vidstream_source = self.vidstream_page.find("source")
			self.watch_link = self.vidstream_source.get("src")
			#print("self vidstream source",self.vidstream_source)
		if __name__ != '__main__':
			self.message = f"{self.name} video link copied to clipboard"
		else:
			self.message = self.watch_link
		return self.message
	def download(self, quality="720p"):
		return 0
		# currently working on this
		self.download_quality = quality
		if self.download_quality=="Auto":
			self.download_quality = "720p"
		self.tbody = self.title_soup.find(class_="dls_table")
		self.download_links = self.tbody.find_all(class_="nop btn g dl _open_window")
		if len(self.download_links)==4:
			if self.download_quality=="240p":
				print("[!] - 240p not available for this episode. Using 360p instead...")
				self.download_quality = "360p"
		self.vidstream_link = domainEgyBest + self.download_links[qualities_dict[self.download_quality]].get("data-url")
		#print(self.vidstream_link,3*"\n")
		self.vidstream_page = bs(get(self.vidstream_link).text, "html.parser")
		self.vidstream_bigbuttons = self.vidstream_page.find("p").find_all(class_="bigbutton")
		#print(self.vidstream_bigbuttons)
		self.download_link = self.vidstream_bigbuttons[0].get("href")
		#print(self.vidstream_link)
		if __name__ != '__main__':
			self.message = f"{self.name} ({self.download_quality}) download link copied to clipboard"
		else:
			self.message = self.download_link
		return self.message