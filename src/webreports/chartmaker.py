'''
Created on May 8, 2014

@author: paepcke
'''
import os
from collections import MutableMapping


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
        :param chartObjArr: array of previously created chart objects. 
            Individual chart object works as well. 
        :type chartObjArr: {[Subclasses of ChartMaker] | Subclasses of ChartMaker}
        '''
        
        if not isinstance(chartObjArr, list):
            chartObjArr = [chartObjArr]
        
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
        
    def createViz(self, title, chartArgs):
        '''
        Start of data structure for all Highchart functions.

        :param title: title of entire chart. Will be printed above the chart
        :type title: String
        :param chartArgs: dict with attribute value pairs. Ex::
                {'type' : 'column'}
            for column charts, or:: 
                {
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false
                }
            for pie charts.
        :type chartArg: {String : String}
        '''
        self.add('chart: ' + '{')
        for argKey in chartArgs.keys():
            self.add(argKey + ': ' + chartArgs[argKey] + ',')
        self.backtrack()
        self.add('},')
        self.add("title: {text: '%s'},\n" % title)

# ---------------------------------------  Chart Class Histogram ----------------------------        
        
# Classes that library users can instantiate

class Histogram(ChartMaker):
    '''
    A histogram maker
    '''
    def __init__(self, chartTitle, xAxisTitle, histogramData):
        '''
        Special subclass for making histograms. The histogramData
        is a dictionary. If it is an OrderedDict then the order
        will map to the columns from left to right. If it is
        a regular dict, then the order along the x-axis depends
        on the Python implementation. 

        :param chartTitle: Title to print underneath the chart
        :type chartTitle: String
        :param xAxisTitle: x-Axis name
        :type xAxisTitle: String
        :param histogramData: [ordered] dictionary of x axis labels and counts 
        :type histogramData: {String : {int | float}}
        '''
        super(Histogram, self).__init__()
        
        series = DataSeries(xAxisTitle, histogramData.values())
        xAxis = Axis(axisDir='x', 
                     titleText=xAxisTitle,
                     labelArr = histogramData.keys(),
                     )
        
        yAxis = Axis(axisDir='y',
                     titleText='Count',
                     dataSeriesArr=series
                     )
                     
        # Start a chart function:  
        self.createViz(chartTitle, {'type' : "'column'"})
        self.add(str(xAxis) + ',')
        self.add(str(yAxis) + ',')
        self.addAllSeries([series])
        
        

# ---------------------------------------  Chart Class Pie ----------------------------        
        
class Pie(ChartMaker):
    
    def __init__(self, chartTitle, pieSectionsDataDict):
        super(Pie, self).__init__()

        # Start the function string, taking
        # care of the 'chart' and 'title' entries:
        self.createViz(chartTitle, {'plotBackgroundColor' : 'null',
                                    'plotBorderWidth' : 'null',
                                    'plotShadow' : 'false'
                                    })

        self.add("plotOptions: {" +
                 "pie: {" +
                     "allowPointSelect: true," +
                     "cursor: 'pointer'," +
                     "dataLabels: {" +
                         "enabled: true," +
                         "format: '<b>{point.name}</b>: {point.percentage:.1f} %'," +
                         "style: {" +
                             "color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'" +
                             "}"
                        "}" +
                    "}" + # close pie:...
                  "},") # close plotOptions
                 
        self.add('series: [{')
        self.add("type: 'pie',")
        self.add("name: '%s'," % self.internalChartName)
        self.add("data: [")
        for pieSectionKey in pieSectionsDataDict:
            self.add("['%s', %s]," % (pieSectionKey, pieSectionsDataDict[pieSectionKey]))
        self.backtrack() # remove trailing comma left by loop
        self.add(']')  # close 'data: [': array of attr/value arrays 
        self.add("}]") # close 'series: [{'


class Line(ChartMaker):
    
    def __init__(self, chartTitle, xAxisLabels, yAxisTitle, lineSeriesObjArray):
        '''
        Special subclass for making line graphs. The lineData
        is a dictionary. 
        
        :param chartTitle: Title to print underneath the chart
        :type chartTitle: String
        :param yAxisTitle: x-Axis name
        :type yAxisTitle: String
        :param lineSeriesObjArray: array of DataSeries objects
        :type lineSeriesObjArray: [DataSeries]
        '''
        super(Line, self).__init__()
        
        #******series = DataSeries(yAxisTitle, lineData.values())

        if not isinstance(lineSeriesObjArray, list):
            lineSeriesObjArray = [lineSeriesObjArray]

        xAxis = Axis(axisDir='x', 
                     labelArr = xAxisLabels
                     )

        yAxis = Axis(axisDir='y',
                     titleText=yAxisTitle,
                     dataSeriesArr=lineSeriesObjArray,
                     argDict = {
                                'plotLines': [{
                                               'value': 0,
                                               'width': 1,
                                               'color': '#808080'
                                               }]
                                }
                    )

        legend = "legend: {" +\
                    "layout: 'vertical'," +\
                    "align: 'right'," +\
                    "verticalAlign: 'middle'," +\
                    "borderWidth: 0" +\
                  "}"

        # Start a chart function:  
        self.createViz(chartTitle, {'type' : "'line'"})
        self.add(str(xAxis) + ',')
        self.add(str(yAxis) + ',')
        self.add(legend + ',')
        self.addAllSeries(lineSeriesObjArray)

        
# ---------------------------------------  Support Classes ----------------------------        
class Axis(object):
    '''
    Container for information needed for x or y axes.
    '''
    
    def __init__(self, 
                 axisDir='x', 
                 titleText=None, 
                 dataSeriesArr=None, 
                 labelArr=None,
                 argDict=None):
        '''
        Args are all keyword optionals. Which are required
        depends on the type of chart. For continuous quantities, minimum/maximum can be supplied, etc.

        :param axisDir: Whether an 'x' axis, or a 'y' axis
        :type axisDir: Char
        :param titleText: title of this axis; printed below or to the side, depending on axis dir.
        :type titleText: String
        :param dataSeriesArr: array of DataSeries objects to chart
        :type dataSeriesArr: [DataSeries]
        :param labelArr: axis labels
        :type labelArr: [String]
        :param argDict: dictionary of additional arg/value pairs for the axis
        :type argDict: {Any : Any} 
        '''
        self.axisDict = {}
        self.axisDir = axisDir
        if titleText is not None:
            self.axisDict['title'] = "{text: '%s'}" % titleText
        if labelArr is not None:
            self.axisDict['categories'] = str(labelArr) + '\n'
        
        # Merge the arbitrary-args dictionary with
        # the other axis data:
        if argDict is not None:
            self.axisDict = dict(list(self.axisDict.items()) + list(argDict.items()))

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
            res += key + ': ' + str(self.axisDict[key]) + ','
        res = res[:-1] + '}'
        return res

    
class BasicDict(MutableMapping):
    '''
    A generic dictionary. Needed now because the
    wonderfully practical DictMixin in going away
    in Python 3. This is the new mixin.
    '''

    def __init__(self, *args, **kwargs):
        self.store = dict()
        self.update(dict(*args, **kwargs))  # use the free update to set keys

    def __getitem__(self, key):
        return self.store[self.__keytransform__(key)]

    def __setitem__(self, key, value):
        self.store[self.__keytransform__(key)] = value

    def __delitem__(self, key):
        del self.store[self.__keytransform__(key)]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def __keytransform__(self, key):
        return key

class DataSeries(BasicDict):
    '''
    Holds one data series
    '''
    
    def __init__(self, seriesName, dataArr, seriesType=None):
        super(DataSeries, self).__init__()
        
        self['name'] = seriesName
        self['data'] = dataArr
        
        if seriesType is not None:
            self['type'] = seriesType
        
    def name(self):
        return self['name']
    
    def data(self):
        return self['data']
        
    def __str__(self):
        '''
        Called when str function is applied to an instance
        of this class.
        :return: the piece of a Highchart datastructure that defines one data series
        :rtype: String
        '''
        res = ''
        res += "{name: '%s',\n" % self['name']
        res += "data: %s}" % str(self['data']) 
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
            