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


def im_process():
	imp = IJ.getImage()
	orgtitle = imp.getTitle()
	print(orgtitle)
	dimentions = imp.getDimensions()
	numZ, nChannels, numframes  = dimentions[3], dimentions[2], dimentions[4]
	imp.setPosition(1,numZ/2,1)
	IJ.resetMinAndMax(imp)
	IJ.run(imp, "Enhance Contrast", "saturated=0.35")
	IJ.setTool("freehand")
	WaitForUserDialog("Circle Inclusion, then click OK.").show()
	IJ.run("Clear Outside")
	IJ.run("Duplicate...", "duplicate")
	IJ.selectWindow(orgtitle)
	IJ.run('Close')
	imp = IJ.getImage()
	newtitle = imp.getTitle()
	channels = ChannelSplitter.split(imp)
	imp_GFP = channels[0]
	imp_RFP = channels[1]
	imp_DAPI = channels[2]
	imp3 = ImageCalculator.run(imp_GFP, imp_RFP, "Add create 32-bit stack")
	imp_all = ImageCalculator.run(imp3, imp_DAPI, "Add create 32-bit stack")
	imp_all.setPosition(1,numZ/2,1)
	IJ.resetMinAndMax(imp_all)
	IJ.run(imp_all, "Enhance Contrast", "saturated=0.35")
	IJ.run(imp_all, "16-bit", "")
	imp_GFP.setTitle('GFP')
	imp_RFP.setTitle('RFP')
	imp_DAPI.setTitle('DAPI')
	imp_all.setTitle('result')
	imp_GFP.show()
	imp_RFP.show()
	imp_DAPI.show()
	imp_all.show()
	imp_all_dup = imp_all.duplicate()
	#IJ.run(imp_all_dup, "Convert to Mask", "method=IsoData background=Dark black")
	# look at this method
	#IJ.run(imp_all_dup, "Auto Threshold", "method=IsoData white stack use_stack_histogram")
	IJ.run(imp_all_dup, "Auto Threshold", "method=Default white stack use_stack_histogram")
	
	IJ.run(imp_all_dup, "Divide...", "value=255 stack")
	imp_all2 = ImageCalculator.run(imp_all, imp_all_dup, "Multiply create 16-bit stack")
	imp_all2.setTitle("result2")
	#IJ.resetMinAndMax(imp_all2)
	#IJ.run(imp_all2, "Enhance Contrast", "saturated=0.35")
	#IJ.run(imp_all2, "16-bit", "")
	imp_all2.show()
	

	IJ.run("Merge Channels...", "c1=GFP c2=RFP c3=DAPI c4=result2 create")
	IJ.selectWindow(newtitle)
	IJ.run('Close')
	IJ.selectWindow('Composite')
	IJ.run("Set Scale...", "distance=0")
	IJ.run("Re-order Hyperstack ...", "channels=[Channels (c)] slices=[Frames (t)] frames=[Slices (z)]")
	
	imp_comp = IJ.getImage()
	IJ.run(imp_comp, "Bio-Formats Exporter", "save=/Users/brendangrieshaber/Desktop/test-output/" + orgtitle + ".ome.tif export compression=LZW")
    #IJ.selectWindow('Merged')
	IJ.run('Close')

od = OpenDialog("Time Laps Images", "")
firstDir = od.getDirectory()
fileList = os.listdir(firstDir)

if "DisplaySettings.json" in fileList:
    fileList.remove("DisplaySettings.json")
if ".DS_Store" in fileList:  
    fileList.remove(".DS_Store")  
#print(firstDir + fileList[0])

fileList.sort()
for fileName in fileList:
    currentFile = firstDir + fileName
    print(currentFile)
    #IJ.run("Bio-Formats Importer", "open=[" + currentFile + "] color_mode=Default split_channels view=Hyperstack stack_order=XYCZT series_list="+str(i))
    #IJ.run("Bio-Formats Importer", "open=[" + currentFile + "] color_mode=Composite view=Hyperstack stack_order=XYCZT use_virtual_stack")
    IJ.run("Bio-Formats Importer", "open=[" + currentFile + "] color_mode=Composite view=Hyperstack stack_order=XYCZT")
    #IJ.run("Set Measurements...", "area limit redirect=None decimal=0")
    #imp = IJ.openImage(currentFile)
    #imp.show()
    im_process()
    