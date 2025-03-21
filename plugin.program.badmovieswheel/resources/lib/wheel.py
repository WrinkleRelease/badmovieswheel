import xbmc
import xbmcgui
import xbmcaddon
import os

class MovieWheel(xbmcgui.WindowDialog):
    def __init__(self):
        super().__init__()
        
        addon = xbmcaddon.Addon()
        self.addon_path = addon.getAddonInfo('path')

        # Get actual screen dimensions
        screen_width = self.getWidth()
        screen_height = self.getHeight()
        screen_center_x = screen_width // 2
        screen_center_y = screen_height // 2
        
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
        # Set wheel size to a percentage of screen height
        wheel_size = int(min(screen_width, screen_height) * 0.7)
        wheel_x = screen_center_x - (wheel_size // 2)
        wheel_y = screen_center_y - (wheel_size // 2)

        xbmc.log(f"Wheel size: {wheel_size}x{wheel_size}", xbmc.LOGINFO)
        xbmc.log(f"Wheel position: ({wheel_x}, {wheel_y})", xbmc.LOGINFO)

        self.wheel = xbmcgui.ControlImage(
            wheel_x,
            wheel_y,
            wheel_size,
            wheel_size,
            "",
            aspectRatio=1  # Maintain aspect ratio
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
        arrow_y = wheel_y - (arrow_height // 3)

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
        self.wheel.setImage(wheel_image, False)  # Ensure no scaling