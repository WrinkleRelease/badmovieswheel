import xbmc
import xbmcgui
import xbmcaddon
import math
import time
import os

class MovieWheel(xbmcgui.WindowDialog):
    def __init__(self):
        super().__init__()
        self.width = 1920
        self.height = 1080
        self.center_x = self.width // 2
        self.center_y = self.height // 2
        self.wheel_radius = 800
        
        # Define arrow dimensions
        self.arrow_width = 197
        self.arrow_height = 106
        
        #------------------------
        ## MARK: Background Image
        #-------------------------
        addon = xbmcaddon.Addon()
        self.addon_path = addon.getAddonInfo('path')
        
        background_image = os.path.join(self.addon_path, 'resources', 'media', 'background.png')
        self.background = xbmcgui.ControlImage(0, 0, self.width, self.height, background_image)
        self.addControl(self.background)
        
        #-----------------
        ## MARK: Add Arrow
        #-----------------
        arrow_image = os.path.join(self.addon_path, 'resources', 'media', 'arrow.png')
        arrow_x = self.center_x - (self.arrow_width // 2)
        arrow_y = self.center_y - self.wheel_radius - self.arrow_height
        
        self.arrow = xbmcgui.ControlImage (
            arrow_x,
            arrow_y,
            self.arrow_width,
            self.arrow_height,
            arrow_image
        )
        self.addControl(self.arrow)
        
    #--------------------
    ## MARK: Create Wheel
    #--------------------
    def create_wheel(self, movies):
        num_segments = len(movies)
        wheel_x = self.center_x - self.wheel_radius
        wheel_y = self.center_y - self.wheel_radius
        
        wheel_image = os.path.join(self.addon_path, 'resources', 'media', f'wheel_{num_segments}.png')
        
        self.wheel = xbmcgui.ControlImage(
            wheel_x,
            wheel_y,
            self.wheel_radius * 2,
            self.wheel_radius * 2,
            wheel_image
        )
        self.addControl(self.wheel)
        