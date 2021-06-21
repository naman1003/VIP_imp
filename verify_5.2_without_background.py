import numpy as np
import multiprocessing
from joblib import Parallel, delayed
import random
import time 
import os
import csv
import sys

mod = 7649
g_inv =[]
g_inv.append(0)


def mul(g, i, mod):
	return (g*i)%mod

def get_inverse(g, mod):
	for i in range(mod):
		if(mul(g,i,mod) == 1):
			return i

for i in range(1,mod):
	g_inv.append(get_inverse(i,mod))


g  = 23




def power(g,a,mod, g_inv):
	if(g==0):
		return 0
	if(a == 0):
		return 1
	if(a>0):
		return (g**a)%mod
	else:
		return power(g_inv[g], abs(a), mod, g_inv)



def get_factors(x):
	y =[]
	x = abs(x)
	for i in range(1, x + 1):
		if x % i == 0:
			y.append(i)
			y.append(-1*i)
	return y  


def process1(i):
	return random.randint(-1*2**10 ,2**10)

def process2(i):
	global mod
	return random.randint(1,mod-1)

def process3(x,i,j):
	global g_inv
	global mod
	j = power(j,-1,mod,g_inv)

	return mul(i,j,mod)


def process4( k, x, y):
	global mod
	global g_inv
	global g
	part1 = power(g, x, mod, g_inv)
	return power(part1, y, mod, g_inv)

def process5(k, x, y, r):
	global mod
	global g_inv
	global g
	part1 = power(g, y, mod, g_inv)
	part2 = power(part1, x, mod, g_inv)
	return power(part2, r, mod, g_inv)


times = []

data = []

i = 320

