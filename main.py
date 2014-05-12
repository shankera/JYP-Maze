#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  main.py
#  
#  Copyright 2013 Arjun <Arjun@HYPERION>
#
from character import Character
from character import Compass
from obstacle import Landmark
from obstacle import Wall
from item import Location
import maze
import random
import array
import sys

def main():
	try:
		print("Type 'help' for a list of commands!")
		valid = True
		
		#Generates player at default location facing north
		you = Character(Location(1,1), Compass(2))		
		try:
			var = raw_input("Would you like to use the default size? (Y/N): ")
		except NameError:
			var = input("Would you like to use the default size? (Y/N): ")
		if var == "y" or var == "Y":
			width = 50
			height = 40
		else:
			try:
				width = raw_input("Enter Width: ")
				height = raw_input("Enter Height: ")
			except NameError:
				width = input("Enter Width: ")
				height = input("Enter Height: ")
				
		obs = generateObstacles(width, height)			#벽들 창조해
		landmarks = generateLandmarks(width, height)		#랜그마크  객체들 창조해
		for x in range(len(landmarks)-1):
			for y in range(len(landmarks[x])-1):
				obs[x][y] = landmarks[x][y]
		
		while valid:
			try:
				var = raw_input("What would you like to do? : ")
			except NameError:
				var = input("What would you like to do? : ")
				
			command = var.split(' ')
			if command[0] == 'quit':
				valid = False
			
			#이것이 이벤트 기능 리스트이다		
			events = dict()
			events['quit'] = doQuit
			events['turn'] = doTurn
			events['move'] = doMove
			events['walk'] = doMove
			events['loc'] = doLoc
			events['compass'] = doCompass
			events['look'] = doLook
			events['help'] = doHelp
			
			validCommand = False
			
			#event loop checks input for keys in list
			for key in events:
				if command[0] == key:
					doThis = events[key]
					valid = doThis(you, obs, *command)
					validCommand = True
			
			if not validCommand:
				print("You can't do that right now.")
			
			if you.compass.direction < 0:	#changes dir to valid value
				you.compass.direction += 4
			elif you.compass.direction > 3:
				you.compass.direction -= 4
				
	except KeyboardInterrupt:
		print("\nQuitting")

def doLoc(you, *extras):
	print(you.loc)
	return True

#creates landmark objects based on the location values collected
#from the data.py file
def generateLandmarks(w, h):
	#find the size that the maze matrix needs to be since it doesn't contain
    #walls, but connections.
	
    width = int(w)
    height = int(h)
    x = maze.print_maze(maze.make_maze(width,height),width,height)
    return x

#creates walls between the predetermined boundaries
def generateObstacles(w, h):
	width = int(w)
	height = int(h)
	obs = [[0 for x in range(height + 1)] for x in range(width + 1)] 
	for x in range (0, width):
		obs[x][0] = 'wall'	
		obs[x][height] = 'wall'
	for y in range(0, height):
		obs[0][y] = 'wall'
		obs[width][y] = 'wall'
	return obs

#prints lines from help file 
def doHelp(*extras):
	f = open('help.txt')
	lines = f.readlines()
	f.close
	for l in lines:
		print(l.rstrip("\n"))
	
	return True

