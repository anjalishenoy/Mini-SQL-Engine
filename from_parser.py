#!/usr/bin/python

def from_parser(str):
	"FROM query validation"
	"str here is split from FROM part of command"

	#Divides into FROM part and WHERE part
	query = str[1].strip().split("WHERE")	

	if ',' not in query[0] and len(query[0].strip().split(" "))>1:
		#"from A B" without comma is invalid
		return False,""
	fromQuery = query[0].strip().split(",")
	

	if len(fromQuery)>2 or '' in fromQuery:
		#from A,B,C not allowed
		#Empty from not allowed
		return False,""
	
	fromQuery = [x.strip() for x in fromQuery]

	return True, fromQuery