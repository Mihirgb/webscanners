import argparse
import os
import csv
import threading
from urllib.request import urlopen
import time

parser=argparse.ArgumentParser(description="Bulk Clickjacking Scanner")
parser.add_argument("-f","--file",required=True,help="Enter file name which contains list of urls")
parser.add_argument("-o","--output",required=True,help="Output file name")
args=parser.parse_args()

count=0
vulncount=0
print(args.file)
print(args.output)

if(os.path.isfile(args.file)):
	print("[*] Input File Exist")
else:
	print("Input file Doesn't exist")
	raise SystemExit

try:
	fileo=open(args.output,"w")
	print("[*] Successfully Created Output File")
except:
	print("[-]Unable to create output file")
	raise SystemExit


listfinal=[]
filei=open(args.file, "r")
while True:
    temp=filei.readline()
    if temp=="":
        break
    else:
        listfinal.append(temp)
print("[*] Successfully added {} urls in list".format(len(listfinal)))


#Main Algo Part
listoutput=[]
def checkcj(url):
	global listoutput
	global fileo
	global count
	global args
	global vulncount
	try:
		data=urlopen(url)
		if data.getcode()==200:
			headers=data.info()
			if not "X-Frame-Options" in headers:
				listoutput.append(url)
				print("[*] ClickJacking found on {}".format(url))
				count=count+1
				vulncount=vulncount+1

	except:
		count=count+1
		pass




thread=[]

for i in range(0,len(listfinal)):
	temp=listfinal[i]
	if (("https" in temp) or ("http" in temp)):
		t1=threading.Thread(target=checkcj,args=(temp,))
		thread.append(t1)
		t1.start()
	else:
		temp1="https://"+temp
		t1=threading.Thread(target=checkcj,args=(temp1,))
		thread.append(t1)
		t1.start()
		temp1="https://"+temp
		t2=threading.Thread(target=checkcj,args=(temp1,))
		thread.append(t2)
		t2.start()



time.sleep(15)
try:
	while(True or count!=len(listfinal)):
		print("Total count {}/{}".format(count,len(listfinal)))
		time.sleep(2)
	print("Total Clickjacking vulnerable site are = {}".format(vulncount))
	print("[*] Wait for a while to save the output file")
	for i in listoutput:
		fileo.write(i)
	fileo.close()
	print("---Good Bye---")
	raise SystemExit
except KeyboardInterrupt:
	print("Total Clickjacking vulnerable site are = {}".format(vulncount))
	print("[*] Wait for a while to save the output file")
	for i in listoutput:
		fileo.write(i)
	fileo.close()
print("---Good Bye---")
raise SystemExit