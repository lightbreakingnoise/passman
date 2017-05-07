import colorama
import json
import random
import sys
import os
import struct
import time
import tarfile

colorama.init()

def generate(num):
	txt = ""
	for i in range(num):
		txt += "1qayxsw23edcvfr45tgbnhz67ujmki89olp0PLOIKMJUZHNBGTRFVCDEWSXYAQ"[random.SystemRandom().randint(0, 62)]
	
	return txt

def output(lnum, txt):
	otxt = "\033[" + ("%d" % lnum) + ";1H" + txt + "\033[0K"
	sys.stdout.write(otxt)
	ret = (lnum + 1) % 31
	return ret

os.system("mode con cols=140 lines=35")

sys.stdout.write("\033[2J\033[1;1H")

y = 1
new_pass = ""
pass_list = []
master = []

while True:
	sys.stdout.write("\033[33;1H\033[2K>")
	i = input().lower().split(" ")
	
	if i[0] == "generate" and len(i) == 1:
		new_pass = generate(10)
		y = output(y, "Your Password> " + new_pass)
	
	elif i[0] == "generate" and len(i) == 2:
		try:
			x = int(i[1])
		except:
			x = 10
		
		new_pass = generate(x)
		y = output(y, "Your Password> " + new_pass)
	
	elif i[0] == "add" and len(i) == 2:
		sys.stdout.write("\033[33;1H\033[2K>>>")
		xtra = input()
		pass_list.append({"account": i[1], "pass": new_pass, "xtra": xtra})
	
	elif i[0] == "list" and len(i) == 1:
		for e in pass_list:
			y = output(y, e["account"] + " :: " + e["xtra"] + " >> " + e["pass"])

	elif i[0] == "load" and len(i) == 2:
		sys.stdout.write("\033[33;1H\033[2K>>>")
		m = input()
		ltxt = m.encode()
		cryptxt = ("%d" % len(m)) + "B"
		master = struct.unpack(cryptxt, ltxt)
		
		try:
			f = open(i[1] + ".crjson", "rb")
		except:
			continue
		
		intxt = f.read()
		f.close()
		cryptxt = ("%d" % len(intxt)) + "B"
		incrypt = struct.unpack(cryptxt, intxt)
		
		outxt = b""
		x = 0
		for n in range(len(incrypt)):
			c = int(incrypt[n])
			b = int(master[x])
			a = (256 + (c - b)) % 256
			outxt += struct.pack("B", a)
			x = (x + 1) % len(master)
		
		try:
			pass_list = json.loads(outxt.decode("utf-8"))
			y = output(y, "loading OK!")
		except:
			y = output(y, "loading FAILED!")
	
	elif i[0] == "help":
		y = output(y, "first, you have to ::generate:: or ::load file:: then you can ::add account:: or ::list:: and ::save file:: and ::exit::")
		
	elif i[0] == "exit" and len(i) == 1:
		break

	elif i[0] == "save" and len(i) == 2:
		sys.stdout.write("\033[33;1H\033[2K>>>")
		m = input()
		ltxt = m.encode()
		cryptxt = ("%d" % len(m)) + "B"
		master = struct.unpack(cryptxt, ltxt)

		x = 0
		intxt = json.dumps(pass_list).encode()
		outxt = b""
		cryptxt = ("%d" % len(intxt)) + "B"
		incrypt = struct.unpack(cryptxt, intxt)

		for n in range(len(incrypt)):
			a = int(incrypt[n])
			b = int(master[x])
			c = (a + b) % 256
			outxt += struct.pack("B", c)
			x = (x + 1) % len(master)

		f = open(i[1] + ".crjson", "wb")
		f.write(outxt)
		f.close()

tname = "Backup " + time.asctime() + ".tar.xz"
tname = tname.replace(" ", "_")
tname = tname.replace(":", "_")

t = tarfile.open(tname, "w:xz")
for f in os.listdir("."):
	if f[-7:] == ".crjson":
		t.add(f)
t.close()

