'''
Created on May 8, 2014

@author: paepcke
'''
import json
import unittest

from chartmaker import HistogramMaker


class TestChartMaker(unittest.TestCase):

    def setUp(self):
        histogramSeries = [0,0,1,1,0,1,1,1,3,1,1,3,1,1,1,1,1,3,2,2,1,3,0,1,1,1,1,1,1,0,1,0,0,1,0,1,1,1,0,1,1,1,1]
        self.numWrong = histogramSeries.count(0)
        self.numRight = len(histogramSeries) - self.numWrong

    def testHistogram(self):
        histMaker = HistogramMaker(['correct', 'incorrect'], [self.numWrong, self.numRight], 'Testchart')
        html = histMaker.getHTML()
        print(html)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()