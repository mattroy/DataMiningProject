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
        self.corpus = papers.Corpus()
        self.corpus.readCorpus("../test/test_corpus.txt")

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

    def testCosineSimilarityEmpty(self):
        self.paper1.abstract = "test sentence"

        sim = self.paper1.abstractCosineSimilarity('')
        self.assertEqual(0, sim)

    def testMaxAppend(self):
        test = [(1,3),(2,5),(3,8)]
        res = papers.appendMax((4,6), test, 3)

        self.assertEqual(res, [(1,3), (2,5), (4,6)])

    def testMaxAppendLess(self):
        test = [(1,3),(2,5),(3,8)]
        res = papers.appendMax((4,6), test, 4)

        self.assertEqual(res, [(1,3), (2,5), (4,6), (3,8)])

    def testMaxAppendMore(self):
        test = [(1,3),(2,5),(3,8)]
        res = papers.appendMax((4,6), test, 6)

        self.assertEqual(res, [(1,3), (2,5), (4,6), (3,8)])

    def testMaxAppendEnd(self):
        test = [(1,3),(2,5),(3,8)]
        res = papers.appendMax((4,9), test, 6)

        self.assertEqual(res, [(1,3), (2,5), (3,8), (4,9)])

    def testMaxAppendEmpty(self):
        test = []
        res = papers.appendMax((1,2), test, 3)

        self.assertEqual(res, [(1,2)])
        
    def testPaperCount(self):
        self.assertEqual(4, len(self.corpus.papersByRef))

    def testAuthorCount(self):
        self.assertEqual(20, len(self.corpus.indicesByAuthor))

    def testVenueCount(self):
        self.assertEqual(2, len(self.corpus.indicesByVenue))

    def testVenueNormalization(self):
        normVenue = papers.getCanonicalVenue("PLDI '00 Proceedings of the ACM SIGPLAN 2000 conference on Programming language design and implementation")
        self.assertEqual(normVenue,
            "pldi proceedings of the acm sigplan conference on programming language design and implementation")

        normVenue = papers.getCanonicalVenue("AAAI Proceedings of the 19th national conference on Artifical intelligence")
        self.assertEqual(normVenue, "aaai proceedings of the national conference on artifical intelligence")

        normVenue = papers.getCanonicalVenue("AAAI Proceedings of the  national conference on Artificial intelligence - Volume 1")
        self.assertEqual(normVenue, "aaai proceedings of the national conference on artificial intelligence")

        normVenue = papers.getCanonicalVenue("AAAI Proceedings of the eighth National conference on Artificial intelligence")
        self.assertEqual(normVenue, "aaai proceedings of the national conference on artificial intelligence")

        normVenue = papers.getCanonicalVenue("advances in fuzzy systems - special issue on fuzzy function, relations, and fuzzy transforms ()")
        self.assertEqual(normVenue, "advances in fuzzy systems")

    def testStopWords(self):
        self.assertEqual(False, self.corpus.isStopWord("computer"))
        self.assertEqual(True, self.corpus.isStopWord("the"))

    def testAbstractList(self):
        for id in self.corpus.papersByRef:
            paper = self.corpus.papersByRef[id]
            
        self.assertEqual(['fopen', 'fopen', 'angle',
'angle', 'angles', 'angles', 'appear', 'bounds', 'called', 'cases', 'circular',
'class', 'classes', 'consecutively', 'consider', 'edges', 'edges', 'find', 'finite',
 'finite', 'gse', 'general', 'general', 'graph', 'graph', 'graph', 'graphs',
 'incident', 'incident', 'incident', 'maximum', 'order', 'ps', 'paper', 'paths',
 'plane', 'plane', 'point', 'point', 'points', 'position', 'position', 'question',
  'sr2', 'sr2', 'set', 'set', 'size', 'spanning', 'spanning', 'straightline', 
  'straightline', 'study', 'tight', 'trees', 'triangulations', 'two', 'type', 
  'vertex', 'we', 'we', 'we'], paper.abstractList)

suite = unittest.TestLoader().loadTestsFromTestCase(TestPapersFunctions)
unittest.TextTestRunner(verbosity=2).run(suite)