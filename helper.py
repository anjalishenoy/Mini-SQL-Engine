#!/usr/bin/python
import operator
import csv
import re
def getDB():
	"Get the database into a list"
	table1=[]
	with open('data/table1.csv', 'rb') as csvfile:
		content = csv.reader(csvfile, delimiter=',')
		for row in content:
			table1.append(row)

	table2=[]
	with open('data/table2.csv', 'rb') as csvfile:
		content = csv.reader(csvfile, delimiter=',')
		for row in content:
			table2.append(row)

	return table1, table2


#----------------------------------------------------------------

def validateTablename(fromQuery, table1, table2):
	"Check for errors in table name"
	X=[]
	Y=[]
	if fromQuery[0] == 'table1':
		X = table1;
		if len(fromQuery)>1:
			if fromQuery[1] == 'table2':
				Y = table2;
			elif fromQuery[1] == 'table1':
				Y = table1
			else:
				return False,"","" 	#Error in table2 name
	elif fromQuery[0] == 'table2':
		X = table2;
		if len(fromQuery)>1:
			if fromQuery[1] == 'table1' :
				Y = table1
			elif fromQuery[1] == 'table2':
				Y = table2
			else:
				return False,"",""
	else:
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

def getHash(fromQuery):
	"Return how to index table elements"

	table1_hash = {'table1.A':0, 'table1.B':1, 'table1.C':2, 'A':0, 'B':1, 'C':2}		#If only table1 in fromQuery
	table2_hash = {'table2.A':0, 'table2.B':1, 'A':0, 'B':1}							#If only table2 in fromQuery
	join12_hash = {'table1.A':0, 'table1.B':1, 'table1.C':2,'table2.A':3, 'table2.B':4}	#If table1,table2
	join21_hash = {'table2.A':0, 'table2.B':1, 'table1.A':2,'table1.B':3, 'table1.C':4}	#If table2, table1

	if fromQuery[0] == 'table1' and len(fromQuery)==1:
		return table1_hash
	elif fromQuery[0] == 'table2' and len(fromQuery)==1:
		return table2_hash
	elif fromQuery[0] == 'table1' and len(fromQuery)==2:
		return join12_hash
	elif fromQuery[0] == 'table2' and len(fromQuery)==2:
		return join21_hash

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
	print query
	for row in table:
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

		if z in hash:
			i4 = hash[z]
		elif re.search('[a-zA-Z]', z):
			#found letters, A>Ab99-hash not allowed
			return False,[]
		else:
			i4=int(z)

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