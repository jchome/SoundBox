#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Dec 22, 2013

@author: julien CORON
'''


import kivy
kivy.require('1.0.5')

from kivy.lang import Builder
from kivy.adapters.listadapter import ListAdapter
from kivy.app import App
from kivy.config import Config

import glob
import os

from customscreen import CustomScreen, CustomScreenManager
from soundscreen import SoundScreenApp

# Samsung S4 : 1080x1920
#Config.set('graphics', 'width', '1080')
#Config.set('graphics', 'height', '1920')

Config.set('graphics', 'width', '450')
Config.set('graphics', 'height', '800')


__version__ = '0.2'
## install & run with 
# buildozer android debug deploy run

## see logs with
# adb logcat -s "python"

Builder.load_string("""
[CustomListItemCategories@SelectableView+BoxLayout]:
	orientation: 'horizontal'
	spacing: '10sp'
	padding: (sp(20), 0)
	size_hint_y: None
	height: '120sp'
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
		width: '107sp'
		selected_color: 1,1,1, 1
		deselected_color: 1,1,1, 1
		background_color: 1,1,1, 1
		background_normal: "images/"+ctx.text+".png"
		background_down: "images/"+ctx.text+".png"
		border: (0,0,0,0)
		
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
		font_size: '32sp'
		font_name: "fonts/bebas.ttf"
		
	ListItemButton:
		id: mainListItemButton
		size_hint_x: None
		width: '30sp'
		selected_color: 1,1,1, 1
		deselected_color: 1,1,1, 1
		background_color: 1,1,1, 1
		background_normal: "app-images/arrow.png"
		background_down: "app-images/arrow.png"
		border: (0,0,0,0)

""")

class BeepBoxScreen(CustomScreen):
	def __init__(self, **kwargs):
		super(BeepBoxScreen, self).__init__(**kwargs)
		self.update_display()
		

	def _read_categories(self):
		self._categories = []
		os.chdir("sounds")
		for filename in glob.glob("*"):
			self._categories.append(filename)
		os.chdir("..")
		self._categories.sort()
		
		
		
	def update_display(self):
		self._read_categories()
		#print(self._categories)
		list_item_args_converter = \
			lambda row_index, obj: {'text': obj,
									'index': row_index,
									'is_selected': False,
									'size_hint_y': None,
									'height': 25
									}
		
		my_adapter = ListAdapter(data = self._categories,
									args_converter=list_item_args_converter,
									selection_mode='single',
									allow_empty_selection=True,
									template='CustomListItemCategories')
		
		my_adapter.bind(on_selection_change=self.item_changed)
		self.containerListView.adapter = my_adapter
		
		
	def item_changed(self, adapter, *args):
		if len(adapter.selection) == 0:
			return
		objectSelected = adapter.data[adapter.selection[0].parent.index]
		adapter.selection[0].deselect()
		
		nextScreen = self.manager.go_next()
		nextScreen.set_categorie( objectSelected )
		
			
	def exit(self):
		self.stop_all()
		

class BeepBoxApp(App):
	def build(self):
		manager = CustomScreenManager()
		mainScreen = BeepBoxScreen(name="main")
		manager.add_screen(mainScreen)
		
		soundScreenApp = SoundScreenApp()
		soundScreenApp.load_kv()
		manager.add_screen(soundScreenApp.build())
		
		return manager

if __name__ == '__main__':
	BeepBoxApp().run()
	