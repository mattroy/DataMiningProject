#papers.py
#
#This class contains classes for dealing with the papers in the data.
#
#Data Mining Project
#CS6220 Fall 2014
#Team ELSAMAT

import math
import string
import re

def getCanonicalVenue(phrase):
	"""
	Remove abrievated years from a string.
	"""
	phrase = phrase.lower().strip()

	phrase = re.sub("'\d\d", "", phrase)
	phrase = re.sub("\d\d\d\d", "", phrase)
	phrase = re.sub("\d\d(st|nd|th|rd)", "", phrase)
	phrase = re.sub("(first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth|eleventh|thirteenth)", "", phrase)
	phrase = re.sub("\d(st|nd|th)", "",phrase)
	phrase = re.sub("( - volume \d| - volume \d\d)", "", phrase)
	phrase = re.sub("-\d\d", "", phrase)
	phrase = re.sub("-.+$", "", phrase)
	phrase = re.sub("(\d$|\d\d$)", "", phrase)
	phrase = re.sub("\s+", " ", phrase)

	return phrase.strip()

def splitWords(words):
	"""
	Split a string into a sorted, normalized list, with punctuation removed.
	"""

	exclude = set(string.punctuation)

	sortedWords = [x.strip().lower() for x in words.split()]
	sortedWords.sort()
	sortedWords = map(lambda x: ''.join(ch for ch in x if ch not in exclude), sortedWords)

	return sortedWords

def appendMax(newItem, refList, maxNum):
	"""
	Add a new item to a list in refList never exceeding the maximum. Item should be a 
	2-tuple, with the second element being the score.
	"""
	if len(refList) == 0:
		return [newItem]
	for i in range(0,len(refList)):
		if refList[i][1] > newItem[1]:
			refList.insert(i, newItem)
			break
		if i == len(refList) -1:
			refList.insert(i + 1, newItem)

	return refList[0:maxNum]

class Paper:
	"""
	Papers with fields for all attributes of the paper.
	"""

	def __init__(self, index=''):
		self.authors = []
		self.references = []
		self.index = index
		self.abstract = ''
		self.title = ''
		self.year = 0
		self.venue = ''
		self.canonicalVenue = ''
		self.titleList = []
		self.abstractList = []

	def buildVectors(self, firstList, secondList):
		"""
		Computes the TF-IDF vectors of the two lists.
		"""
	
		sortedAb1 = sorted(firstList) #splitWords(self.abstract)
		sortedAb2 = sorted(secondList) #splitWords(secondAbstract)

		#vec1 and vec2 will contain 1 for an existing word, or 0 for non existing word
		vec1 = []
		vec2 = []
		i = 0
		j = 0

		while i < len(sortedAb1) and j < len(sortedAb2):			
			if sortedAb1[i] == sortedAb2[j]:
				vec1.append(1)
				vec2.append(1)
				i += 1
				j += 1

			elif sortedAb1[i] < sortedAb2[j]:
				vec1.append(1)
				vec2.append(0)
				i += 1

			elif sortedAb1[i] > sortedAb2[j]:
				vec1.append(0)
				vec2.append(1)
				j += 1

		# One of the lists is longer, vectors must be made the same length
		if i < len(sortedAb1):
			while i < len(sortedAb1):
				vec1.append(1)
				vec2.append(0)
				i += 1

		if j < len(sortedAb2):
			while j < len(sortedAb2):
				vec1.append(0)
				vec2.append(1)
				j += 1

		return (vec1, vec2)
		
	def titleCosineSimilarity(self, secondTitleList):
		"""
		Compute the similarity between the titles of two papers.
		"""
		
		return self.cosineSimilarity(self.titleList, secondTitleList)

	def abstractCosineSimilarity(self, secondAbstractList): 
		"""
		Compute the cosine similarity between the abstract of this paper 
		and the given string.
		"""

		return self.cosineSimilarity(self.abstractList, secondAbstractList)
		

	def authorsCosineSimilarity(self, secondAuthorsList):
		"""
		Compute the cosine similarity between the authors of this paper
		and the given string.
		"""

		return self.cosineSimilarity(self.authors, secondAuthorsList)

	def cosineSimilarity(self, list1, list2):
		"""
		Compute the cosine similarity between two lists of words.
		"""
		
		vec1, vec2 = self.buildVectors(list1, list2)
		
		if len(vec1) == 0 or len(vec2) == 0:
			return 0

		if sum(vec1) == 0 or sum(vec2) == 0:
			return 0

		sumxx = 0
		sumyy = 0
		sumxy = 0

		for i in range(0,len(vec1)):
			x = vec1[i]
			y = vec2[i]

			sumxx += x*x
			sumyy += y*y
			sumxy += x*y

		return sumxy / math.sqrt(sumxx * sumyy)

