from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.clock import mainthread, Clock
# from kivy.uix.behaviors import ButtonBehavior


import time
import threading


fps = 1000
dro = 1/fps



carousel_indicator_minopacity = 0.2
class CarouselIndicatorCircle(
			Image
			  ):
	def __init__(self, **kwargs):
		
		
		
		kwargs["source"] = "static/circle1.png"
		
		super().__init__(**kwargs)
		
		
		
		
		size = 0.1
		self.size_hint = (size,size)
		self.background_color = (1,0,1,1)
	
	@mainthread
	def select(self):
		# self.source = self.selected_img
		self.opacity = 1
		# pass
	@mainthread
	def unselect(self):
		# pass
		self.opacity = carousel_indicator_minopacity
		# self.source = self.unselected_img
	
	@mainthread
	def set_opacity(self,opac):
		self.opacity = opac
	

class CarouselMember(
	
				  Button
				  ):
	def __init__(self,**kwargs):
		surati = kwargs["surati"]
		del kwargs["surati"]
		kwargs["background_normal"] = surati
		kwargs["background_down"] = surati
		super().__init__(**kwargs)
		
		

		self.current_width = 1
		self.size_hint = (1,0.8)
		self.pos_hint = {"center_x" :  0.5,"y" : 0.2}

		self.narrowing = False
		
		self.bind(on_press=self.hover_start)
			
			
		self.bind(on_release=self.unhover)

		self.init_x_cord = None
		self.init_time = None
		


		
	def hover(self,instance,cords):

		
		x_cord = (  ( cords[0] - (self.parent.hold_startpos[0] - (self.parent.poshint_startpos)) ) / Window.size[0])
		if self.init_x_cord == None:
			self.init_x_cord = x_cord
		if self.init_time == None:
			self.init_time = time.time()
		self.current_x_cord = x_cord
		self.current_time = time.time()
		sxvaoba = x_cord - self.init_x_cord


		if self.parent.members.index(self) == 0:

			if x_cord > 0.5:
				self.pos_hint = {"x" : 0,"y" : 0.2}
				self.current_width = 1 + (x_cord - 0.5)/20
				self.size_hint = (self.current_width,0.8)
			else:
				self.current_width = 1
				self.pos_hint = {"center_x" : x_cord,"y" : 0.2}
				self.hover_for_others(x_cord) 
		elif self.parent.members.index(self) == len(self.parent.members) - 1:

			if x_cord < 0.5:
				self.current_width = 1 + (0.5 - x_cord )/20
				self.pos_hint = {"x" : 1 - self.current_width ,"y" : 0.2}
				
				self.size_hint = (self.current_width,0.8)
			else:
				self.current_width = 1
				self.pos_hint = {"center_x" : x_cord,"y" : 0.2}
				self.hover_for_others(x_cord) 
				
			
			
		else:
			self.pos_hint = {"center_x" : x_cord,"y" : 0.2}
			self.hover_for_others(x_cord)
			self.current_width = 1
			
			
	def hover_for_others(self,x_cord):

		for m in self.parent.members:
			if m != self:
				
				m.pos_hint = {"center_x" : x_cord + (self.parent.members.index(m) - self.parent.members.index(self)) ,"y" : 0.2}

	def hover_start(self,instance):
		
		if self.narrowing == True:
			self.pos_hint["center_x"] = 0.5

		self.parent.hold_startpos = self.last_touch.pos
		self.parent.poshint_startpos = Window.size[0] * self.pos_hint["center_x"]
		
		self.moving = False


		if ((self.parent.members.index(self) + 1) <= (len(self.parent.members) - 1)):
			self.parent.members[self.parent.members.index(self) + 1].moving = False
		
		if (self.parent.members.index(self) - 1) >= 0:
			self.parent.members[self.parent.members.index(self) - 1].moving = False
		
		
		Window.bind(mouse_pos=self.hover)

	def unhover(self,instance):
		Window.unbind(mouse_pos=self.hover)
		



		self.moving = True
		
		
		if ((self.parent.members.index(self) + 1) <= (len(self.parent.members) - 1)):
			
		
			self.parent.members[self.parent.members.index(self) + 1].moving = True
			


		
		if (self.parent.members.index(self) - 1) >= 0 and self.current_width == 1: 
			self.parent.members[self.parent.members.index(self) - 1].moving = True


			threading.Thread(target=self.chamoshveba).start()
		
		if ((self.parent.members.index(self) - 1) >= 0) == False:
			
			if self.current_width == 1:
				threading.Thread(target=self.chamoshveba).start()
			else:
				#stop
				self.narrowing = True

				
				widget_type = "first"
				
				threading.Thread(target=self.shrink,args=(widget_type,)).start()

		if ((self.parent.members.index(self) ) == (len(self.parent.members) - 1)):
			if self.current_width != 1:
				self.narrowing = True
				print("BLBLBLOBIANI")
				threading.Thread(target=self.shrink,args=("last",)).start()
			


	def shrink(self,widget_type="first"):
		
		# fps = 1000 
		# dro = 1/fps
		
		veloc = -0.0002
		
		accelerat = -(veloc**2) / (2* ( self.current_width- 1))
		while self.current_width > 1 and self.narrowing:
			self.current_width +=veloc
			
			self.size_hint = (self.current_width,0.8)
			if widget_type == "last":
				
				self.pos_hint = {"x" : 1 - self.current_width ,"y" : 0.2}
			time.sleep(dro)
		self.current_width= 1
		self.size_hint = (self.current_width,0.8)
		self.pos_hint["center_x"] = 0.5
		self.narrowing = False
		
		
	
		
	def chamoshveba(self):
		
		self.x_cord = self.pos_hint["center_x"]
		
		
		
		required_swipe_velocity = 1
		
		speed = 0.003



		
		acc = 0
		
		
		
		area = 0.1
		area = 0
		


		
		
		try:
			
			x_cord_distance_travelled = self.current_x_cord - self.init_x_cord
			x_cord_time_travelled = self.current_time - self.init_time
			swipe_velocity = (x_cord_distance_travelled) / (x_cord_time_travelled)
			self.init_time = None
			self.init_x_cord = None
			
			# print("swipe velocity :",swipe_velocity)
			
			if  (self.x_cord < -0 - area) or ( swipe_velocity < -required_swipe_velocity):
				
				if (2*(self.x_cord -(-0.5)) ) != 0:
					accelerat = -(speed**2)/(2*(self.x_cord -(-0.5)) )
					if self.parent.members.index(self) + 1 <= (len(self.parent.members) - 1):
						
						
						self.parent.current_widget = self.parent.members.index(self) + 2


						self.parent.binded_switch_func("right")





						# if self.parent.indicator != False:

						# 	temp_dro = 1
						# 	temp_xcord = self.x_cord
						# 	temp_speed = speed
							
						# 	while temp_xcord > -0.5:
						# 		temp_xcord += -temp_speed
						# 		temp_speed+=accelerat
						# 		temp_dro+=1

						# 	intervals = temp_dro * dro
						# 	self.parent.indicator.opchange_size =   (1-carousel_indicator_minopacity)/ (temp_dro)

						while self.x_cord > -0.5 and self.moving:
							self.pos_hint["center_x"] = self.x_cord
							self.hover_for_others(self.x_cord)
							self.x_cord+=-speed
							
							speed+=accelerat
							accelerat+=-acc
							# if self.parent.indicator != False:
							# 	self.parent.indicator.select_th(self.parent.current_widget)
							# 	self.parent.indicator.unselect_th(self.parent.current_widget -1)
								
							time.sleep(dro)
						if self.moving:
							self.x_cord = -0.5
							self.pos_hint["center_x"] = self.x_cord
							self.hover_for_others(self.x_cord)

							# if self.parent.indicator != False:
							# 	self.parent.indicator.select_th(self.parent.current_widget,custom=True)
							# 	self.parent.indicator.unselect_th(self.parent.current_widget -1,custom=True)
							
					else:
						# print("ZDOP")

						accelerat = -(speed**2)/(2*(self.x_cord -0.5) )
						self.parent.current_widget = self.parent.members.index(self) + 1
						self.parent.binded_switch_func("right")



						
						while self.x_cord > 0.5 and self.moving:
							self.pos_hint["center_x"] = self.x_cord
							self.hover_for_others(self.x_cord)
							self.x_cord+=-speed
							
							speed+=-(-accelerat)
							accelerat+=-acc
							
							time.sleep(dro)
						if self.moving:
							self.x_cord = 0.5
							
							self.pos_hint["center_x"] = self.x_cord
							self.hover_for_others(self.x_cord)

						
				
			elif (self.x_cord > 1 + area) or ( swipe_velocity > required_swipe_velocity) :
				
				
				if self.parent.members.index(self) - 1 >= 0:
					
					
					if (2*(1.5- self.x_cord ) ) != 0:
						accelerat = (speed**2)/(2*(1.5- self.x_cord ) )
						self.parent.current_widget = self.parent.members.index(self)
						self.parent.binded_switch_func("left")


						# if self.parent.indicator != False:

						# 	temp_dro = 1
						# 	temp_xcord = self.x_cord
						# 	temp_speed = speed
							
						# 	while temp_xcord > -0.5:
						# 		temp_xcord += -temp_speed
						# 		temp_speed+=accelerat
						# 		temp_dro+=1

						# 	intervals = temp_dro * dro
						# 	self.parent.indicator.opchange_size =   (1-carousel_indicator_minopacity)/ (temp_dro)


							
						while self.x_cord < 1.5 and self.moving:
							self.pos_hint["center_x"] = self.x_cord
							self.hover_for_others(self.x_cord)
							self.x_cord+=speed
							speed+=-accelerat
							

							# if self.parent.indicator != False:
							# 	self.parent.indicator.select_th(self.parent.current_widget)
							# 	self.parent.indicator.unselect_th(self.parent.current_widget + 1)
							
							time.sleep(dro)
							
						if self.moving:				
							self.x_cord = 1.5
							self.pos_hint["center_x"] = self.x_cord
							self.hover_for_others(self.x_cord)


							# if self.parent.indicator != False:
							# 	self.parent.indicator.select_th(self.parent.current_widget,custom=True)
							# 	self.parent.indicator.unselect_th(self.parent.current_widget + 1,custom=True)
						

				else:
					accelerat = -(speed**2)/(2*(self.x_cord -0.5) )
					self.parent.current_widget = self.parent.members.index(self) + 1
					self.parent.binded_switch_func("left")
					while self.x_cord < 0.5 and self.moving:
						self.pos_hint["center_x"] = self.x_cord
						self.hover_for_others(self.x_cord)
						self.x_cord+=speed
						
						speed+=-accelerat
						accelerat+=-acc
						
						time.sleep(dro)
					if self.moving:
						self.x_cord = 0.5
						
						self.pos_hint["center_x"] = self.x_cord
						self.hover_for_others(self.x_cord)


			else:
				# print("returnnn")
				if (2*(self.x_cord -0.5) ) != 0:
					accelerat = -(speed**2)/(2*(self.x_cord -0.5) )
					if self.x_cord > 0.5:
						# print("return from left")
						self.parent.current_widget = self.parent.members.index(self) + 1
						self.parent.binded_switch_func(None)
						while self.x_cord > 0.5 and self.moving:
							self.pos_hint["center_x"] = self.x_cord
							self.hover_for_others(self.x_cord)
							self.x_cord+=-speed
							
							speed+=-(-accelerat)
							accelerat+=-acc
							
							time.sleep(dro)
						if self.moving:
							self.x_cord = 0.5
							
							self.pos_hint["center_x"] = self.x_cord
							self.hover_for_others(self.x_cord)
							


					else:
						# print("returnnn from right")

						self.parent.current_widget = self.parent.members.index(self) + 1
						self.parent.binded_switch_func(None)
						while self.x_cord < 0.5 and self.moving:
							self.pos_hint["center_x"] = self.x_cord
							self.hover_for_others(self.x_cord)
							self.x_cord+=speed
							
							speed+=-accelerat
							accelerat+=-acc
							
							time.sleep(dro)
						if self.moving:
							self.x_cord = 0.5
							
							self.pos_hint["center_x"] = self.x_cord
							self.hover_for_others(self.x_cord)
							

							
			 
		
		except Exception as e:
			print(e)
			

