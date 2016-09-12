#!/usr/bin/python
import sqlparse
from select_parser import *
from from_parser import *
from where_parser import *

def validater_parser(cmd):

	#to check for ; at end of query
	n=len(cmd)
	if n==0:
		#empty string
		return False,""

	if cmd[n-1] != ";":
		return False,""
	cmd=cmd.strip(';')
	cmd=sqlparse.format(cmd, keyword_case='upper')
	cmd = cmd.encode('UTF8')	#Unicode to list conversion, as cmd was previously unicode

	#Split from middle first
	str = cmd.strip().split("FROM")

	if len(str) <= 1:
		#After splitting with FROM there are less than 2 entries(only select, no from)	(or only from no select)
		return False,""

	#SELECT QUERY VALIDATION-----------------------------------------------
	result, selectQuery = select_parser(str)
	if result==False:
		return False,""

	#FROM QUERY VALIDATION-------------------------------------------------
	result, fromQuery = from_parser(str)
	if result==False:
		return False,""

	#WHERE QUERY VALIDATION------------------------------------------------
	result, whereQuery = where_parser(str)
	if result==False:
		return False,""
	
	cmd = []
	cmd = [selectQuery, fromQuery, whereQuery]

	return True, cmd
