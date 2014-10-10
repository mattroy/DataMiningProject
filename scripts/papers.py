#papers.py
#
#This class contains classes for dealing with the papers in the data.
#
#Data Mining Project
#CS6220 Fall 2014
#Team ELSAMAT

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


class Corpus:
	"""
	Holds a collection of papers with ability to query by fields.
	"""

	def __init__(self):
		self.papersByRef = {}
		self.indicesByAuthor = {}


	def readCorpus(self, location):
		with open(location, "r") as file:
			for line in file:
				if line.startswith("#index"):
					index = line[7:].strip()
					paper = Paper(index)
					self.papersByRef[index] = paper
				
				elif line.startswith('#*'):
					paper.title = line[3:].strip()

				elif line.startswith("#@"):
					authors = [x.strip() for x in line[3:].split(";")]
					paper.authors = authors
					for author in authors:
						if author in self.indicesByAuthor:
							self.indicesByAuthor[author].append(paper.index)
						else:
							self.indicesByAuthor[author] = [paper.index]

				elif line.startswith("#t"):
					paper.year = line[3:].strip()

				elif line.startswith("#c"):
					paper.venue = line[3:].strip()

				elif line.startswith("#%"):
					paper.references.append(line[3:].strip())

				elif line.startswith("#!"):
					paper.abstract = line[3:].strip()