class CarouselIndicator(FloatLayout):
	def __init__(self,carousel,**kwargs):
		super().__init__(**kwargs)
		self.carousel = carousel

		self.carousel.indicator = self
		

		carousel_members_len = len(self.carousel.members)
		carousel_members_len = 3
		area = 0.3
		self.circles = []
		for i in range(1, carousel_members_len+ 1):

			x_pos =  ((1 - area)/2  + ((area) / (carousel_members_len + 1) ) * i)
			self.circle = CarouselIndicatorCircle(pos_hint={"center_x" : x_pos,"center_y" : 0.5})
			self.circles.append(self.circle)
			self.add_widget(self.circle)
	
	@mainthread
	def select_th(self,index,custom=False):
		el = self.circles[index-1]
		# opincrease_size =  ( (1-carousel_indicator_minopacity)/ (shading / dro))
		# while self.circles[index-1].opacity <= 1:
		# 	time.sleep(dro)
		# 	# print("opacacacac",self.circles[index-1].opacity)
		
		if custom == False:
			self.circles[index-1].opacity += self.opchange_size
		else:
			self.circles[index-1].opacity = 1
	@mainthread
	def unselect_th(self,index,custom=False):
		el = self.circles[index-1]
		# opincrease_size =  ( (1-carousel_indicator_minopacity)/ (shading / dro))
		# while self.circles[index-1].opacity <= 1:
		# 	time.sleep(dro)
		# 	# print("opacacacac",self.circles[index-1].opacity)
		
		if custom == False:
			self.circles[index-1].opacity += -self.opchange_size
		else:
			self.circles[index-1].opacity = carousel_indicator_minopacity
	
		# 	self.circles[index-1].opacity += opincrease_size
		# self.circles[index-1].opacity = 1

	def switch_to(self,index,shading=False):

		if shading == False:
			for i in self.circles:
				i.unselect()
			
			self.circles[index-1].select()
		else:
			threading.Thread(target=self.select_th,args=(index,shading,)).start()
			# pass


class Carousel(FloatLayout):
	def __init__(self,members,**kwargs):
		super().__init__(**kwargs)
		self.current_widget = 1
		self.bind_switch_func(lambda : None)
		self.size_hint=(1,1)
		self.pos_hint = {"center_x" : 0.5,"y" : 0}
		self.members = members
		self.indicator = False
		
		
			
		for widget in self.members[::-1]:
			super().add_widget(widget)
			widget.parent = self
	def bind_switch_func(self,func):
		self.binded_switch_func = func

	