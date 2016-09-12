#!/usr/bin/python

from parser import *
from execute import *

if __name__ == "__main__":

	hash=["Successful Query", "Error in FROM query", "Error in SELECT query", "Error in WHERE query"]
	cmd=""
	while 1:
		cmd = raw_input(">")
		
		if cmd =="quit" or cmd=="q":
			break
		
		result,parsed_cmd = validater_parser(cmd)
		if result ==False:
			print "Syntax error"
			continue
		
		#we have the syntactically parsed commands, now execute it
		sig = execute(parsed_cmd)
		print hash[sig]


print "Goodbye!"