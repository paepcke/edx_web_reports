'''
Created on May 8, 2014

@author: paepcke
'''
import re
import unittest

from chartmaker import ChartMaker, Histogram
from htmlmin.minify import html_minify

class TestChartMaker(unittest.TestCase):
    
    REMOVE_SRC_PATTERN = re.compile(r'src=[^>]*>')

    def setUp(self):
        histogramSeries = [0,0,1,1,0,1,1,1,3,1,1,3,1,1,1,1,1,3,2,2,1,3,0,1,1,1,1,1,1,0,1,0,0,1,0,1,1,1,0,1,1,1,1]
        self.numWrong = histogramSeries.count(0)
        self.numRight = len(histogramSeries) - self.numWrong

    def testHistogram(self):
        histChart = Histogram('Testchart', 'Correctness', ['correct', 'incorrect'], [self.numRight, self.numWrong])
        html = ChartMaker.makeWebPage([histChart])
        #print(html)
        htmlNoCR = re.sub('\n','',html)
        htmlMinimized = html_minify(htmlNoCR)
        #print(htmlMinimized)
        with open('data/testHistogramGroundTruth.txt', 'r') as fd:
            groundTruth = fd.read()
        self.assertEqual(self.removeLocalPart(groundTruth.strip()), self.removeLocalPart(htmlMinimized.strip()))

    def removeLocalPart(self, aString):
        '''
        To compare ground truth to computed results, all
        string pieces that depend on the computer on which 
        the test is run need to be removed from both the
        computed string, and ground truth.
        :param aString: string from which to remove locality dependent pieces
        :type aString: String
        :return: cleaned up string
        :rtype: String
        '''
        return re.sub(TestChartMaker.REMOVE_SRC_PATTERN, '', aString)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()