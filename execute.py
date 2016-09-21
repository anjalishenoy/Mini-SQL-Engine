#!/usr/bin/python
from table_class import *
from helper import *
from extract_where import *
from extract_select import *

def execute(cmd):
	"EXECUTE the sql command"
	"0--> Successful 1-->Error in fromQuery  2-->error in selectQuery   3--->error in whereQuery"
	selectQuery = cmd[0]
	fromQuery = cmd[1]
	whereQuery = cmd[2]

	#Get the tables as objects
	table = getDB()
	result,X,Y = validateTablename(fromQuery, table)

	if result == False:
		return 1	#Errror in some table name
	L=[]
	for q in fromQuery:
		for t in table:
			if q == t.name:
				L.append(t)	#list of required tables

	#Get cartesian product
	joinTable = join(X,Y)
	
	#extract from the table using where condition
	result,joinTable = extract_where(joinTable, whereQuery,fromQuery,L)
	
	if result == False:
		return 3	#Errror in some where query
	
	result, finalTable = extract_select(joinTable, selectQuery, fromQuery,L);

	if result == False:
		return 2	#Errror in some select query

	printTable(finalTable,selectQuery)
	return 0