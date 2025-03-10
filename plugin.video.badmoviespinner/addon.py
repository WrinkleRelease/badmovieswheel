import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin
import json
import random
import math
import time
from urllib.parse import parse_qsl

# Plugin information
ADDON = xbmcaddon.Addon()
ADDON_NAME = ADDON.getAddonInfo('name')
ADDON_ID = ADDON.getAddonInfo('id')


class MovieWheel(xbmcgui.WindowXMLDialog):
    def __init__(self, *args, **kwargs):
        self.movies = kwargs.get('movies', [])
        self.selected_movie = None
        self.wheel_spinning = False
        self.spin_time = 5.0  # Spin duration in seconds
        self.spin_slowdown = 0.95  # Deceleration factor
        self.current_angle = 0
        self.spin_speed = 0
        self.segment_size = 360.0 / len(self.movies) if self.movies else 0

    def onInit(self):
        # Set up the wheel background
        self.wheel_bg = self.getControl(101)
        self.movie_labels = []

        # Set up labels for each movie
        for i, movie in enumerate(self.movies):
            label = xbmcgui.ControlLabel(0, 0, 0, 0, movie['title'])
            self.addControl(label)
            self.movie_labels.append(label)

        # Position all movie labels around the wheel
        self.update_labels_position()

        # Setup spinner button
        self.spin_button = self.getControl(201)

    def update_labels_position(self):
        center_x = self.getWidth() / 2
        center_y = self.getHeight() / 2
        # Slightly smaller radius for better spacing
        radius = min(center_x, center_y) * 0.6

        for i, label in enumerate(self.movie_labels):
            angle = math.radians(self.current_angle + i * self.segment_size)

        # Ensure labels have a fixed size for consistent positioning
        label.setWidth(150)
        label.setHeight(30)

        # Calculate positions
        x = center_x + radius * math.cos(angle) - label.getWidth() / 2
        y = center_y + radius * math.sin(angle) - label.getHeight() / 2

        # Apply position and keep text readable
        label.setPosition(int(x), int(y))
        label.setAngle(-self.current_angle)  # Counter-rotate labels

        # Highlight the selected movie segment
        if self.wheel_spinning is False and i == self.get_selected_index():
            label.setColor('0xFFFFFF00')  # Yellow for selected
        else:
            label.setColor('0xFFFFFFFF')  # White for others
            
    def get_selected_index(self):
        # Determine which segment is currently at the "selected" position (top)
        normalized_angle = self.current_angle % 360
        segment_index = int(normalized_angle / self.segment_size)
        return (len(self.movies) - segment_index) % len(self.movies)

    def onAction(self, action):
        action_id = action.getId()
        if action_id in [xbmcgui.ACTION_PREVIOUS_MENU, xbmcgui.ACTION_NAV_BACK]:
            self.close()

    def onClick(self, control_id):
        if control_id == 201 and not self.wheel_spinning:  # Spin button
            self.spin_wheel()
        elif control_id == 202:  # Play button (only active after wheel stops)
            if self.selected_movie:
                self.play_movie()

    def spin_wheel(self):
        self.wheel_spinning = True
        self.spin_speed = random.uniform(20, 30)  # Initial spin speed

        # Disable play button during spinning
        self.getControl(202).setEnabled(False)

        # Start spinning animation
        start_time = time.time()
        while time.time() - start_time < self.spin_time and self.spin_speed > 0.5:
            self.current_angle += self.spin_speed
            self.spin_speed *= self.spin_slowdown
            self.update_labels_position()
            self.wheel_bg.setPosition(
                int(self.getWidth() / 2), int(self.getHeight() / 2))
            self.wheel_bg.setRotation(self.current_angle)
            xbmc.sleep(50)  # Short delay to control frame rate

        # Wheel has stopped
        self.wheel_spinning = False
        selected_index = self.get_selected_index()
        self.selected_movie = self.movies[selected_index]

        # Highlight selected movie and enable play button
        self.update_labels_position()
        self.getControl(202).setEnabled(True)

        # Show selection dialog
        selection_text = f"Selected: {self.selected_movie['title']}"
        self.getControl(301).setText(selection_text)
        self.getControl(301).setVisible(True)

    def play_movie(self):
        if self.selected_movie:
            # Fixed JSON-RPC call that was causing the error
            jsonrpc_string = '{"jsonrpc":"2.0","method":"Player.Open","params":{"item":{"movieid":' + str(
                self.selected_movie["movieid"]) + '}},"id":1}'
            xbmc.executeJSONRPC(jsonrpc_string)
            self.close()


def get_bad_unwatched_movies():
    # Get all movies
    request = {
        "jsonrpc": "2.0",
        "method": "VideoLibrary.GetMovies",
        "params": {
            "properties": ["title", "playcount", "tag"]
        },
        "id": 1
    }

    response = json.loads(xbmc.executeJSONRPC(json.dumps(request)))

    # Filter for unwatched bad movies
    bad_unwatched_movies = []
    if 'result' in response and 'movies' in response['result']:
        for movie in response['result']['movies']:
            tags = movie.get('tag', [])
            if 'Bad Movies' in tags and movie.get('playcount', 0) == 0:
                bad_unwatched_movies.append(movie)

    # Select up to 10 random movies
    if len(bad_unwatched_movies) > 10:
        bad_unwatched_movies = random.sample(bad_unwatched_movies, 10)

    return bad_unwatched_movies


def run():
    # Get movies fitting our criteria
    movies = get_bad_unwatched_movies()

    if not movies:
        dialog = xbmcgui.Dialog()
        dialog.notification(
            ADDON_NAME, "No unwatched bad movies found!", xbmcgui.NOTIFICATION_INFO, 5000)
        return

    # Launch the wheel window
    wheel = MovieWheel("movie_wheel.xml", ADDON.getAddonInfo(
        'path'), "default", movies=movies)
    wheel.doModal()
    del wheel


# Entry point
if __name__ == "__main__":
    run()
