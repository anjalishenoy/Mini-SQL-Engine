#!/usr/bin/python
from helper import *
import sys
def extract_select(joinTable, selectQuery, fromQuery,L):
	l=['MAX', 'MIN', 'SUM', 'AVERAGE','DISTINCT','max','min','sum','average','distinct']
	flag=0
	m={}	#Map
	finalTable=[]
	tempTable=[]
	N=0;	#length of table

	if '*' in selectQuery:
		return True,joinTable

 	for func in l:
		for str in selectQuery:
			if func in str:
				#to check if any function is used
				flag=1
				break

	hash = getHash(fromQuery,L)
	if flag==0:
		#No call to functions
		index=[]
		for str in selectQuery:
			if str in hash:
				#Getting indices of columns
				index.append(hash[str])
			else:
				return False, ''

		finalTable = [[each_list[i] for i in index] for each_list in joinTable]

	elif flag==1:
		
		#Mapping column to the operation they hold, if no operation then map to column number
		for i in range(len(selectQuery)):
			flag=0
			for j in range(len(l)):
				if l[j] in selectQuery[i]:
					m[selectQuery[i]]=l[j]
					flag=1
			if flag==0:
				#No function applied
				return False,[]
		
		#Getting required columns from select query
		col=[]
		operation=[]
		for x in selectQuery:
			if isinstance(m[x], basestring):	#If some operation has to be done		
				op=x.split(')')
				if len(op)!=2:
					#Braces not balanced
					return False,[]
				if '' not in op:
					# ) has chars attached
					return False,[]

				op=op[0].split('(')
				if len(op)!=2:
					#Braces not balanced
					return False,[]

				if op[1] not in hash:
					#Retrieved column not in table
					return False,[]
				col.append(hash[op[1]])
				operation.append(op[0])
			else:
				return False,''

		for row in joinTable:

			temp=[]
			for j in col:
				temp.append(row[j])
			#Getting the requred columns
			tempTable.append(temp)

		#Operating on columns
		sumArr=[0]*len(col)
		distinctArr=[{}]*len(col)	#creating dictionary for 
		maxArr=[tempTable[0][0]]*len(col)	#initialise with [intmin intmin..]
		minArr=[tempTable[0][0]]*len(col)		#initialise with [intmax intmax.. ]

		for row in tempTable:
			for i in range(len(row)):
				element=row[i]
				distinctArr[i][element]='a'
				sumArr[i]=sumArr[i]+int(element)
				maxArr[i]=max(maxArr[i],int(element))
				minArr[i]=min(minArr[i],int(element))

		N=sum(1 for x in tempTable)

		for i in range(len(operation)):
			if operation[i] in ['SUM','sum']:
				finalTable.append(sumArr[i])
			elif operation[i] in ['AVERAGE','average']:
				finalTable.append(sumArr[i]/N)
			elif operation[i] in ['MAX', 'max']:
				finalTable.append(maxArr[i])
			elif operation[i] in ['MIN', 'min']:
				finalTable.append(minArr[i])
			elif operation[i] in ['DISTINCT', 'distinct']:
				finalTable=list(distinctArr[i].keys())

	return True, finalTable



