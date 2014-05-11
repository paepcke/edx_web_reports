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
    An abstract superclass of all
    chart classes
    '''
    # Opening of complete HTML document
    # Includes start of <head>, up to 
    # just before the function def(s):
    HTML_HEADER = "<!DOCTYPE HTML>\n" +\
    			  " <head>\n" +\
    			  '     <meta http-equiv="Content-Type" content="text/HTML; charset=utf-8">\n' +\
    			  "     <title>OpenEdx Chart</title>\n" +\
			      "\n" +\
    			  '     <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js"></script>\n' +\
    			  '     <script type="text/javascript">\n'
    # Beginning of a function def inside <head>.
    # The %s is used in in each instantiation
    # of a chart making subclass to provide a name
    # to the function that defines that chart.
    # The name is used later in <div>s that contain
    # the respective chart:
    CHART_FUNC_HEADER = " $(function () {\n" +\
                        "     $('#%s').highcharts({\n"

    # Closing one chart function definition;
    # common to all definitions: 
    CHART_FUNC_FOOTER = "});});"
    CURR_DIR  = os.path.dirname(__file__)

    # End of a complete definition of chart 
    # functions in <head> section, plus 
    # ref to required Highchart files: 
    HTML_END_FUNC_DEFS = "      </script>" +\
				       "   </head>" +\
				       "   <body>" +\
				       '<script src="%s/../js/highcharts/highcharts.js"></script>' % CURR_DIR +\
				       '<script src="%s/../js/highcharts/modules/exporting.js"></script>' % CURR_DIR

    # A <div> in the <body> that contains a chart.
    # The %s is used to reference the chart object
    # that is to be included (i.e. a chart function definition
    # in <head> section):
    CHART_DIV   = '<div id="%s" style="min-width: 310px; height: 400px; margin: 0 auto"></div>'
    
    
    HTML_END	=  "   </body></html>"

    CHART_NAME_INDEX = 0


    # -------------------------------------- Superclass for All Chart Classes ----------------------------
    @classmethod
    def makeWebPage(cls, chartObjArr):
        '''
        Class method that creates a renderable
        HTML page, given an array of chart instances,
        i.e. of ChartMaker subclasses:
        :param cls: ChartMaker class object
        :type cls: ChartMaker
        :param chartObjArr: array of previously created chart objects
        :type chartObjArr: [Subclasses of ChartMaker]
        '''
        # HTML up to chart function defs in <head>:
        html = ChartMaker.HTML_HEADER
        # Add each chart function definition:
        for chartObj in chartObjArr:
            html += chartObj.getChartFuncSource()
        # Close out the <head> section, finishing
        # chart function defs, and reference Highchart
        # files:
        html += ChartMaker.HTML_END_FUNC_DEFS

        # Create one <div> section for each chart:
        for chartObj in chartObjArr:
            html += ChartMaker.CHART_DIV % chartObj.getInternalName() 

        return html

    def __init__(self):
        '''
        Init method of abstract superclass:
        '''
        self.internalChartName = 'chart%d' % ChartMaker.CHART_NAME_INDEX
        ChartMaker.CHART_NAME_INDEX += 1
        self.thisChartFuncHeader = ChartMaker.CHART_FUNC_HEADER % self.internalChartName
        
        self.funcDef = self.thisChartFuncHeader

    def getChartFuncSource(self):
        '''
        Return a fully formed chart function.
        :return: Highcharts chart function
        :rtype: String 
        '''
        return self.funcDef + ChartMaker.CHART_FUNC_FOOTER

    def getInternalName(self):
        '''
        Each chart object holds an automatically
        generated name. The name is used to reference
        the chart (function) in <div> sections.
        :returns: Fully formed function, including all closing parens/braces
        :rtype: String
        '''
        return self.internalChartName
    
    def add(self, javascriptStr):
        '''
        Add one substring to the growing function body
        :param javascriptStr: substring to add
        :type javascriptStr: String
        '''
        self.funcDef += javascriptStr

    def backtrack(self, numChars=1):
        '''
        Remove numChars characters from the function
        body. Used in loops where commas are added.
        The last comma must often be removed
        :param numChars: number of characters to remove from function body
        :type numChars: int
        '''
        self.funcDef = self.funcDef[:-numChars]

    def addAllSeries(self, seriesArray):
        '''
        Given an array of DataSeries objects,
        add them to the function body. Data series
        are yAxis values. Can have multiple for charts
        like column charts:
        :param seriesArray: all data series objects to add. 
        :type seriesArray: [DataSeries]
        '''
        self.add('series: [')
        for seriesObj in seriesArray:
            self.add(str(seriesObj) + ',')
        # Remove last comma:
        self.backtrack()
        self.add(']')
        
    def createViz(self, chartType, title):
        '''
        Start of data structure for all Highchart functions.
        :param chartType: type of chart: 'column', 'pie', etc.
        :type chartType: String
        :param title: title of entire chart. Will be printed above the chart
        :type title: String
        '''
        self.add("chart: {type: '%s' },\n" % chartType)
        self.add("title: {text: '%s'},\n" % title)

# ---------------------------------------  Chart Class Histogram ----------------------------        
        
# Classes that library users can instantiate

class Histogram(ChartMaker):
    '''
    A histogram maker
    '''
    
    def __init__(self, chartTitle, xAxisTitle, xAxisLabelArr, counts):
        '''
        Special subclass for making histograms.
        :param chartTitle: Title to print underneath the chart
        :type chartTitle: String
        :param xAxisTitle: x-Axis name
        :type xAxisTitle: String
        :param xAxisLabelArr: labels along the x-Axis
        :type xAxisLabelArr: [String]
        :param counts: y-values
        :type counts: DataSeries
        '''
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
                     
        # Start a chart function:             
        self.createViz('column', chartTitle)
        self.add(str(xAxis) + ',')
        self.add(str(yAxis) + ',')
        self.addAllSeries([series])
        
        

# ---------------------------------------  Chart Class Pie ----------------------------        
        
class Pie(ChartMaker):
    
    def __init__(self):
        super(Pie, self).__init__()
# ---------------------------------------  Service Classes ----------------------------        

# ---------------------------------------  Support Classes ----------------------------        
class Axis(object):
    '''
    Container for information needed for x or y axes.
    '''
    
    def __init__(self, axisDir='x', titleText=None, minimum=None, maximum=None, dataSeriesArr=None, labelArr=None):
        '''
        Args are all keyword optionals. Which are required
        depends on the type of chart. For continuous quantities, minimum/maximum can be supplied, etc.
        :param axisDir: Whether an 'x' axis, or a 'y' axis
        :type axisDir: Char
        :param titleText: title of this axis; printed below or to the side, depending on axis dir.
        :type titleText: String
        :param minimum: minimum value of the axis
        :type minimum: {int | float}
        :param maximum: maximum value of the axis
        :type maximum: {int | float}
        :param dataSeriesArr: array of DataSeries objects to chart
        :type dataSeriesArr: [DataSeries]
        :param labelArr: axis labels
        :type labelArr: [String]
        '''
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
        '''
        Called when str function is applied to an instance
        of this class.
        :return: the piece of a Highchart datastructure that defines an axis
        :rtype: String
        '''
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
    '''
    Holds one data series
    '''
    
    def __init__(self, seriesName, dataArr, seriesType=None):
        self.seriesDict = {'name' : seriesName,
                           'data' : dataArr
                           }
        if seriesType is not None:
            self.seriesDict['type'] = seriesType
        
    def __str__(self):
        '''
        Called when str function is applied to an instance
        of this class.
        :return: the piece of a Highchart datastructure that defines one data series
        :rtype: String
        '''
        res = ''
        res += "{name: '%s',\n" % self.seriesDict['name']
        res += "data: %s}" % str(self.seriesDict['data']) 
        return res
        
class Tooltip(object):
    '''
    Holds information about tooltips
    '''
    
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
        '''
        Called when str function is applied to an instance
        of this class.
        :return: the piece of a Highchart datastructure that defines a data series
        :rtype: String
        
        '''
        res = 'tooltip: {'
        for key in self.tooltipDict.keys():
            res += key + ': ' + self.tooltipDict[key] + ','
        res = res[:-1] + '}'            
        return res       
            