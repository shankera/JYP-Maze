#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import maze
import time
def main():
	f = open('benchmarking.txt', 'w')
	
	for x in range (280,281):
		start = time.clock()
		y = maze.print_maze(maze.make_maze(x,x),x,x)
		end = time.clock()
		f.write(str(end-start))
		f.write('\n')
		
		
main()