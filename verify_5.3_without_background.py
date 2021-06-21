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

def process4(x, y):
	global g_inv
	global g
	global mod
	return power(g, y, mod, g_inv)

def process5(x, y):
	global g
	global g_inv
	global mod
	coeffs = []
	coeffs.append(random.randint(-1*2**10 ,2**10))
	coeffs.append(y)
	shares = []
	shares.append(power(g,coeffs[0]*1 + coeffs[1], mod, g_inv))
	shares.append(power(g,coeffs[0]*2 + coeffs[1], mod, g_inv))
	shares.append(power(g,coeffs[0]*3 + coeffs[1], mod, g_inv))
	return shares

def process6(x, shares_X, shares_Y):
	global mod
	return mul(shares_X[0],shares_Y[0],mod)

def process7(x, shares_X, shares_Y):
	global mod
	return mul(shares_X[1],shares_Y[1],mod)

def process8(x, shares_X, shares_Y):
	global mod
	return mul(shares_X[2],shares_Y[2],mod)

def process9(x, server1, server2):
	global mod
	global g_inv
	server1 = power(server1, 2, mod, g_inv)
	server2 = power(server2, -1, mod, g_inv)
	return mul(server1, server2, mod)

def process10(x, a, b):
	return (a*b)
def process11(x, val):
	shares =[]
	shares.append(random.randint(-1*2**10 ,2**10))
	shares.append(random.randint(-1*2**10 ,2**10))
	shares.append(val-(shares[0]+ shares[1]))
	return shares

def process12(i, x, a):
	e=[]
	e.append(x[0]-a[0])
	e.append(x[1]-a[1])
	e.append(x[2]-a[2])
	return e

def process13(i, x):
	return (x[0]+x[1]+x[2])

def process14(k, f, a, e, b, c):
	return(f*a[0] + e*b[0] + c[0])

def process15(k, f, a, e, b, c):
	return(f*a[1] + e*b[1] + c[1])

def process16(k, f, a, e, b, c):
	return(f*a[2] + e*b[2] + c[2] + e*f)

def process17(x, a,b):
	global mod
	global g_inv
	return(power(a,b,mod, g_inv))

def process18( k, x, y):
	global mod
	global g_inv
	global g
	part1 = power(g, x, mod, g_inv)
	return power(part1, y, mod, g_inv)


