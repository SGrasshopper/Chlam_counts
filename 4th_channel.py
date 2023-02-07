from ij.plugin import ImageCalculator
from net.imglib2.img.display.imagej import ImageJFunctions
from java.awt.event import TextListener
from ij import Menus
from ij.gui import GenericDialog
from ij.io import OpenDialog
from ij.measure import ResultsTable
from ij.gui import WaitForUserDialog
from ij.plugin import ChannelSplitter
import java.util.ArrayList as ArrayList
import csv
import os
import sys
from ij import IJ
from ij import ImagePlus

imp = IJ.getImage()
orgtitle = imp.getTitle()
dimentions = imp.getDimensions()
numZ, nChannels, numframes  = dimentions[3], dimentions[2], dimentions[4]
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
IJ.run("Merge Channels...", "c1=GFP c2=RFP c3=DAPI c4=result create")
IJ.selectWindow(orgtitle)
#github test yay
