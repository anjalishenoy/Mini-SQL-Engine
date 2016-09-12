#!/usr/bin/python

def select_parser(str):
	"SELECT query validation"
	query = str[0].strip().split(" ",1)	#Only 1st space is split
	query[1]=query[1].strip()

	if query[0] != "SELECT":
		#1. Doesnt start with select, invalid syntax
		return False, ""	
	if len(query)<=1:
		#only "select" no following column name;
		return False,""
	if "*" in query[1] and len(query[1])>1:	
		#2. "select *,abc or select * abd" not allowed
		return False,""
	#elif len(query[1].split(" "))>1 and "," not in query[1]:
		#3. select abc pqr not allowed
	#	return False,""

	selectQuery = query[1].strip().split(",");
	
	if '' in selectQuery:
		#4. for queries of type "select abc, pwr, from abd;"
		return False,""
	selectQuery = [x.strip().replace(" ","") for x in selectQuery]
	
	return True, selectQuery
