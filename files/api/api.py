from serpent.game_api import GameAPI
from serpent.sprite_locator import SpriteLocator
from serpent.sprite import Sprite
from serpent.game_frame import GameFrame

from skimage import io

import numpy as np

from .navigation_game_fsm import NavigationGameFSM
from fysom import Fysom


class DonkeyKongAPI(GameAPI):

    def __init__(self, game=None):
        super().__init__(game=game)

        self.navigationGameFSM = NavigationGameFSM()

        self._prepare_sprites()

        self.WIDTH = 34
        self.HEIGHT = 32
        self.n_WIDTH = 2
        self.n_HEIGHT = 2

        self.MARIO = 1
        self.ROLLING_BARREL = 2
        self.FALLING_BARREL = 3
        self.FLAMMY = 4

        self.sprite_locator = SpriteLocator()


    def _prepare_sprites(self):
        # Death Sprite
        path = './plugins/SerpentDonkeyKongGamePlugin/files/data/sprites/death_{}.png'
        image = io.imread(path.format(1))
        self.death_sprite = Sprite("DEATH", image_data=image[...,np.newaxis])
        for i in range(2,11):
            image = io.imread(path.format(i))
            self.death_sprite.append_image_data(image[...,np.newaxis])

        # Mario Sprite
        path = './plugins/SerpentDonkeyKongGamePlugin/files/data/sprites/mario_{}.png'
        image = io.imread(path.format(1))
        self.mario_sprite = Sprite("MARIO", image_data=image[...,np.newaxis])
        for i in range(2,30):
            image = io.imread(path.format(i))
            self.mario_sprite.append_image_data(image[...,np.newaxis])

        # Falling Barrels Sprite
        path = './plugins/SerpentDonkeyKongGamePlugin/files/data/sprites/falling_barrel_{}.png'
        image = io.imread(path.format(1))
        self.falling_barrel_sprite = Sprite("FALLING", image_data=image[...,np.newaxis])
        for i in range(2,3):
            image = io.imread(path.format(i))
            self.falling_barrel_sprite.append_image_data(image[...,np.newaxis])

        # Rolling Barrels Sprite
        path = './plugins/SerpentDonkeyKongGamePlugin/files/data/sprites/rolling_barrel_{}.png'
        image = io.imread(path.format(1))
        self.rolling_barrel_sprite = Sprite("ROLLING", image_data=image[...,np.newaxis])
        for i in range(2,3):
            image = io.imread(path.format(i))
            self.rolling_barrel_sprite.append_image_data(image[...,np.newaxis])

        # Fire Monster Sprite
        path = './plugins/SerpentDonkeyKongGamePlugin/files/data/sprites/flammy_{}.png'
        image = io.imread(path.format(1))
        self.flammy_sprite = Sprite("FLAMMY", image_data=image[...,np.newaxis])
        for i in range(2,5):
            image = io.imread(path.format(i))
            self.flammy_sprite.append_image_data(image[...,np.newaxis])

        # Splash Screen Sprite
        image = io.imread('./plugins/SerpentDonkeyKongGamePlugin/files/data/sprites/sprite_main_menu_splash_screen.png')
        self.splash_screen = Sprite("SPLASH", image_data=image[...,np.newaxis])

    def analyze_frame(self, game_frame):
        if (self.navigationGameFSM.current == "black_screen"):
            location = self.sprite_locator.locate(sprite=self.death_sprite, game_frame=game_frame)
            if (location == None):
                location = self.sprite_locator.locate(sprite=self.mario_sprite, game_frame=game_frame)
                if (location != None):
                    self.navigationGameFSM.play()
        elif (self.navigationGameFSM.current == "playing"):
            location = self.sprite_locator.locate(sprite=self.mario_sprite, game_frame=game_frame)
            if (location != None):
                # reduce frame
                pass
            location = self.sprite_locator.locate(sprite=self.death_sprite, game_frame=game_frame)
            if (location != None):
                self.navigationGameFSM.die()
        elif (self.navigationGameFSM.current == "lost"):
            location = self.sprite_locator.locate(sprite=self.splash_screen, game_frame=game_frame)
            if (location != None):
                self.navigationGameFSM.run()

    def get_mario_frame(self, game_frame):
        location = self.sprite_locator.locate(sprite=self.mario_sprite, game_frame=game_frame)
        reduced_frame = None
        units_array = None
        if (location != None):
            temp = game_frame.frame[location[0]-self.HEIGHT*self.n_HEIGHT:location[2]+self.HEIGHT*self.n_HEIGHT,location[1]-self.WIDTH*self.n_WIDTH:location[3]+self.WIDTH*self.n_WIDTH]
            reduced_frame = GameFrame(temp)
            units_array = self._reduction(reduced_frame)

        return (reduced_frame, units_array)

    def _reduction(self, game_frame):
        simplified_frame = self._simplify_frame(game_frame)

        units_array = np.zeros((1+2*self.n_HEIGHT, 1+2*self.n_WIDTH))
        units_array[self.n_HEIGHT][self.n_WIDTH] = self.MARIO

        x, y, z = game_frame.frame.shape
        height = int(x/self.HEIGHT)
        widht = int(y/self.WIDTH)

        for i in range(0, height-1):
            for j in range(0, widht-1):
                case = simplified_frame[i*self.HEIGHT + int(self.HEIGHT/2)-1][j*self.WIDTH + int(self.WIDTH/2)-1]
                if (case == self.FALLING_BARREL):
                    units_array[i][j] = self.FALLING_BARREL
                elif (case == self.ROLLING_BARREL):
                    units_array[i][j] = self.ROLLING_BARREL
                elif (case == self.FLAMMY):
                    units_array[i][j] = self.FLAMMY

        return units_array


    def _simplify_frame(self, game_frame):
        x, y, z = game_frame.frame.shape
        simplified_frame = np.zeros((x, y))

        location = self.sprite_locator.locate(sprite=self.mario_sprite, game_frame=game_frame)
        if(location != None):
            for i in range(location[0], location[2]):
                for j in range(location[1], location[3]):
                    simplified_frame[i][j] = 1

            locations = self._multiple_locate(sprite=self.rolling_barrel_sprite, game_frame=game_frame)
            for location in locations:
                for i in range(location[0], location[2]):
                    for j in range(location[1], location[3]):
                        simplified_frame[i][j] = self.ROLLING_BARREL

            locations = self._multiple_locate(sprite=self.falling_barrel_sprite, game_frame=game_frame)
            for location in locations:
                for i in range(location[0], location[2]):
                    for j in range(location[1], location[3]):
                        simplified_frame[i][j] = self.FALLING_BARREL

            locations = self._multiple_locate(sprite=self.flammy_sprite, game_frame=game_frame)
            for location in locations:
                for i in range(location[0], location[2]):
                    for j in range(location[1], location[3]):
                        simplified_frame[i][j] = self.FLAMMY

        return simplified_frame

    def _multiple_locate(self, sprite=None, game_frame=None, screen_region=None, use_global_location=True):
        constellation_of_pixel_images = sprite.generate_constellation_of_pixels_images()
        locations = []

        frame = game_frame.frame

        if screen_region is not None:
            frame = serpent.cv.extract_region_from_image(frame, screen_region)

        for i in range(len(constellation_of_pixel_images)):
            constellation_of_pixels_item = list(sprite.constellation_of_pixels[i].items())[0]

            query_coordinates = constellation_of_pixels_item[0]
            query_rgb = constellation_of_pixels_item[1]

            rgb_coordinates = Sprite.locate_color(query_rgb, image=frame)

            rgb_coordinates = list(map(lambda yx: (yx[0] - query_coordinates[0], yx[1] - query_coordinates[1]), rgb_coordinates))

            maximum_y = frame.shape[0] - constellation_of_pixel_images[i].shape[0]
            maximum_x = frame.shape[1] - constellation_of_pixel_images[i].shape[1]

            for y, x in rgb_coordinates:
                if y < 0 or x < 0 or y > maximum_y or x > maximum_x:
                    continue

                for yx, rgb in sprite.constellation_of_pixels[i].items():
                    if tuple(frame[y + yx[0], x + yx[1], :]) != rgb:
                        break
                else:
                    locations.append((
                        y,
                        x,
                        y + constellation_of_pixel_images[i].shape[0],
                        x + constellation_of_pixel_images[i].shape[1]
                    ))

        if len(locations) != 0 and screen_region is not None and use_global_location:
            for i in range(0,len(locations)):
                locations[i] = (
                    locations[i][0] + screen_region[0],
                    locations[i][1] + screen_region[1],
                    locations[i][2] + screen_region[0],
                    locations[i][3] + screen_region[1]
                )

        if len(locations) > 0:
            locations = self._epurate(locations)

        return locations

    def _epurate(self, locations):
        temp = []
        epurated = []
        for i in range(0,len(locations)):
            if(not locations[i][0] in temp):
                temp.append(locations[i][0])
                epurated.append(locations[i])
        return epurated



    """
    Methods to use the NavigationGame FSM
    """

    def not_running(self):
        return self.navigationGameFSM.current == "not_running"

    def is_in_menu(self):
        return self.navigationGameFSM.current == "menu"

    def is_playing(self):
        return self.navigationGameFSM.current == "playing"

    def is_dead(self):
        return self.navigationGameFSM.current == "dead"

    def run(self):
        self.navigationGameFSM.run()

    def next(self):
        self.navigationGameFSM.next()

    def replay(self):
        self.navigationGameFSM.replay()



    class MyAPINamespace:

        @classmethod
        def my_namespaced_api_function(cls):
            api = DonkeyKongAPI.instance