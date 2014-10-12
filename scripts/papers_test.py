#papers_test.py
#
#Test for players classes.
#
#Data Mining Project
#CS6220 Fall 2014
#Team ELSAMAT

import unittest
import papers

class TestPapersFunctions(unittest.TestCase):

    def setUp(self):
        self.paper1 = papers.Paper()
        self.paper2 = papers.Paper()

    def testVector(self):
        self.paper1.abstract = "The first test sentence"
        self.paper2.abstract = "The second test sentence"

        vector1, vector2 = self.paper1.abstractVectors(self.paper2.abstract)

        self.assertEqual(vector1,[1,0,1,1,1])
        self.assertEqual(vector2, [0,1,1,1,1])

    def testVectorDifferentLength(self):
        self.paper1.abstract = "A"
        self.paper2.abstract = "A second test sentence"

        vector1, vector2 = self.paper1.abstractVectors(self.paper2.abstract)

        self.assertEqual(vector1, [1,0,0,0])
        self.assertEqual(vector2, [1,1,1,1])

    def testCosineSimilarity(self):
        self.paper1.abstract = "The test sentence"
        self.paper2.abstract = "The test sentence"

        sim = self.paper1.abstractCosineSimilarity(self.paper2.abstract)

        self.assertEqual(1, sim)

    def testCosineSimilarityDiff(self):
        self.paper1.abstract = "Different sentence"
        self.paper2.abstract = "other words"

        sim = self.paper1.abstractCosineSimilarity(self.paper2.abstract)

        self.assertEqual(0, sim)

    def testCosineSimilarityPunctuation(self):
        self.paper1.abstract = "A sentence. with some, punctuation."
        self.paper2.abstract = "with, some sentence a. punctuation"

        sim = self.paper1.abstractCosineSimilarity(self.paper2.abstract)

        self.assertEqual(1, sim)


suite = unittest.TestLoader().loadTestsFromTestCase(TestPapersFunctions)
unittest.TextTestRunner(verbosity=2).run(suite)