import numpy as np
import galois
import multiprocessing
from joblib import Parallel, delayed
import random
import time
import csv


def process(i):
	return random.randint(-1*2**10 ,2**10)

def process1(i,x):
	return i*x




GF256 = galois.GF(2**8)
g  = 123
g = GF256(g)


times = []
for i in range(1001,2001):
	tot_time =0
	seperate_time = [0,0,0,0,0,0]
	for j in range(100):
		x= []
		y=[]
		z=0
		for k in range(i):
			x.append(random.randint(-1*2**10, 2**10))
			y.append(random.randint(-1*2**10, 2**10))
			z = z+ x[k]*y[k]
		time1 = time.perf_counter()

		time11 = time.perf_counter()
		random_num = Parallel(n_jobs=8)(delayed(process)(c) for c in range(2*i-1))

		#multiplying ai*yi
		sum =0
		mult_ay = Parallel(n_jobs=8)(delayed(process1)(y[c],random_num[c]) for c in range(i))
	
		for k in range(len(mult_ay)):
			sum+= -1*mult_ay[k]
		for k in range(i, 2*i-1):
			sum+= -1*random_num[k]
		
		random_num.append(sum)
		time2 = time.perf_counter()
		seperate_time[1] = seperate_time[1] + (time2 -time1)

		tow =[]
		T1 = []
		T2 = []
		T =[]
		
		time1 = time.perf_counter()
		for k in range(i):
			tow.append(g**(x[k]+random_num[k]))
		time2 = time.perf_counter()
		seperate_time[2] = seperate_time[2] + (time2 -time1)

		#for k in range(i):
		#	T1.append((tow[k]**y[k]))


		#for k in range(i):
		#	temp = (g**random_num[k+i])
		#	T2.append(temp)

		time1 = time.perf_counter()
		for k in range(i):
			T.append((tow[k]**y[k])*(g**random_num[k+i]))
		time2 = time.perf_counter()
		seperate_time[3] = seperate_time[3] + (time2 -time1)

		time1 = time.perf_counter()
		mul =1
		for k in range(len(T)):
			mul = mul*T[k]



		ans = (mul == g**z)

		time2 = time.perf_counter()
		seperate_time[4] = seperate_time[4] + (time2 -time1)
		time22 = time.perf_counter()
		seperate_time[5] = seperate_time[5] + (time22 -time11)
	seperate_time[0] = i
	seperate_time[1] = seperate_time[1]/100
	seperate_time[2] = seperate_time[2]/100
	seperate_time[3] = seperate_time[3]/100
	seperate_time[4] = seperate_time[4]/100
	seperate_time[5] = seperate_time[5]/100
	times.append(seperate_time)
	print(i)

fields =['Size','TA', 'C1', 'C2', 'Anyone','Total']
filename = '/home/naman/mp-spdz-0.2.4/verify_4.1.csv'
with open(filename, 'w') as csvfile: 
    # creating a csv writer object 
# creating a csv writer object 
    csvwriter = csv.writer(csvfile) 
        
    # writing the fields 
    csvwriter.writerow(fields) 
        
    # writing the data rows 
    csvwriter.writerows(times)



    


