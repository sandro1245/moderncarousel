from kivy.uix.floatlayout import FloatLayout

class Carousel(FloatLayout):
	def __init__(self,carousel_size,members,**kwargs):
		super().__init__(**kwargs)
		self.current_widget = 1
		self.bind_switch_func(lambda direction: None)
		self.size_hint=(1,1)
		self.carousel_size = carousel_size
		# self.pos_hint = {"center_x" : 0.5,"y" : 0}
		self.members = members
		self.indicator = False
		
		
			
		for widget in self.members[::-1]:
			super().add_widget(widget)
			widget.parent = self
			widget.carousel_size = self.carousel_size
			widget.size_hint = widget.carousel_size
			widget.pos_hint = {"center_x" :  0.5,"y" : 1-self.carousel_size[1]}
	def bind_switch_func(self,func):
		self.binded_switch_func = func

	