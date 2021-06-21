import subprocess
import csv
from decimal import Decimal


def run_command(command):
    p = subprocess.Popen(command,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    return iter(p.stdout.readline, b'')



def ret_int(s):
	x ="0"
	y = ""
	for i in range(len(s)):
		if(s[i] == 'e'):
			x = s[i+1:len(s)]
			break
		y = y + s[i]
	return Decimal(y)*10**Decimal(x)






times = []

for i in range(32):
	times.append(0)

for y in range(100):
	command = 'Scripts/brain.sh dot_prod_timing'.split()
	i =0
	j =0
	sum =0
	for line in run_command(command):
	    line = line.decode('UTF-8')
	    #print(line)
	    x = line.split()
	    if(x[0] == "sbitvec(20)" ):
	    	continue
	    #if(x[0] == "Running" ):
	    #	continue
	    if(i>5):
	    	if(i%2 ==0):
	    		if(x[0]  == "Time"):
	    			break
	    		#print(line)
	    		time1 = ret_int(x[4])
	    		#print(time1)
	    	else :
	    		#print(line)
	    		time2 = ret_int(x[-1])
	    		#print(time2 - time1)
	    		times[j] = times[j] + (time2 - time1)
	    		if(j== 31):
	    			break
	    		else :
	    			j = j+1
	    i+=1
	print(y)


for i in range(32):
	times[i] = times[i]/100
print(times[31])

filename = '/home/naman/mp-spdz-0.2.4/dot_pr_time.csv'
with open(filename, 'w') as csvfile: 
    # creating a csv writer object 
    csvwriter = csv.writer(csvfile) 
    csvwriter.writerow(times) 


