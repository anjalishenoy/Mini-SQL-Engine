#!/usr/bin/python

def where_parser(str):
	"WHERE validation"

	#Multiple where statements handled in from_parser
	query = str[1].strip().split("WHERE")

	if len(query)>2:
		#Implies there are multiple where
		return False,""

	whereQuery = []
	if len(query)==2:
		#If where exists then take where query
		whereQuery = query[len(query)-1].strip().split()
		whereQuery =[x.strip() for x in whereQuery]
	return True, whereQuery	#Edit
