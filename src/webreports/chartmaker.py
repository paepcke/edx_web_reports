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

    HTML_HEADER = "<!DOCTYPE HTML>\n" +\
                  "<funcDef>\n" +\
    			  " <head>\n" +\
    			  '     <meta http-equiv="Content-Type" content="text/funcDef; charset=utf-8">\n' +\
    			  "     <title>OpenEdx Chart</title>\n" +\
			      "\n" +\
    			  '     <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js"></script>\n' +\
    			  '     <script type="text/javascript">\n'
    CHART_FUNC_HEADER = " $(function () {\n" +\
                        "     $('#%s').highcharts({\n"

    CHART_FUNC_FOOTER = "});});"
    CURR_DIR  = os.path.dirname(__file__)

    HTML_END_FUNC_DEFS = "      </script>" +\
				       "   </head>" +\
				       "   <body>" +\
				       '<script src="%s/../js/highcharts/highcharts.js"></script>' % CURR_DIR +\
				       '<script src="%s/../js/highcharts/modules/exporting.js"></script>' % CURR_DIR

    CHART_DIV   = '<div id="%s" style="min-width: 310px; height: 400px; margin: 0 auto"></div>'
    
    
    HTML_END	=  "   </body></html>"

    CHART_NAME_INDEX = 0

    @classmethod
    def makeWebPage(cls, chartObjArr):
        html = ChartMaker.HTML_HEADER
        for chartObj in chartObjArr:
            html += chartObj.getChartFuncSource()
        html += ChartMaker.HTML_END_FUNC_DEFS

        for chartObj in chartObjArr:
            html += ChartMaker.CHART_DIV % chartObj.getInternalName() 

        return html

    def __init__(self):
        '''
        Constructor
        '''
        self.internalChartName = 'chart%d' % ChartMaker.CHART_NAME_INDEX
        ChartMaker.CHART_NAME_INDEX += 1
        self.thisChartFuncHeader = ChartMaker.CHART_FUNC_HEADER % self.internalChartName
        
        self.funcDef = self.thisChartFuncHeader

    def getChartFuncSource(self):
        return self.funcDef + ChartMaker.CHART_FUNC_FOOTER

    def getInternalName(self):
        return self.internalChartName
    
    def add(self, javascriptStr):
        self.funcDef += javascriptStr

    def backtrack(self, numChars=1):
        self.funcDef = self.funcDef[:-numChars]

    def addAllSeries(self, seriesArray):
        '''
        
        :param seriesArray: array of DataSeries objects
        :type seriesArray: [DataSeries]
        '''
        self.add('series: [')
        for seriesObj in seriesArray:
            self.add(str(seriesObj) + ',')
        # Remove last comma:
        self.backtrack()
        self.add(']')
        
    def createViz(self, chartType, title):
        self.add("chart: {type: '%s' },\n" % chartType)
        self.add("title: {text: '%s'},\n" % title)
        
class Histogram(ChartMaker):
    
    def __init__(self, chartTitle, xAxisTitle, xAxisLabelArr, counts):
        super(Histogram, self).__init__()
        self.xAxisLabelArr = xAxisLabelArr
        self.counts = counts
        
        series = DataSeries('Correct', counts)
        xAxis = Axis(axisDir='x', 
                     titleText=xAxisTitle,
                     labelArr = xAxisLabelArr,
                     )
        
        yAxis = Axis(axisDir='y',
                     titleText='Count',
                     dataSeriesArr=series
                     )
                     
                     
        self.createViz('column', chartTitle)
        self.add(str(xAxis) + ',')
        self.add(str(yAxis) + ',')
        self.addAllSeries([series])
        
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
        res += "{name: '%s',\n" % self.seriesDict['name']
        res += "data: %s}" % str(self.seriesDict['data']) 
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
            