######################################################################
# This code uses a cluster-counting algorithm to determine whether   #
# a randomly populated square lattice percolates.                    #
######################################################################

import pygame, random, time
import numpy as np

##start pygame
pygame.init()

##DEFINE PERCOLATION VARIABLES
while True:
	n = input("Enter matrix size: ")
	p = input ("Enter occupation probability as a percentage(0<p<100): ")
	if type(n) is int and type(p) is int:
		break
	else:
		print "\nEnter integer values."

##DEFINE FUNCTIONS
def draw_lat(): ##Draw Lattice
	lat = np.zeros((n,n), int)
	for i in range(0,n):
		for j in range(0, n):
			rando = random.randint(1, 100)
			if rando < p:
				lat[i,j] = 1
				pygame.draw.rect(screen,(255,255,255),[j*inc, i*inc,inc,inc])   				
			else:
				pygame.draw.rect(screen,(0,0,0),[j*inc, i*inc,inc,inc])
			pygame.display.flip()
	return(lat)
def neighbors(can, lat, i, j,n, x): ##find neighbors
	nn = np.zeros((5), int)
	nn[0] = lat[i, j]#current block
	if (nn[0] == 1):
		lat[i,j] = x + 2
		update_lat(lat, x)
	if (i > 0 ):
		nn[1] = lat[i-1, j] #up
		if nn[1] == 1:
			b = np.array([i-1, j])
			can = np.vstack((can, b))
			lat[i-1,j] = x+2
			update_lat(lat, x)
	if (i < n-1):
		nn[2] = lat[i+1, j] #down
		if nn[2] == 1:
			b = np.array([i+1, j])
			can = np.vstack((can, b))
			lat[i+1,j] = x+2
			update_lat(lat, x)
	if (j > 0):
		nn[3] = lat[i, j-1] #left
		if nn[3] == 1:
			b = np.array([i, j-1])
			can = np.vstack((can, b))
			lat[i,j-1] = x+2
			update_lat(lat, x)
	if (j < n-1):
		nn[4] = lat[i, j+1] #right 
		if  nn[4] == 1:
			b = np.array([i, j+1])
			can = np.vstack((can, b))
			lat[i,j+1] = x+2
			update_lat(lat, x)
	return(lat, can)
def update_lat(lat, color): ##add colors for each cluster
	one = random.randint(0,255)
	two = random.randint(0, 255)
	three = random.randint(0, 255)
	for i in range(0, n):
		for j in range(0, n):
			if lat[i,j] == color+2:
				pygame.draw.rect(screen,(one, two, three),[j*inc, i*inc,inc,inc])   
def find_root(lat,n): ##Find the next empty block
	root = np.zeros((1,2), int)
	for i in range (0, n):
		for j in range(0, n):
			if lat[i,j] == 1:
				root[0,0]= i
				root[0,1] = j
				return(root, True)
	else:
		return(root, False)
def percolation(lat,n): ##fill the cluster and check if the lattice percolates
	found = True
	color = 0
	perc = False
	while(True):
		can = np.zeros((1, 2), int)
		can, found = find_root(lat,n)
		if (found == False):
			break
		else:
			x=0
			while(x < len(can)): 
				lat, can= neighbors(can, lat, can[x,0], can[x,1],n, color)
				x+=1 
			color += 1	
	pygame.display.flip()
	##check horizontally for percolation
	for i in range (0, n-1):
		if (lat[i, 0] != 0 and np.in1d(lat[i, 0], lat[:, n-1] )):
			perc = True
	##check vertically for percolation
	for j in range (0, n-1):
		if (lat[0, j] != 0 and np.in1d(lat[0, j], lat[n-1, :])):
			perc = True
	return(perc)

	
#MAIN
#Single Run
screen_size = 500
inc = screen_size/n
screen = pygame.display.set_mode([screen_size, screen_size])
screen.fill((0,0,0))
pygame.display.flip()

lat = draw_lat()
perc = percolation(lat,n)
if perc == True:
	print "PERCOLATES"
else:
	print "DOES NOT PERCOLATE"
pygame.time.wait(4000)
pygame.image.save(screen, "latSample(n=30, p = 60).jpeg")
pygame.quit()








