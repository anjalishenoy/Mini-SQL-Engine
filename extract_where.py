#!/usr/bin/python
from helper import *

def extract_where(joinTable, whereQuery,fromQuery):

	if whereQuery == []:
		#No where condition
		return True,joinTable

	condition,task = getCondition(whereQuery)

	if len(task)>2:
		#if number of conditions are > 2
		return False,[]

	#String to operator
	ops = { '<': operator.lt, '<=': operator.le, '=':operator.eq, '<>':operator.ne, '>=':operator.ge, '>':operator.gt }	
	hash = getHash(fromQuery)
	
	if len(task)==1:
		#single condition
		result, table=singleCondiiton(task, hash, ops, joinTable)
		
	else:
		#Condition with AND / OR
		result,table= doubleCondition(task,hash,ops,joinTable,condition)

	if result == False:
		return False,[]
	else:
		return True, table

	return True, joinTable