class Corpus:
	"""
	Holds a collection of papers with ability to query by fields.
	"""

	def __init__(self, normalizeVenues=True):
		self.papersByRef = {}
		self.indicesByAuthor = {}
		self.indicesByVenue = {}
		self.indicesByCanonicalVenue = {}
		self.normalizeVenues = normalizeVenues
		self.smallSet = {}
		self.stopWords = {}
		self.loadStopWords()
		self.venueReferences = {}
		self.venueReferenceCount = {}
		self.paperReferenceCount = {}

	def computeAllVenueReferences(self):
		"""
		Builds a dictionary of dictionarys where each key is a canonicalVenue and the sub-dictionary
		contains all canonicalVenues listed as references by papers from the first venue.
		"""
		self.venueReferences = {}
		for paperId in self.papersByRef:
			currentPaper = self.papersByRef[paperId]

			if currentPaper.canonicalVenue not in self.venueReferences:
				self.venueReferences[currentPaper.canonicalVenue] = {}
				self.venueReferenceCount[currentPaper.canonicalVenue] = 0

			for ref in currentPaper.references:

				if ref in self.paperReferenceCount:
					self.paperReferenceCount[ref] += 1
				else:
					self.paperReferenceCount[ref] = 1

				if ref in self.papersByRef:
					refPaper = self.papersByRef[ref]
					self.venueReferenceCount[currentPaper.canonicalVenue] += 1
					if refPaper.canonicalVenue in self.venueReferences[currentPaper.canonicalVenue]:
						self.venueReferences[currentPaper.canonicalVenue][refPaper.canonicalVenue] += 1
					else:
						self.venueReferences[currentPaper.canonicalVenue][refPaper.canonicalVenue] = 1

	def loadStopWords(self):
		"""
		Initialize the stop word list from a file. Each stopword should be on a separate line.
		"""
		with open("./scripts/stop_words.txt", "r") as file:
			for line in file:
				self.stopWords[line.strip().lower()] = 1

	def isStopWord(self, word):
		"""
		True if the given word is a stop word.
		"""
		return word in self.stopWords

	def readCorpus(self, location):
		"""
		Load the corpus from a file.
		"""
		with open(location, "r") as file:
			for line in file:

				#paper id
				if line.startswith("#index"):
					index = line[7:].strip()
					paper = Paper(index)
					self.papersByRef[index] = paper
				
				#title
				elif line.startswith('#*'):
					paper.title = line[3:].strip()
					for word in paper.title.split():
						if not self.isStopWord(word.strip().lower()):
							paper.titleList.append(word.strip().lower())

				#authors
				elif line.startswith("#@"):
					authors = [x.strip() for x in line[3:].split(";")]
					paper.authors = authors
					for author in authors:
						if author in self.indicesByAuthor:
							self.indicesByAuthor[author].append(paper.index)
						else:
							self.indicesByAuthor[author] = [paper.index]

				#year
				elif line.startswith("#t"):
					if line[3:].strip() != '':
						paper.year = int(line[3:].strip())
					else:
						paper.year = 0

				#venue
				elif line.startswith("#c"):
					paper.venue = line[3:].strip()

					if paper.venue in self.indicesByVenue:
						self.indicesByVenue[paper.venue].append(paper.index)
					else:
						self.indicesByVenue[paper.venue] = [paper.index]

					paper.canonicalVenue = getCanonicalVenue(paper.venue)

					if paper.canonicalVenue in self.indicesByCanonicalVenue:
						self.indicesByCanonicalVenue[paper.canonicalVenue].append(paper.index)
					else:
						self.indicesByCanonicalVenue[paper.canonicalVenue] = [paper.index]

				#references
				elif line.startswith("#%"):
					paper.references.append(line[3:].strip())

				#abstract
				elif line.startswith("#!"):
					paper.abstract = line[3:].strip()
					for word in splitWords(paper.abstract):
						if not self.isStopWord(word):
							paper.abstractList.append(word)
		self.computeAllVenueReferences()
