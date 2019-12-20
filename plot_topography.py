#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#=======================================================================
#  Plot_topography - Version 1.0
#  Copyright 2019   Fernando Borbon
#======================================================================= 

# Import libraries 
import matplotlib.pyplot as plt
import numpy as np
import pyproj
import os

from osgeo import gdal
gdal.UseExceptions()
#import cartopy.crs as ccrs

#***********************************************************************
# Creates the directory if it does not exists
def ensure_dir(f):
	d = os.path.abspath(f)
	if not os.path.exists(d):
		os.makedirs(d)


# Save plot to file
def save_figures(figure_handle, outputFolder, fileFormat, filename):
	ensure_dir(outputFolder)
	
	if fileFormat=='pdf':
		# Save group in pdf document
		filepath = outputFolder + filename + '.pdf'
		if os.path.isfile(filepath):
			os.remove(filepath) 
		
		pp = PdfPages(filepath)
		try:
			for i in range(0, len(figure_handle['fig'])): 
				pp.savefig(figure_handle['fig'][i], bbox_inches='tight')
		except:
			pp.savefig(figure_handle['fig'], bbox_inches='tight')
		pp.close()
	
	elif fileFormat=='png':
		# Save individual PNG files
		for i in range(0, len(figure_handle['fig'])):
			figure_handle['fig'][i].tight_layout()
			figure_handle['fig'][i].savefig(outputFolder+figure_handle['name'][i]+'.png', dpi=300)


# Plot topography map
def plot_topo(fileFolderIn, fileName, p0, save_figs):
	# Plot image for topography data
	print(' Enters function plot_topo')
	
	# Setings
	color_list = ['b', 'r', 'y', 'c', 'pink', 'orange', 'k']
	fsizeL = 10; fsizeT = 10;  fsizeA = 10; fsizeText = 8; fsizeLeg = 12
	fig_num = 0 
	figure_handle = {'fig':[], 'name':[]}
	fileFormat = 'png'
	save_figs = 1 # Turn on figure saving to files
	
	#........................................................................
	figuresFolder = fileFolderIn
	filePath = fileFolderIn + fileName
	
	ds = gdal.Open(filePath)
	data = ds.ReadAsArray()
	data[data<=0] = -1000
	gt = ds.GetGeoTransform() # x0, dx, dxdy, y0, dydx, dy
	extent = (gt[0], gt[0] + ds.RasterXSize * gt[1], gt[3] + ds.RasterYSize * gt[5], gt[3])
	
	#........................................................................
	p = pyproj.Proj(proj='utm',zone='30T north',ellps='WGS84', epgs=4326, datum='WGS84', units='m')
	extent_UTM = np.array(p(extent[0:2], extent[2:])).flatten()/1000
	
	#........................................................................
	fig_num += 1 
	fig = plt.figure(num=fig_num, figsize=(10,10))
	figure_handle['fig'].append(fig)
	figure_handle['name'].append('Spain_topography')
	ax = fig.add_subplot()  # projection=ccrs.PlateCarree()
	ax.hlines(p0[1],    p0[0], p0[0]+10, color='k', lw=3)
	ax.hlines(p0[1]+10, p0[0], p0[0]+10, color='k', lw=3)
	ax.vlines(p0[0],    p0[1], p0[1]+10, color='k', lw=3)
	ax.vlines(p0[0]+10, p0[1], p0[1]+10, color='k', lw=3)
	ax.plot([p0[0]+10, extent_UTM[1]], [p0[1]+10, extent_UTM[-1]], color='k', lw=3)
	ax.plot([p0[0]+10, extent_UTM[1]], [p0[1], extent_UTM[-2]], color='k', lw=3)
	c = ax.imshow(data, origin='upper', cmap='terrain',extent=extent_UTM)  # transform=ccrs.PlateCarree() / transform=ccrs.Geodetic()
#	cbar = plt.colorbar(c)
#	cbar.set_label('Altitude [m]')
#	ax.set_xlim([600, 620])
#	ax.set_ylim([4735, 4755])
	plt.xlabel('Easting [km]', fontsize=fsizeL)
	plt.ylabel('Northing [km]', fontsize=fsizeL)
	plt.show()
	
	#....................................
	if save_figs:
		print('  Save figures to files in folder: '+figuresFolder)
		save_figures(figure_handle, figuresFolder, fileFormat, 'plot_topo')


#***********************************************************************
# Plot topography
# Source: http://opentopo.sdsc.edu/rasterOutput?jobId=rt1576079091524&metadata=1
# Download data: https://b2drop.eudat.eu/s/XGTw72xmnQ9JLno

def main():
	fileFolderIn = '/mnt/Storage/Datos/Mediciones/RAW/Alaiz/Mapa SRTM/v4/'
	fileName = 'output_srtm.tif'
	fileFormat = 'png'
	save_figs = 1
	# square
	#p0 = np.array([613, 4726])    # Bottom left corner of square. Original values 
	p0 = np.array([604, 4739.25])  # Correct square limits for better match 
	plot_topo(fileFolderIn, fileName, p0, save_figs)

