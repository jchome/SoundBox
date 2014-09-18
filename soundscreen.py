#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Dec 22, 2013

@author: julien CORON
'''


import kivy
from kivy.app import App
kivy.require('1.0.5')

from kivy.lang import Builder
from kivy.adapters.listadapter import ListAdapter
from kivy.config import Config
from kivy.core.audio import SoundLoader
from kivy.properties import StringProperty
from kivy.clock import Clock


import glob
import os


from customscreen import CustomScreen

# Samsung S4 : 1080x1920
#Config.set('graphics', 'width', '1080')
#Config.set('graphics', 'height', '1920')

Config.set('graphics', 'width', '450')
Config.set('graphics', 'height', '800')


__version__ = '0.1'
## install & run with 
# buildozer android debug deploy run

## see logs with
# adb logcat -s "python"

#a faire: 
#- animation lorsque ca joue
#- nettoyage dans le dossier

Builder.load_string("""
[CustomListItemSound@SelectableView+BoxLayout]:
	orientation: 'horizontal'
	spacing: '10sp'
	padding: (sp(20), 0)
	size_hint_y: None
	height: '75sp'
	index: ctx.index
	canvas.after:
		Color:
			rgb: 0.5,0.5,0.5
		Line:
			rectangle: self.x,self.y+self.height,self.width,0
	
	
	# icon of item
	ListItemButton:
		id: mainListItemButton
		size_hint_x: None
		width: '75sp'
		selected_color: 1,1,1, 1
		deselected_color: 1,1,1, 1
		background_color: 1,1,1, 1
		background_normal: "app-images/play-button.png"
		background_down: "app-images/play-button.png"
		
	ListItemButton:
		selected_color: 0,0,1, 0
		deselected_color: 1,1,1, 0
		background_color: 1,1,1, 0
		background_normal: ""
		background_down: ""
		
		halign: 'left'
		text_size: (self.width , None)
		color: [1,1,1, 1]
		text: ctx.text
		markup: True
		font_size: '22sp'
		font_name: "fonts/segoe_ui_light.ttf"
		

""")

class SoundScreen(CustomScreen):
	EMPTY_ICON = "app-images/play-button.png"
	
	ANIMATION_FILES = ["app-images/animation/01.png",
					"app-images/animation/02.png",
					"app-images/animation/03.png",
					"app-images/animation/04.png",
					"app-images/animation/05.png"]
	
	current_index_animation = 0
	
	id = None
	audio = None
	text = StringProperty("")
	icon = StringProperty(EMPTY_ICON)
	
	def __init__(self, **kwargs):
		super(SoundScreen, self).__init__(**kwargs)
		self._categorie = None
		

	def set_categorie(self, aCategorie):
		self._categorie = aCategorie
		self.update_display()
		
	def update_display(self):
		self._sounds = []
		if self._categorie is None:
			return
		self.title_button.text = "Sound Box / " + self._categorie
		
		os.chdir("sounds")
		os.chdir(self._categorie)
		for aFilename in glob.glob("*"):
			self._sounds.append(aFilename[:-4])
		os.chdir("../..")
		
		list_item_args_converter = \
			lambda row_index, obj: {'text': obj,
									'index': row_index,
									'is_selected': False
									}
		
		my_adapter = ListAdapter(data = self._sounds,
									args_converter=list_item_args_converter,
									selection_mode='single',
									allow_empty_selection=True,
									template='CustomListItemSound')
		
		my_adapter.bind(on_selection_change=self.item_changed)
		self.containerListView.adapter = my_adapter
		
	def item_changed(self, adapter, *args):
		if len(adapter.selection) == 0:
			return
		objectSelected = adapter.data[adapter.selection[0].parent.index]
		adapter.selection[0].deselect()
		
		self.audio = SoundLoader.load("sounds/"+self._categorie+"/"+objectSelected+".mp3")
		self.play()

	def play(self):
		try:
			self.audio.stop()
		except:
			pass
		self.current_index_animation = 0
		Clock.schedule_once(self._play_audio, 0)
		self.start_animation()

	def _play_audio(self, dt):
		self.audio.play()
		self.audio.bind(on_stop = self.stop)
		self.display_stop_button()
		
		
	def stop(self,  arg = None):
		try:
			self.audio.unbind(on_stop = self.stop)
			self.audio.stop()
		except:
			pass
		self.hide_stop_button()
		self.stop_animation()

	def display_stop_button(self):
		self.icon = "app-images/stop-button.png"
	
	def hide_stop_button(self):
		self.icon = self.EMPTY_ICON
		
	def start_animation(self):
		Clock.schedule_interval(self.change_image, 0.1)
		
	def stop_animation(self):
		Clock.unschedule(self.change_image)
		self.corner_button.icon = ""
		
	def change_image(self, dt):
		self.corner_button.icon = self.ANIMATION_FILES[self.current_index_animation]
		self.current_index_animation += 1
		
		if self.current_index_animation >= len(self.ANIMATION_FILES):
			self.current_index_animation = 0
	
	def pre_back(self):
		self.stop()
		return super(SoundScreen, self).pre_back()
	
	
class SoundScreenApp(App):
	def build(self):
		return SoundScreen(name="sound")
	