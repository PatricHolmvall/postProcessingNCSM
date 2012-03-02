# This file is part of PostProcessingNCSM.
#
# PostProcessingNCSM is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PostProcessingNCSM is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PostProcessingNCSM. If not, see <http://www.gnu.org/licenses/>.

import pickle
import numpy as np
import pylab as pl
import itertools as it
from matplotlib import rc
from matplotlib.ticker import *
import matplotlib.pyplot as plt


#try:
#    pf = open('../runs/'+rp.dataFile)
#except IOError:
#    raise Exception("Unable to open the data file 'runs/"
#                    ""+str(rp.dataFile)+"', make sure that it lies in the "
#                    "correct folder with read premission.")



def unpickleDataFile(dataFile):
    """
    Unpickle NCSM data file and return the data structure in it.

    :type dataFile: string
    :param dataFile: Data file containing NCSM runs.

    :type allRuns: dict
    :param allRuns: Dictionary containing the NCSM runs and all the associated
                    data for each run. The dictionary is in a very specific
                    format, described in the file
                    `currentDictionaryStructure.txt`.
    """
    pf = open('runs/'+dataFile)
    allRuns = pickle.load(pf)

    return allRuns




def printInfo(dataFile, allRuns):
    """
    Print info about the runs and observables measured in a NCSM run data file.

    :type dataFile: string
    :param dataFile: Data file containing NCSM runs.
    
    :type allRuns: dict
    :param allRuns: Dictionary containing the NCSM runs and all the associated
                    data for each run. The dictionary is in a very specific
                    format, described in the file
                    `currentDictionaryStructure.txt`.
    """
    print 'Number of runs in datafile \''+str(dataFile)+'\': ',
    print str(len(allRuns))

    for ncsmrun in allRuns:
        print '\n\n###### NCSM-Run: ' + str(ncsmrun),
        print ' ######'
        print 'Fields/Observables:',
        print '\'' + '\', \''.join(allRuns[ncsmrun]) + '\''




def journalStylePlot(figureWidthPt):
    """
    Fix figure proportions to match journal-style. Provide 

    :type figureWidthPt: float
    :param figureWidthPt: Figure width in pt.

    :type figureSize: list
    :param figureSize: List of floats describing width and height of figure.
    """
    
    inchesPerPt = 1.0/72.27 # Convert pt to inch
    goldenMean = (np.sqrt(5)-1.0)/2.0 # Aesthetic ratio
    figureWidth = figureWidthPt*inchesPerPt # width in inches
    figureHeight = figureWidth*goldenMean # height in inches
    figureHeight = figureHeight + 40 * inchesPerPt # Add space for title
    figureSize =  [figureWidth,figureHeight]
    return figureSize




def plotObservable(dataSeries, groupBy, xLabel, yLabel, plotStyle):
    """
    Plot an observable with dependence 

    :type rp: :class:`run_params.RunParams` class
    :param rp: An instance of RunParams containing which file, observables and
               fitting function to use.
    """




def preformFit(rp):
    """
    Preform a chi-squared fit procedure on observables in a NCSM run. The
    fitting functions are defined in the fit_functions.py file.

    :type rp: :class:`run_params.RunParams` class
    :param rp: An instance of RunParams containing which file, observables and
               fitting function to use.
    """
    print 'fit the function, freddy!'




def postProcess(rp):
    """
    Post Process NCSM runs in a file and plot observables versus hw or Nmax. All
    post processing settings, including data file and what observables to plot
    are set by the user in the runner-file through the :class:`RunParams` class.

    :type rp: :class:`run_params.RunParams` class
    :param rp: An instance of RunParams with different settings for the post
               processing.
    """
    
    # List of dictionaries containing different quantities that observables can
    # be plotted against.
    dependenceList = [{'id': 'nmax', 'invert': False, 'group': 'hw',
                       'groupLabel': r'$\hbar\Omega$'},
                      {'id': 'nmax', 'invert': True, 'group': 'hw',
                       'groupLabel': r'$\hbar\Omega$'},
                      {'id': 'hw', 'invert': False, 'group': 'nmax',
                       'groupLabel': r'N${_max}$'}]

                  
    # Unpickle
    allRuns = unpickleDataFile(rp.dataFile)


    # Print info
    if rp.printInfo:
        printInfo(allRuns)


    # Set rc parameters for LaTeX support in figures
    pl.rcParams.update(rp.rcUserParams)


    # Preform chi-squared fit procedure
    if rp.preformFit:
        preformFit(rp)


    ncsmRunList = []

    figureNumber = 1
    
    # Loop through runs
    for ncsmrun in allRuns:
        ncsmRunList.append(ncsmrun)

        # Loop through observables provided by the user
        for observable in rp.observables:
            # Make list of tuples into numpy array
            runData = np.array(allRuns[ncsmrun][observable['id']])

            
            # Create a view of runData in order to enable sorting without
            # changing the shape or integrity of runData. The view will be a
            # structured array with specified labels, which is good for sorting,
            # while runData will remain a numpy 2D ndarray which is good for
            # plotting and doing math.
            dt = [('hw',float), ('nmax',float), (observable['id'],float)]
            runDataView = runData.ravel().view(dt)

            # Group the data 
            runDataView.sort(order=dependenceList[rp.xAxisVariable]['group'])

            groupList = []

            if observable['drawPlot']:
                pl.figure(figureNumber)
                pl.title(r'NCSM run: '+str(ncsmrun))
                pl.xlabel(observable['xlabel'])
                pl.ylabel(observable['ylabel'])

            # Group data by distinct values to create data series
            keynum = 0
            for key, group in it.groupby(runData, lambda x: x[0]):
                styleNum = keynum%len(rp.plotStyle)
                groupList.append(key)
                dataSeries = np.array(list(group))
                if observable['drawPlot']:
                    pl.plot(dataSeries[:,1],dataSeries[:,2],
                            rp.plotStyle[styleNum][0],
                            markersize=rp.plotStyle[styleNum][1],label=str(key))
                keynum += 1
            figureNumber += 1
            
            if observable['drawPlot']:
                pl.legend(loc=4,
                          title=dependenceList[rp.xAxisVariable]['groupLabel'])
    # Show plots
    if rp.drawPlot:
        pl.show()