times = []
data = []
fields = ["size", "ShareGen1", "ShareGen2", "Generating Randomness","ProofGen1","ProofGen2", "PartialEval","Generation of additive shares", "VIP reconstruct", "verify", "Total Time" ]
field = ['size', 'Client 1 sends x shares to three servers', 'Client 2 sends y shares to three servers', 'Client 1 publishes tow', 'Client 2 publishes T' ]
i =512
while(i<=512):
		seperate_time = [0,0, 0, 0, 0, 0, 0, 0,0,0,0]
		seperate_data = [0,0,0,0,0]
		for j in range(100):
			z=0
			X = Parallel(n_jobs=8)(delayed(process1)(c) for c in range(i))
			Y = Parallel(n_jobs=8)(delayed(process1)(c) for c in range(i))

			x_input = Parallel(n_jobs=8)(delayed(process4)(c, X[c]) for c in range(i))
			y_input = Parallel(n_jobs=8)(delayed(process4)(c, Y[c]) for c in range(i))
			#for k in range(i):
				#z = z+ x[k]*y[k]
			#print((x[0]*y[0])%mod)

			#z = z%mod
			#ShareGen
			time11 = time.perf_counter()
			time1 = time.perf_counter()
			X_mult_shares = Parallel(n_jobs=8)(delayed(process5)(c, X[c]) for c in range(i))
			time2 = time.perf_counter()
			seperate_time[1] = seperate_time[1] + (time2 -time1)

			time1 = time.perf_counter()
			Y_mult_shares = Parallel(n_jobs=8)(delayed(process5)(c, Y[c]) for c in range(i))
			time2 = time.perf_counter()
			seperate_time[2] = seperate_time[2] + (time2 -time1)



			#ProofGen
			time1 = time.perf_counter()
			alpha = Parallel(n_jobs=8)(delayed(process2)(p) for p in range(i))
			b0 = random.randint(1,mod-1)
			c = mul(alpha[0],b0,mod)
			with open('c.txt', 'w') as f:
				f.write(str(power(g,c,mod,g_inv)))
			beta = Parallel(n_jobs=8)(delayed(process3)(x,c,alpha[x]) for x in range(i))
			time2 = time.perf_counter()
			seperate_time[3] = seperate_time[3] + (time2 -time1)

			time1 = time.perf_counter()
			tow = Parallel(n_jobs=8)(delayed(process18)(k, alpha[k],x_input[k]) for k in range(i))
			with open('tow.txt', 'w') as f:
				for x in tow:
					f.write(str(x))
					f.write('\n')

			time2 = time.perf_counter()
			seperate_time[4] = seperate_time[4] + (time2 -time1)



	
			time1 = time.perf_counter()

			T = Parallel(n_jobs=8)(delayed(process18)(val, beta[val], y_input[val]) for val in range(i))



			with open('T.txt', 'w') as f:
				for x in T:
					f.write(str(x))
					f.write('\n')
			time2 = time.perf_counter()
			seperate_time[5] = seperate_time[5] + (time2 -time1)




			#PartialEval
			time1 = time.perf_counter()
			server1 = Parallel(n_jobs=8)(delayed(process6)(c, X_mult_shares[c], Y_mult_shares[c]) for c in range(i))
			server2 = Parallel(n_jobs=8)(delayed(process7)(c, X_mult_shares[c], Y_mult_shares[c]) for c in range(i))
			server3 = Parallel(n_jobs=8)(delayed(process8)(c, X_mult_shares[c], Y_mult_shares[c]) for c in range(i))
			time2 = time.perf_counter()
			seperate_time[6] = seperate_time[6] + (time2 -time1)

			#step2
			#mult_reconstrcuted = Parallel(n_jobs=8)(delayed(process9)(c, server1[c], server2[c]) for c in range(i))

			#partialeval additive

			time1 = time.perf_counter()
			server1_exp = Parallel(n_jobs=8)(delayed(process17)(c, server1[c], 2) for c in range(i))
			server2_exp = Parallel(n_jobs=8)(delayed(process17)(c, server2[c], -1) for c in range(i))

			
			a = Parallel(n_jobs=8)(delayed(process1)(c) for c in range(i))
			b = Parallel(n_jobs=8)(delayed(process1)(c) for c in range(i))

			c =  Parallel(n_jobs=8)(delayed(process10)(k, a[k], b[k]) for k in range(i))

			a_shares = Parallel(n_jobs=8)(delayed(process11)(k, a[k]) for k in range(i))
			b_shares = Parallel(n_jobs=8)(delayed(process11)(k, b[k]) for k in range(i))
			c_shares = Parallel(n_jobs=8)(delayed(process11)(k, c[k]) for k in range(i))

			mult_1_shares =  Parallel(n_jobs=8)(delayed(process11)(k, server1_exp[k]) for k in range(i))
			mult_2_shares =  Parallel(n_jobs=8)(delayed(process11)(k, server2_exp[k]) for k in range(i))



			e_shares = Parallel(n_jobs=8)(delayed(process12)(k, mult_1_shares[k],a_shares[k]) for k in range(i))
			f_shares =  Parallel(n_jobs=8)(delayed(process12)(k, mult_2_shares[k],b_shares[k]) for k in range(i))



			e = Parallel(n_jobs=8)(delayed(process13)(k, e_shares[k]) for k in range(i))
			f = Parallel(n_jobs=8)(delayed(process13)(k, f_shares[k]) for k in range(i))

			z_server_1 = Parallel(n_jobs=8)(delayed(process14)(k, f[k], a_shares[k], e[k], b_shares[k], c_shares[k]) for k in range(i))
			z_server_2 = Parallel(n_jobs=8)(delayed(process15)(k, f[k], a_shares[k], e[k], b_shares[k], c_shares[k]) for k in range(i))
			z_server_3 = Parallel(n_jobs=8)(delayed(process16)(k, f[k], a_shares[k], e[k], b_shares[k], c_shares[k]) for k in range(i))

			inn_share_1 =0
			inn_share_2 =0
			inn_share_3 =0
			for k in range(i):
				inn_share_1 = inn_share_1 + z_server_1[k]
				inn_share_2 = inn_share_2 + z_server_2[k]
				inn_share_3 = inn_share_3 + z_server_3[k]

			time2 = time.perf_counter()
			seperate_time[7] = seperate_time[7] + (time2 -time1)

			#vip reconstruct
			time1 = time.perf_counter()
			z_out = inn_share_3+ inn_share_2 + inn_share_1
			z_out = z_out%mod
			#print(z)
			#print(z_out)

			#print(z== z_out)
			time2 = time.perf_counter()
			seperate_time[8] = seperate_time[8] + (time2 -time1)

			with open('z.txt', 'w') as f:
				f.write(str(power(g,z_out,mod, g_inv)))
			with open('i.txt', 'w') as f:
				f.write(str(i))

			#verify
			time1 = time.perf_counter()
			os.system("./foo")
			time2 = time.perf_counter()
			seperate_time[9] = seperate_time[9] + (time2 -time1)
			time22 = time.perf_counter()
			seperate_time[10] = seperate_time[10] + (time22 -time11)

		seperate_time[0] = i
		seperate_time[1] = seperate_time[1]/100
		seperate_time[2] = seperate_time[2]/100
		seperate_time[3] = seperate_time[3]/100
		seperate_time[4] = seperate_time[4]/100
		seperate_time[5] = seperate_time[5]/100
		seperate_time[6] = seperate_time[6]/100
		seperate_time[7] = seperate_time[7]/100
		seperate_time[8] = seperate_time[8]/100
		seperate_time[9] = seperate_time[9]/100
		seperate_time[10] = seperate_time[10]/100
		times.append(seperate_time)


		print(i)
		i= i+64


filename = 'verify_4.3.csv'
with open(filename, 'w') as csvfile: 
    # creating a csv writer object 
# creating a csv writer object 
	csvwriter = csv.writer(csvfile) 
        
    # writing the fields 
	csvwriter.writerow(fields) 
        
    # writing the data rows 
	csvwriter.writerows(times)


