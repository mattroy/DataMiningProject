#papers.py
#
#This class contains classes for dealing with the papers in the data.
#
#Data Mining Project
#CS6220 Fall 2014
#Team ELSAMAT

import math
import string

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
		self.year = ''
		self.venue = ''

	def abstractVectors(self, secondAbstract):
		"""
		Computes the TF-IDF vectors of the abstract of this paper and a given
		 string.
		"""
	
		sortedAb1 = splitWords(self.abstract)
		sortedAb2 = splitWords(secondAbstract)

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

	def abstractCosineSimilarity(self, secondAbstract): 
		"""
		Compute the cosine similarity between the abstract of this paper 
		and the given string.
		"""

		vec1, vec2 = self.abstractVectors(secondAbstract)

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

	def __init__(self):
		self.papersByRef = {}
		self.indicesByAuthor = {}
		self.indicesByVenue = {}


	def readCorpus(self, location):
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
					paper.year = line[3:].strip()

				#venue
				elif line.startswith("#c"):
					paper.venue = line[3:].strip()
					if paper.venue in self.indicesByVenue:
						self.indicesByVenue[paper.venue].append(paper.index)
					else:
						self.indicesByVenue[paper.venue] = [paper.index]

				#references
				elif line.startswith("#%"):
					paper.references.append(line[3:].strip())

				#abstract
				elif line.startswith("#!"):
					paper.abstract = line[3:].strip()
