from time import sleep
import pyautogui
pyautogui.PAUSE = 1
pyautogui.FAILSAFE = False


def distance(s,e):
	return ((s['x']-e['x'])**2+(s['y']-e['y'])**2)**0.5

speed = 200

start_point = {}
start_point['x'] , start_point['y'] = ( 31 , 13 )

end_point = {}
end_point['x'] , end_point['y'] = ( 0 , 0 )

window_size = {}
window_size['x'] , window_size['y'] = pyautogui.size()
window_size['x'] , window_size['y'] = window_size['x'] , window_size['y'] - 100
print('Window Details',window_size)

# Line equation ay = bx + c
left_side = {}
left_side['a'] , left_side['b'] , left_side['c'] = ( 0 , 1 , 0  )

right_side = {}
right_side['a'] , right_side['b'] , right_side['c'] = ( 0 , 1 , - window_size['x'] )

top_side = {}
top_side['a'] , top_side['b'] , top_side['c'] = ( 1 , 0 , 0 )

bottom_side = {}
bottom_side['a'] , bottom_side['b'] , bottom_side['c'] = ( 1 , 0 ,  window_size['y'] )

print('------------------------------------------------')
print("Sides , eq : ay = bx + c")
print('------------------------------------------------')
print("Left   {}y={}x+{}".format(left_side['a'],left_side['b'],left_side['c']))
print("Right  {}y={}x+{}".format(right_side['a'],right_side['b'],right_side['c']))
print("Top    {}y={}x+{}".format(top_side['a'],top_side['b'],top_side['c']))
print("Bottom {}y={}x+{}".format(bottom_side['a'],bottom_side['b'],bottom_side['c']))
print('------------------------------------------------')

direction = {}
direction['x'] , direction['y'] = ( 1 , 1 )

def PI(p,l):

	try:
		x1 = (-l['a']*(p['y']-p['x']) + l['c']) / (l['a']-l['b'])
	except ZeroDivisionError:
		x1 = None

	if x1 != None:
		y1 = x1 + (p['y']-p['x'])
		

	try:
		x2 = (l['a']*(p['y']+p['x']) - l['c']) / (l['a']+l['b'])
	except ZeroDivisionError:
		x2 = None

	if x2 != None:
		y2 = - x2 + (p['y']+p['x'])

	if None in (x1,x2):
		raise Exception('Cannot compute PI for parallel lines')

	return {'x':x1,'y':y1} , {'x':x2,'y':y2}


def chooseP(ps):
	global window_size

	p , q = ps[0] , ps[1]
	
	if 0 <= p['x'] <= window_size['x'] and 0 <= p['y'] <= window_size['y']:
		return p
	elif 0 <= q['x'] <= window_size['x'] and 0 <= q['y'] <= window_size['y']:
		return q

	return {}

def move(prev_direction,curr_postion):
	global right_side,left_side,top_side,bottom_side,window_size

	points = []

	if prev_direction['x'] == 1 :
		right_ps  = PI(curr_postion,right_side)
		right_p = chooseP(right_ps)
		points += [right_p]
	elif prev_direction['x'] == -1 :
		left_ps   = PI(curr_postion,left_side)
		left_p = chooseP(left_ps)
		points += [left_p]
	else:
		raise Exception('Wrong x direction')

	if prev_direction['y'] == -1 :
		top_ps  = PI(curr_postion,bottom_side)
		top_p = chooseP(top_ps)
		points += [top_p]
	elif prev_direction['y'] == 1 :
		bottom_ps   = PI(curr_postion,top_side)
		bottom_p = chooseP(bottom_ps)
		points += [bottom_p]
	else:
		raise Exception('Wrong y direction')

	try:
		points.remove({})
	except ValueError:
		pass

	for i in range(len(points)):
		points[i]['x'] = int(points[i]['x'])
		points[i]['y'] = int(points[i]['y'])

	update_direction = lambda p : { 'x': prev_direction['x'] if p['x'] not in (0,window_size['x']) else -1*prev_direction['x'] ,
									'y': prev_direction['y'] if p['y'] not in (0,window_size['y']) else -1*prev_direction['y'] }
	'''
	print('------------------------------------------------')
	print(PI(curr_postion,left_side))
	print(PI(curr_postion,right_side))
	print(PI(curr_postion,top_side))
	print(PI(curr_postion,bottom_side))
	print(points)
	print('------------------------------------------------')
	'''

	if len(points) == 1 :
		return points[0] , update_direction(points[0])

	if points[0] == curr_postion :
		return points[1] , update_direction(points[1])

	return points[0] , update_direction(points[0])

'''
print({'x': -1, 'y': 1},{'x': 1260, 'y': 0})
move({'x': -1, 'y': 1},{'x': 1260, 'y': 0})

exit()
'''
############################################################################
pyautogui.moveTo( start_point['x'] , start_point['y'] , duration = 1)

while True:
	#print('------------------------------------------------')
	#print('Direction :',direction)
	end_point , direction = move(direction,start_point)
	#print("Start : {} ; End :{} ; Updated Direction {}".format(start_point,end_point,direction))
	#print('------------------------------------------------')
	pyautogui.moveTo( end_point['x'] , end_point['y'] , duration = distance(start_point,end_point)/speed)
	start_point = end_point
