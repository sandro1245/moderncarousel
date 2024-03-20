
from kivy.uix.floatlayout import FloatLayout
from moderncarousel.carouselindicatorcircle import CarouselIndicatorCircle
from kivy.clock import mainthread

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
			# self.circle = CarouselIndicatorCircle(pos_hint={"center_x" : x_pos,"center_y" : 0.5})
			

			if ("center_y" in kwargs["pos_hint"]):
				circle_poshint = {"center_x" : x_pos,"center_y" : 0.5}
			elif ("y" in kwargs["pos_hint"]):
				circle_poshint = {"center_x" : x_pos,"y" : 0}
			
			
			
			self.circle = CarouselIndicatorCircle(pos_hint=circle_poshint)
			
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