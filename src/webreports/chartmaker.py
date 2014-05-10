'''
Created on May 8, 2014

@author: paepcke
'''
import os


class ChartTypes:
    COLUMN = 'column'
    BAR    = 'bar'
    PIE    = 'pie'

class DataCategory:
    CATEGORICAL = 0
    CONTINUOUS  = 1

class ChartMaker(object):
    '''
    classdocs
    '''

    JS_HEADER = "<!DOCTYPE HTML>\n" +\
                "<html>\n" +\
    			" <head>\n" +\
    			'     <meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n' +\
    			"     <title>OpenEdx Chart</title>\n" +\
			    "\n" +\
    			'     <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js"></script>\n' +\
    			'     <script type="text/javascript">\n' +\
                " $(function () {\n" +\
                "     $('#container').highcharts({\n"

    CURR_DIR  = os.path.dirname(__file__)

    HTML_FOOTER = ");});" +\
				  "      </script>" +\
				  "   </head>" +\
				  "   <body>" +\
				  '<script src="%s/../js/highcharts/highcharts.js"></script>' % CURR_DIR +\
				  '<script src="%s/../js/highcharts/modules/exporting.js"></script>' % CURR_DIR +\
                  '<div id="container" style="min-width: 310px; height: 400px; margin: 0 auto"></div>' +\
				  "   </body>" +\
				  "</html>"



    def __init__(self):
        '''
        Constructor
        '''
        self.html = ChartMaker.JS_HEADER
    
    def add(self, javascriptStr):
        self.html += javascriptStr
        
    def closeJs(self):
        self.add('}')
        self.html += ChartMaker.HTML_FOOTER
        return self.html
    
    def getHTML(self):
        return self.html
    
    def createViz(self, chartType, title):
        self.add("chart: {type: '%s' },\n" % chartType)
        self.add("title: {text: '%s'},\n" % title)
        
class HistogramMaker(ChartMaker):
    
    def __init__(self, xAxisLabelArr, counts, chartTitle):
        super(HistogramMaker, self).__init__()
        self.xAxisLabelArr = xAxisLabelArr
        self.counts = counts
        
        series = DataSeries('Correct', counts)
        xAxis = Axis(axisDir='x', 
                     titleText='Correct answers',
                     labelArr = xAxisLabelArr,
                     )
        
        yAxis = Axis(axisDir='y',
                     titleText='Count',
                     dataSeriesArr=series
                     )
                     
                     
        self.createViz('column', chartTitle)
        self.add(str(xAxis) + ',')
        self.add(str(yAxis))
        self.closeJs()
        
        
class Axis(object):
    
    def __init__(self, axisDir='x', titleText=None, minimum=None, maximum=None, dataSeriesArr=None, labelArr=None):
        self.axisDict = {}
        self.axisDir = axisDir
        if titleText is not None:
            self.axisDict['title'] = "{text: '%s'}" % titleText
        if minimum is not None:
            self.axisDict['min'] = minimum
        if maximum is not None:
            self.axisDict['max'] = maximum
        if labelArr is not None:
            self.axisDict['categories'] = str(labelArr) + '\n'

    def __str__(self):
        res = ''
        if self.axisDir == 'x':
            res += 'xAxis: {\n'
        else:
            res += 'yAxis: {\n'
            
        for key in self.axisDict.keys():
            res += key + ': ' + self.axisDict[key] + ','
        res = res[:-1] + '}'
        return res
        
class DataSeries(object):
    
    def __init__(self, seriesName, dataArr, seriesType=None):
        self.seriesDict = {'name' : seriesName,
                           'data' : dataArr
                           }
        if seriesType is not None:
            self.seriesDict['type'] = seriesType
        
    def __str__(self):
        res = ''
        res += "{name: '%s',\n}" % self.seriesType['name']
        res += "data: %s}" % str(self.seriesDict['dataArr']) 
        return res
        
class Tooltip(object):
    
    def __init__(self, headerFormat=None, pointFormat=None, footerFormat=None, shared=None, useHTML=None):
        self.tooltipDict = {}
        if headerFormat is not None:
            self.tooltipDict['headerFormat'] = headerFormat
        if footerFormat is not None:
            self.tooltipDict['footerFormat'] = footerFormat
        if pointFormat is not None:
            self.tooltipDict['pointFormat'] = pointFormat
        if shared is not None:
            self.tooltipDict['shared'] = 'true'
        if useHTML is not None:
            self.tooltipDict['useHTML'] = 'true'
                            
    def __str__(self):
        res = 'tooltip: {'
        for key in self.tooltipDict.keys():
            res += key + ': ' + self.tooltipDict[key] + ','
        res = res[:-1] + '}'            
        return res       
            