import fiji.plugin.trackmate.features.FeatureFilter as FeatureFilter
import fiji.plugin.trackmate.features.track.TrackDurationAnalyzer as TrackDurationAnalyzer
import fiji.plugin.trackmate.features.track.TrackSpotQualityFeatureAnalyzer as TrackSpotQualityFeatureAnalyzer
import fiji.plugin.trackmate.Spot as Spot
import fiji.plugin.trackmate.Spot.frameComparator as frameComparator
import fiji.plugin.trackmate.Model as Model
import fiji.plugin.trackmate.Settings as Settings
import fiji.plugin.trackmate.TrackMate as TrackMate
import fiji.plugin.trackmate.detection.LogDetectorFactory as LogDetectorFactory
import fiji.plugin.trackmate.tracking.jaqaman.SparseLAPTrackerFactory as SparseLAPTrackerFactory
import fiji.plugin.trackmate.features.spot.SpotIntensityMultiCAnalyzerFactory as SpotIntensityMultiCAnalyzerFactory
from fiji.plugin.trackmate import SelectionModel
from fiji.plugin.trackmate.gui.displaysettings import DisplaySettingsIO
from fiji.plugin.trackmate.visualization.hyperstack import HyperStackDisplayer
from ij.plugin import ChannelSplitter
from ij.plugin import ImageCalculator
from net.imglib2.img.display.imagej import ImageJFunctions
from java.awt.event import TextListener
from ij import Menus
from ij.gui import GenericDialog
from ij.io import OpenDialog
from ij.measure import ResultsTable
from ij.gui import WaitForUserDialog
import java.util.ArrayList as ArrayList
import csv
import os
import sys
from ij import IJ
from ij import ImagePlus
import shutil
import time
from ij.gui import GenericDialog
import sys
from ij.plugin.frame import RoiManager


def roi_save():
	imp = IJ.getImage()
	orgtitle = imp.getTitle()
	dimentions = imp.getDimensions()
	numZ, nChannels, numframes  = dimentions[3], dimentions[2], dimentions[4]
	imp.setPosition(1,numZ/2,1)
	IJ.resetMinAndMax(imp)
	IJ.run(imp, "Enhance Contrast", "saturated=0.35")
	IJ.setTool("freehand")
	WaitForUserDialog("Circle Inclusion, then click OK.").show()
	imp = IJ.getImage()
	roi = imp.getRoi()
	rm.addRoi(roi)
	IJ.run('Close')
	
#-----------------------------------------------------------------------------
od = OpenDialog("Time Laps Images", "")
	
firstDir = od.getDirectory()
fileList = os.listdir(firstDir)
if "DisplaySettings.json" in fileList:
	    fileList.remove("DisplaySettings.json")
if ".DS_Store" in fileList:  
	    fileList.remove(".DS_Store")  

fileList.sort()
rm = RoiManager()
	#path='/Users/scottgrieshaber/Documents/Counts_scripts/AScIELVA/cropped_images/'
for	fileName in fileList:
	currentFile = firstDir + fileName
	print(currentFile)
	IJ.run("Bio-Formats Importer", "open=[" + currentFile + "] color_mode=Composite view=Hyperstack stack_order=XYCZT")
	roi_save()
	
rm.save("/Users/scottgrieshaber/Desktop/RoiSet.zip")
#------------------------------------------------------------------------------------
	
	