#prints out objects in adjacent locations
def doLook(you, obs, command, *extras):
	direction = 0
	#there is something after look
	encountered = 0
	if len(extras) > 0:
		#if told to look left
		if extras[0] == 'left':	
			direction = 1
			#North
			if you.compass.direction == 0:
				if obs[you.loc.x-1][you.loc.y] != '':
					encountered = obs[you.loc.x-1][you.loc.y]
			#East
			elif you.compass.direction == 1:
				if obs[you.loc.x][you.loc.y-1] != '':
					encountered = obs[you.loc.x][you.loc.y-1]
			#South
			elif you.compass.direction == 2:
				if obs[you.loc.x+1][you.loc.y] != '':
					encountered = obs[you.loc.x+1][you.loc.y]
			#West
			elif you.compass.direction == 3:
				if obs[you.loc.x][you.loc.y+1] != '':
					encountered = obs[you.loc.x][you.loc.y+1]	
		#if told to look left	
		elif extras[0] == 'right':
			direction = 2
			#North
			if you.compass.direction == 0:
				if obs[you.loc.x+1][you.loc.y] != '':
					encountered = obs[you.loc.x+1][you.loc.y]
			#East
			elif you.compass.direction == 1:
				if obs[you.loc.x][you.loc.y+1] != '':
					encountered = obs[you.loc.x][you.loc.y+1]
			#South
			elif you.compass.direction == 2:
				if obs[you.loc.x-1][you.loc.y] != '':
					encountered = obs[you.loc.x-1][you.loc.y]
			#West
			elif you.compass.direction == 3:
				if obs[you.loc.x][you.loc.y-1] != '':
					encountered = obs[you.loc.x][you.loc.y-1]	
	else:
		direction = 3
		#North
		if you.compass.direction == 0:
			if obs[you.loc.x][you.loc.y-1] != '':
				encountered = obs[you.loc.x][you.loc.y-1]
		#East
		elif you.compass.direction == 1:
			if obs[you.loc.x+1][you.loc.y] != '':
				encountered = obs[you.loc.x+1][you.loc.y]
		#South
		elif you.compass.direction == 2:
			if obs[you.loc.x][you.loc.y+1] != '':
				encountered = obs[you.loc.x][you.loc.y+1]
		#West
		elif you.compass.direction == 3:
			if obs[you.loc.x-1][you.loc.y] != '':
				encountered = obs[you.loc.x-1][you.loc.y]
	
	if encountered != 0:
		if direction == 1:
			print("There is a",encountered,"to the left of you.")
		elif direction == 2:
			print("There is a",encountered,"to the right of you.")
		else:
			print("There is a",encountered,"in front of you.")
	else:
		if direction == 1:
			print("There is nothing to the left of you.")
		elif direction == 2:
			print("There is nothing to the right of you.")
		else:
			print("There is nothing in front of you.")
		
	return True
			
def doQuit(*extras):
	return False
	
def doTurn(you, obs, command, *extras):
	if len(extras) == 0:
		print("You must specify a direction.")
	elif extras[0]== 'left':
		you.compass.direction -= 1
	elif extras[0] == 'right':
		you.compass.direction += 1
	elif extras[0] == 'around':
		you.compass.direction += 2
	else:
		print("You can't turn that way.")
	return True

def doMove(you, obs, *command):
	x = 1
	try:
		if len(command) >2:
			if command[2] != '':
				#value of move distance
				x = int(command[2])
	except ValueError:
		x = 0
	if x == 0:
		print("Invalid move distance")
		
	if x > 0:
		canMove = True
	else:
		canMove = False
		
	counter = 0
	
	#moves forward in increments of 1
	while canMove:
		counter += 1
		
		validLoc = 0
		if len(command) >1:
			if command[1] != "forward":
				validLoc = 3
				x = 0
		else:
			validLoc = 3
			x = 0
			
		#creates a location object based on the compass, one spot away
		#North
		if you.compass.direction == 0:
			newloc = Location(you.loc.x, you.loc.y - 1)
		#East
		elif you.compass.direction == 1:
			newloc = Location(you.loc.x + 1, you.loc.y)
		#South
		elif you.compass.direction == 2:
			newloc = Location(you.loc.x, you.loc.y + 1)
		#West
		elif you.compass.direction == 3:
			newloc = Location(you.loc.x - 1, you.loc.y)
	
		if obs[newloc.x][newloc.y] != 0 and obs[newloc.x][newloc.y] != "" :
			encountered = obs[newloc.x][newloc.y]
			if x > 1:
				validLoc = 2
			else:
				validLoc = 1
				
			canMove = False
				
		if counter == x+1:
			canMove = False
		if canMove:
			you.loc = newloc
	
	if validLoc == 2 :
		print("You walked %d and encountered a %s" % (counter-1, encountered))
	
	elif validLoc == 1:
		print("There is a %s in your way" % (encountered))
	elif validLoc == 3:
		print("You must specify a direction! Only forward works!")
	
	return True
	
def doCompass(you, *extras):
	print("You are facing " + str(you.compass) + ".")
	return True

main()

