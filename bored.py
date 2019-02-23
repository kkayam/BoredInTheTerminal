import os,msvcrt,sys
import numpy as np

if os.name == 'nt':
    import msvcrt
    import ctypes
    class _CursorInfo(ctypes.Structure):
        _fields_ = [("size", ctypes.c_int),
                    ("visible", ctypes.c_byte)]
def hide_cursor():
    if os.name == 'nt':
        ci = _CursorInfo()
        handle = ctypes.windll.kernel32.GetStdHandle(-11)
        ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
        ci.visible = False
        ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
    elif os.name == 'posix':
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()
hide_cursor()




class GameObject:
	def __init__(self,x = 0,y = 0):
		self.position = [x,y]
	def update(self):
		pass
	def render(self):
		pass
	def kill(self):
		o.all_objects.remove(self)

class player(GameObject):
	def __init__(self,x,y):
		super().__init__(x,y)
	def update(self):
		input_char = msvcrt.getch().decode()
		if input_char=='w':
			self.position[0]=clamp(self.position[0]-1,0,15)
		if input_char=='a':
			self.position[1]=clamp(self.position[1]-1,0,15)
		if input_char=='s':
			self.position[0]=clamp(self.position[0]+1,0,15)
		if input_char=='d':
			self.position[1]=clamp(self.position[1]+1,0,15)
		if input_char=='e':
			e = explosion(self.position[0],self.position[1])
			o.add(e)
		if input_char=='q':
			sys.exit()
	def render(self):
		r.render[self.position[0]][self.position[1]] = 'ö'

class explosion(GameObject):
	def __init__(self,x,y):
		super().__init__(x,y)
		self.time = 0
	def update(self):
		self.time +=1
		if self.time>4:
			self.kill()
	def render(self):
		for x in range(0,10):
			try:
				r.render[self.position[0]+round(np.int(np.cos(np.deg2rad(x*36))*self.time))][self.position[1]+round(np.int(np.sin(np.deg2rad(x*36))*self.time))] = '%'
			except:
				pass
			

class playfield(GameObject):
	def __init__(self):
		super().__init__(0,0)
	def render(self):
		r.render = [['-' for x in range(16)] for x in range(16)]

class renderer:
	def __init__(self):
		self.render = [['+' for x in range(16)] for x in range(16)]
	def printmenu(self):
		print("Play with wasd keys, e for explosion and q to quit")
	def print(self):
		os.system('cls')
		for row in self.render:
			print(" ".join(row))
		self.printmenu()

class objects:
	def __init__(self):
		self.all_objects = []
	def update(self):
		for object in self.all_objects:
			object.update()
			if not self.insidescreen(object.position):
				object.kill()
	def render(self):
		for object in self.all_objects:
			object.render()
	def insidescreen(self,position):
		if position[0]>15 or position[0]<0 or position[1]>15 or position[1]<0:
			return False
		return True
	def add(self,object):
		self.all_objects.append(object)

def clamp(x,min_value,max_value):
	if x<min_value:
		return min_value
	if x>max_value:
		return max_value
	return x

pf = playfield()
o = objects()
r = renderer()
player = player(2,2)

o.add(pf)
o.add(player)

while (True):
	r.print()
	o.update()
	o.render()