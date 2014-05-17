'''
Created on May 8, 2014

@author: paepcke
'''
from collections import OrderedDict
import datetime
import re
from unittest import skipIf
import unittest

from htmlmin.minify import html_minify

from chartmaker import ChartMaker, Histogram, Pie, Line, Heatmap, DataSeries


DO_ALL = False

class TestChartMaker(unittest.TestCase):
    
    REMOVE_SRC_PATTERN = re.compile(r'src=[^>]*>')

    def setUp(self):
        histogramSeries = [0,0,1,1,0,1,1,1,3,1,1,3,1,1,1,1,1,3,2,2,1,3,0,1,1,1,1,1,1,0,1,0,0,1,0,1,1,1,0,1,1,1,1]
        self.numWrong = histogramSeries.count(0)
        self.numRight = len(histogramSeries) - self.numWrong
        
        
        self.histogramData = DataSeries([self.numRight, self.numWrong])
                             
        self.pieData  = [DataSeries([20], legendLabel='Europe'),
                         DataSeries([40], legendLabel='Asia'),
                         DataSeries([35], legendLabel='US'),
                         DataSeries([5],  legendLabel='Other'),
                         ]

        self.lineData = [DataSeries([1,3,5,7,9,11], legendLabel='CS101'),
                         DataSeries([5,9,3,1,1,7], legendLabel='CS144'),
                         DataSeries([7,5,3], legendLabel='CS140'),
                         ]
        self.xAxisLabels = ['Spring 2012', 'Fall 2012', 'Spring 2013', 'Fall 2013', 'Spring 2014', 'Summer 2014']
        
    def tearDown(self):
        # Make sure that the automatically generated chart 
        # names: chart0, chart1, ... start at 0 for each test.
        # Else the ground truth files will be wrong.
        
        ChartMaker.CHART_NAME_INDEX = 0

    @skipIf (not DO_ALL, 'comment me if do_all == False, and want to run this test')
    def testHistogram(self):
        histChart = Histogram('Testchart', 
                              'Correctness',
                              ['correct', 'incorrect'],
                              self.histogramData)
        html = ChartMaker.makeWebPage(histChart)
        #print(html)
        htmlNoCR = re.sub('\n','',html)
        htmlMinimized = html_minify(htmlNoCR)
        #print(htmlMinimized)
        with open('data/testHistogramGroundTruth.txt', 'r') as fd:
            groundTruth = fd.read()
        self.assertEqual(self.removeLocalPart(groundTruth.strip()), self.removeLocalPart(htmlMinimized.strip()))

    @skipIf (not DO_ALL, 'comment me if do_all == False, and want to run this test')
    def testPie(self):
        pieChart = Pie('Participant Origin', self.pieData)
        html = ChartMaker.makeWebPage(pieChart)
        #print(html)
        htmlNoCR = re.sub('\n','',html)
        htmlMinimized = html_minify(htmlNoCR)
        #print(htmlMinimized)
        with open('data/testPieGroundTruth.txt', 'r') as fd:
            groundTruth = fd.read()
        self.assertEqual(self.removeLocalPart(groundTruth.strip()), self.removeLocalPart(htmlMinimized.strip()))
        
    @skipIf (not DO_ALL, 'comment me if do_all == False, and want to run this test')
    def testLine(self):
        lineChart = Line('Percent Finishing to Certificate', self.xAxisLabels, 'Completion (%)', self.lineData)
        html = ChartMaker.makeWebPage(lineChart)
        #print(html)
        htmlNoCR = re.sub('\n','',html)
        htmlMinimized = html_minify(htmlNoCR)
        print(htmlMinimized)
        with open('data/testLineGroundTruth.txt', 'r') as fd:
            groundTruth = fd.read()
        self.assertEqual(self.removeLocalPart(groundTruth.strip()), self.removeLocalPart(htmlMinimized.strip()))

    #******@skipIf (not DO_ALL, 'comment me if do_all == False, and want to run this test')
    def testHeatmap(self):
        heatChart = Heatmap('Test Heatmap',
                            ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'OCt', 'Nov', 'Dec'],
                            'Time',
                            'data/testHeatmapInput.csv',
                            rowsToSkip=1,
                            xToComparableFunc=datetime.datetime,
                            yToComparableFunc=float,
                            zToComparableFunc=float
                            )
        html = ChartMaker.makeWebPage(heatChart)
        #print(html)
        with open('/home/paepcke/tmp/trash8.html', 'w') as fd:
            for line in html:
                fd.write(line)



    # --------------------------  Support Functions ------------------

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