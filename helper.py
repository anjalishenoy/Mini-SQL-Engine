#!/usr/bin/python
import fnmatch
import os
from table_class import *
import operator
import csv
import re
def getDB():
	"Get the database into a list"

	table_list=[]
	
	f = open('data/metadata.txt', 'r')
	flag=0
	buf=f.readline().strip()
	while buf != '':
		if buf=="<begin_table>":
			name=f.readline().strip()
			attr=[]	#Attributes of table
			buf=f.readline().strip()

			#attribute list
			while buf !="<end_table>":
				attr.append(buf)
				buf=f.readline().strip()

			for file in os.listdir('data'):
				if fnmatch.fnmatch(file, name+'.csv'):
					break
			file='data/'+file
			table=[]
			with open(file, 'rb') as csvfile:
				content = csv.reader(csvfile, delimiter=',')
				for row in content:
					table.append(row)

			table_list.append(Table(name,attr,table))

		buf=f.readline().strip()

	return table_list


#----------------------------------------------------------------

def validateTablename(fromQuery, table):
	"Check for errors in table name"
	X=[]
	Y=[]
	flagX=0
	flagY=0
	for q in fromQuery:
		found=0
		for t in table:
			if q == t.name:
				found=1
				if flagX==0:
					flagX=1
					X=t.table
				elif flagY==0:
					flagY=1
					Y=t.table
				else:
					#More than 3 tables
					return False,"",""
		if found==0:
			return False,"",""

	return True,X,Y

#----------------------------------------------------------------

def join(X,Y):
	"Create cartesian Product"
	joinTable = []
	for row1 in X:
		if Y != []:		
			#Two tables given in fromQuery
			for row2 in Y:
				joinTable.append(row1+row2)
		else:	
			#Only 1 table in query
			joinTable.append(row1)
	return joinTable

#-----------------------------------------------------------------

def getHash(fromQuery,L,selectQuery):
	"Return how to index table elements"

	i=0
	dict={}
	for t in L:
		for attr in t.attr:
			dict[t.name+'.'+attr]=i;
			i=i+1

	i=0;
	#if len(L)==1:
	#	for attr in L[0].attr:
	#		dict[attr]=i;
	#		i=i+1;

	attr1=L[0].attr;
	if len(L)>1:
		attr2=L[1].attr;

	new_dict=dict;
	for a in attr1:
		for b in attr2:
			if a == b:
				return dict;
				#found same column names
			else:
				new_dict[a]=i;
				new_dict[b]=i+len(attr);

	return new_dict

#------------------------------------------------------------------------

def getCondition(whereQuery):
	"Get the conditions in where and parse it"
	condition = ''
	if 'AND' in whereQuery:
		index = whereQuery.index('AND')
		condition = 'and'
	elif 'OR' in whereQuery:
		index = whereQuery.index('OR')
		condition = 'or'
	else:
		index = -1

	if condition!='':
		n=len(whereQuery)
		q1 = ''.join(whereQuery[0:index])
		q2 = ''.join(whereQuery[index+1:n])
		q = [q1, q2]	#QUERY
	else:
		q = ''.join(whereQuery)
		q = [q]

	return condition, q

#--------------------------------------------------------------------------
def printTable(table, query):
	for q in query:
		print q,
	print ""
	for row in table:
		if isinstance(row,list):
			for element in row:
				print element,
			print ""
		else:
			print row


#------------------------------------------------
def singleCondiiton(task, hash, ops,joinTable):
	"If single condiiton in where"

	symb=['=','<>','>','<','>=','<=']
	op=''
	for s in symb:
		if s in task[0]:
			op=s;
			task=task[0].split(op)
	
	if op=='':
		#No operator found, invalid cond
		return False,[]


	table=[]
	for row in joinTable:
		if task[0] in hash:
			i=hash[task[0]];
		else:
			#Invalid column name
			return False,[]
		if task[1] in hash:
			j=hash[task[1]]
			#Either it's a col name or a number
			if ops[op](int(row[i]),int(row[j])):
				table.append(row)
		else:
			if re.search('[a-zA-Z]', task[1]):
				#found letters, A>Ab99-hash not allowed
				return False,[]
			else:
				j=task[1]
			#Either it's a col name or a number
			if ops[op](int(row[i]),int(j)):
				table.append(row)
	return True, table

#--------------------------------------------------

def doubleCondition(task,hash,ops,joinTable,condition):
	print task
	h={'and'}
	symb=['=','<>','>','<','>=','<=']
	op1=''
	op2=''
	for s in symb:
		if s in task[0]:
			op1=s;
			p,q=task[0].split(op1)
		if s in task[1]:
			op2=s
			r,z=task[1].split(op2)
	
	if op1=='' or op2=='':
		#No operator found, invalid cond
		return False,[]

	table=[]
	for row in joinTable:
		if p in hash and r in hash:
			i1=row[hash[p]]
			i3=row[hash[r]]
		else:
			return False,[]

		if q in hash:
			i2 = row[hash[q]]
		elif re.search('[a-zA-Z]', q):
			#found letters, A>Ab99-hash not allowed
			return False,[]
		else:
			#it's a number
			i2=int(q)

		if z in hash:
			i4 = row[hash[z]]
		elif re.search('[a-zA-Z]', z):
			return False,[]
		else:
			i4=int(z)


		val1=ops[op1](int(i1),int(i2))
		val2=ops[op2](int(i3),int(i4))
		if condition=='and':
			if val1 and val2:
				table.append(row)
		elif condition=='or':
			if val1 or val2:
				table.append(row)

	return True, table