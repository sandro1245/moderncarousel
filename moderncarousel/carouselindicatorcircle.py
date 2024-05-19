from kivy.uix.image import Image
from kivy.clock import mainthread
from moderncarousel.vars import *

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
	