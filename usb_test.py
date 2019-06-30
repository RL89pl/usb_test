#!/usr/bin/env/python3

import time, os, sys
import usb.core
import pyudev

def writetofile(filename,mysizeMB):
	# writes string to specified file repeatdely, until mysizeMB is reached. Then deletes fle 
	mystring = "The quick brown fox jumps over the lazy dog"
	writeloops = int(1000000*mysizeMB/len(mystring))
	try:
		f = open(filename, 'w')
	except:
		# no better idea than:
		raise
	for x in range(0, writeloops):
		f.write(mystring)
	f.close()
	os.remove(filename)

############## 

def diskspeedmeasure(dirname):
	# returns writing speed to dirname in MB/s
	# method: keep writing a file, until 0.5 seconds is passed. Then divide bytes written by time passed
	filesize = 1	# in MB
	maxtime = 0.5 	# in sec
	filename = os.path.join(dirname,'outputTESTING.txt')
	start = time.time()
	loopcounter = 0
	while True:
		try:
			writetofile(filename, filesize)
		except:
			# I have no better idea than:
			raise	
		loopcounter += 1
		diff = time.time() - start
		if diff > maxtime: break
	return (loopcounter*filesize)/diff

############## Start of main


if __name__ == "__main__":
	time.sleep(3)
	context = pyudev.Context()
	monitor = pyudev.Monitor.from_netlink(context)
	monitor.filter_by(subsystem='usb')
	for device in iter(monitor.poll, None):
		time.sleep(3)
		if device.action == 'add':
			# print("----------------------------------------")
			# print('{} podlaczone'.format(device))
			# print("----------------------------------------")
			dev = usb.core.find()
			idVendor = hex(dev.idVendor)
			idProduct = hex(dev.idProduct)
			# print(idVendor)
			# print(idProduct)
			time.sleep(3)
			os.system("sudo mount /dev/sda1 /media/usb")
			print("***********")
			print("Rozpoczecie")
			print("***********")


			dirname = "/media/usb"

			try:
				speed = diskspeedmeasure(dirname)
				print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
				print("Predkosc zapisu na dysku: %.2f Mb na sekunde" % speed)
				print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
			except IOError as e:
				if e.errno == 13:
					print("************************************************************************")
					print("Problem zapisu na dysku. Prawdopodobnie uszkodzone USB")
					print("************************************************************************")
			except:
				print("************************")
				print("Cos poszlo nie tak")
				print("************************")
				raise
			os.system("sudo umount /media/usb")
			print("***********************************************")
			print("Zakonczone")
			print("***********************************************")


#lsblk