while(i<=512):


	publish_tow =0
	publish_T = 0

	seperate_data = [0, 0, 0, 0, 0]
	seperate_time = [0,0,0,0,0,0,0,0,0]
	for j in range(100):
		z=0
		x_input = Parallel(n_jobs=8)(delayed(process1)(c) for c in range(i))
		y_input = Parallel(n_jobs=8)(delayed(process1)(c) for c in range(i))
		#for k in range(i):
		#	z = z+ x_input[k]*y_input[k]

	
		z1 = random.randint(-1*2**10 ,2**10)
		z2 = random.randint(-1*2**10 ,2**10)
		z3 = z - z1 - z2

		z_server1 = [z1, z2]
		z_server2 = [z2, z3]
		z_server3 = [z3, z1]


		with open('i.txt', 'w') as f:
			f.write(str(i))

		time11 = time.perf_counter()
		time1 = time.perf_counter()
		#c = random.randint(-mod ,mod)
		
		





		#random setup
		random1 = random.randint(-1*2**10 ,2**10)
		random2 = random.randint(-1*2**10 ,2**10)
		random3 = random.randint(-1*2**10 ,2**10)

		server1_random =[random1, random2]
		server2_random = [random2, random3]
		server3_random = [random3, random1]
		time2 = time.perf_counter()
		seperate_time[1] = seperate_time[1] + (time2 -time1)


		time1 = time.perf_counter()
		# random reconstruct
		r = server1_random[0] + server1_random[1] + server3_random[0]
		time2 = time.perf_counter()
		seperate_time[2] = seperate_time[2] + (time2 -time1)



		
		#factors = get_factors(c)
		time1 = time.perf_counter()
		alpha = Parallel(n_jobs=8)(delayed(process2)(p) for p in range(i))
		b0 = random.randint(1,mod-1)
		c = mul(alpha[0],b0,mod)
		beta = Parallel(n_jobs=8)(delayed(process3)(x,c,alpha[x]) for x in range(i))
		with open('c.txt', 'w') as f:
			f.write(str(power(g,c,mod,g_inv)))
		time2 = time.perf_counter()
		seperate_time[3] = seperate_time[3] + (time2 -time1)




		time1 = time.perf_counter()
		#g_raised_to_alpha = []
		#for k in range(i):
		#	g_raised_to_alpha.append(power(g,alpha[k],mod, g_inv))

		#print(x_input)
		#print(alpha)

		tow = Parallel(n_jobs=8)(delayed(process4)(k, alpha[k],x_input[k]) for k in range(i))

		publish_tow = publish_tow + sys.getsizeof(tow)

		#for k in range(i):
		#	tow.append(power(g_raised_to_alpha[k],x[k],mod, g_inv))
		time2 = time.perf_counter()
		seperate_time[4] = seperate_time[4] + (time2 -time1)
		time1 = time.perf_counter()
		#print("here1")
		#g_raised_to_beta = []
		#for k in range(i):
		#	g_raised_to_beta.append(power(g,beta[k],mod, g_inv))



		#T =[]
		#for k in range(i):
		#	T.append(power(g_raised_to_beta[k],y[k], mod, g_inv))
		#print(i)
		#print(beta)
		#print(y_input)
		T = Parallel(n_jobs=8)(delayed(process5)(val, beta[val], y_input[val],r) for val in range(i))
		publish_T = publish_T + sys.getsizeof(T)

		#print("here2")
		time2 = time.perf_counter()
		seperate_time[5] = seperate_time[5] + (time2 -time1)

		time1 = time.perf_counter()
		#partial eval part 2

		v_server1 = [(server1_random[0]*z_server1[0])%mod, (server1_random[1]*z_server1[1])%mod]
		v_server2 = [(server2_random[0]*z_server2[0])%mod, (server2_random[1]*z_server2[1])%mod]
		v_server3 = [(server3_random[0]*z_server3[0])%mod, (server3_random[1]*z_server3[1])%mod]

		v_server1_final = [power(g,v_server1[0], mod, g_inv), power(g, v_server1[1], mod, g_inv)]
		v_server2_final = [power(g,v_server2[0], mod, g_inv), power(g, v_server2[1], mod, g_inv)]
		v_server3_final = [power(g,v_server3[0], mod, g_inv), power(g, v_server3[1], mod, g_inv)]

		time2 = time.perf_counter()
		seperate_time[6] = seperate_time[6] + (time2 -time1)


		with open('T.txt', 'w') as f:
			for x in T:
				f.write(str(x))
				f.write('\n')

		with open('tow.txt', 'w') as f:
			for x in tow:
				f.write(str(x))
				f.write('\n')


		time1 = time.perf_counter()
		part1 = mul(v_server1_final[0], v_server1_final[1], mod)
		part2 = mul(part1, v_server2_final[1], mod)
		with open('z.txt', 'w') as f:
			f.write(str(part2))




		#time1 = time.perf_counter()

		os.system("./foo")
		time2 = time.perf_counter()
		seperate_time[7] = seperate_time[7] + (time2 -time1)

		time22 = time.perf_counter()
		seperate_time[8] = seperate_time[8] + (time22 -time11)

	seperate_time[0] = i
	seperate_time[1] = seperate_time[1]/100
	seperate_time[2] = seperate_time[2]/100
	seperate_time[3] = seperate_time[3]/100
	seperate_time[4] = seperate_time[4]/100
	seperate_time[5] = seperate_time[5]/100
	seperate_time[6] = seperate_time[6]/100
	seperate_time[7] = seperate_time[7]/100
	seperate_time[8] = seperate_time[8]/100
	times.append(seperate_time)

	print(i)
	i = i+64



fields =['Size','Random setup', 'Random Reconstruct','TA', 'C1', 'C2', 'Patrial Eval part 2 ', 'Anyone','Total']
field = ['Size', 'Data sent by C1 while sharing shares of x', 'Data sent by C2 while sharing shares of y', 'Data sent while publishing tow', 'Data sent while publishing T']
filename = 'verify_4.2.csv'
with open(filename, 'w') as csvfile: 
    # creating a csv writer object 
# creating a csv writer object 
	csvwriter = csv.writer(csvfile) 
        
    # writing the fields 
	csvwriter.writerow(fields) 
        
    # writing the data rows 
	csvwriter.writerows(times)


			


		
		

		







		







