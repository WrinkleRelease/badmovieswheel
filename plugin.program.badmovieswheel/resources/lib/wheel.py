import xbmc
import xbmcgui
import xbmcaddon
import math
import time
import os

class MovieWheel(xbmcgui.WindowDialog):
    def __init__(self):
        super().__init__()
        
        addon = xbmcaddon.Addon()
        self.addon_path = addon.getAddonInfo('path')

        # Fixed dimensions for 1920x1080
        screen_width = 1920
        screen_height = 1080
        screen_center_x = screen_width // 2   # Should be 960
        screen_center_y = screen_height // 2  # Should be 540
        
        xbmc.log(f"Screen dimensions: {screen_width}x{screen_height}", xbmc.LOGINFO)
        xbmc.log(f"Screen center: ({screen_center_x}, {screen_center_y})", xbmc.LOGINFO)

        #------------------------
        ## MARK: Background Image
        #-------------------------
        background_image = os.path.join(self.addon_path, 'resources', 'media', 'background.png')
        self.background = xbmcgui.ControlImage(0, 0, screen_width, screen_height, background_image)
        self.addControl(self.background)
        
        #-------------
        ## MARK: Wheel
        #-------------
        wheel_width = 800
        wheel_height = 800
        # Center the wheel using screen center coordinates
        wheel_x = screen_center_x - (wheel_width // 2)    # 960 - 400 = 560
        wheel_y = screen_center_y - (wheel_height // 2)   # 540 - 400 = 140

        xbmc.log(f"Wheel dimensions: {wheel_width}x{wheel_height}", xbmc.LOGINFO)
        xbmc.log(f"Wheel position: ({wheel_x}, {wheel_y})", xbmc.LOGINFO)

        self.wheel = xbmcgui.ControlImage(
            wheel_x,
            wheel_y,
            wheel_width,
            wheel_height,
            ""
        )

        self.addControl(self.wheel)
        
        #-----------------
        ## MARK: Add Arrow
        #-----------------
        arrow_width = 197
        arrow_height = 106
        # Center arrow with wheel
        arrow_x = screen_center_x - (arrow_width // 2)
        # Position arrow closer to wheel
        arrow_y = wheel_y - (arrow_height // 3)  # Adjusted fraction for better overlap

        xbmc.log(f"Arrow dimensions: {arrow_width}x{arrow_height}", xbmc.LOGINFO)
        xbmc.log(f"Arrow position: ({arrow_x}, {arrow_y})", xbmc.LOGINFO)
        
        arrow_image = os.path.join(self.addon_path, 'resources', 'media', 'arrow.png')
        self.arrow = xbmcgui.ControlImage(
            arrow_x,
            arrow_y,
            arrow_width,
            arrow_height,
            arrow_image
        )
        self.addControl(self.arrow)

    def create_wheel(self, movies):
        num_segments = len(movies)
        wheel_image = os.path.join(self.addon_path, 'resources', 'media', f'wheel_{num_segments}.png')
        self.wheel.setImage(wheel_image)