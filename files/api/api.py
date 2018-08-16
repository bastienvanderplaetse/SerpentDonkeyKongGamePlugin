from serpent.game_api import GameAPI
from serpent.sprite_locator import SpriteLocator
from serpent.sprite import Sprite
from serpent.game_frame import GameFrame

from skimage import io

import numpy as np

import math
import time

from .navigation_game_fsm import NavigationGameFSM
from fysom import Fysom

import concurrent.futures

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
        self.MOVING_ENTITY = 2
        self.LADDER = 3
        self.LADDER_DELTA = 18

        self.LEVEL_WIN_HEIGHT = 32

        self.sprite_locator = SpriteLocator()

        self.ladders_positions = dict()
        self.ladders_positions[0] = [453, 10000]
        self.ladders_positions[1] = [102, 249]
        self.ladders_positions[2] = [285, 452]
        self.ladders_positions[3] = [104, 194]
        self.ladders_positions[4] = [452, 10000]
        self.ladders_positions[5] = [324, 10000]

        self.on_ladders = dict()
        self.on_ladders[(0,453)] = [374, 328]
        self.on_ladders[(1,102)] = [312, 268]
        self.on_ladders[(1,249)] = [318, 262]
        self.on_ladders[(2,285)] = [258, 202]
        self.on_ladders[(2,452)] = [252, 208]
        self.on_ladders[(3,104)] = [192, 148]
        self.on_ladders[(3,194)] = [196, 144]
        self.on_ladders[(4,452)] = [133, 88]
        self.on_ladders[(5,324)] = [81, 32]

        self.last_stage = 0
        self.max_stage = 0
        self.last_change_stage = 0
        self.useless_actions = 0

        self.level_direction = dict()
        orientation = 1
        for i in range(6):
            self.level_direction[i] = orientation
            orientation = orientation * (-1)

        self.ladders_thresholds = [384, 328, 268, 208, 148, 88]

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
        for i in range(2,5):
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
        locations = [None, None]
        if (self.navigationGameFSM.current == "black_screen"):
            locations[0] = self.sprite_locator.locate(sprite=self.mario_sprite, game_frame=game_frame)
            if (locations[0] != None):
                self.navigationGameFSM.play()
        elif (self.navigationGameFSM.current == "playing"):
            loc = self._multiple_locate(sprite=self.mario_sprite, game_frame=game_frame, forced=True)
            if(len(loc) != 0):
                locations[0] = loc[0]
                locations[1] = None
            else :
                locations[0] = None
                loc = self._multiple_locate(sprite=self.death_sprite, game_frame=game_frame, forced=True)
                if(len(loc) != 0):
                    locations[1] = loc[0]

            if (locations[0] != None):
                has_mario = True

            if (locations[1] != None and locations[0] == None):
                self.navigationGameFSM.die()
                has_mario = False

            if (locations[0] != None and locations[1] == None and locations[0][0] <= self.LEVEL_WIN_HEIGHT):
                self.navigationGameFSM.win()

            if (self.last_change_stage == 0):
                self.last_change_stage = time.time()

        return locations

    def _get_ladders(self, mario_posY):
        level = self._get_level(mario_posY)
        return self.ladders_positions[level]

    def _get_level(self, mario_posY):
        stage = 0
        for i in range(5,-1,-1):
            if (mario_posY <= self.ladders_thresholds[i]):
                stage = i
                break;

        if (stage != self.last_stage):
            self.last_stage = stage
            if (stage > self.max_stage):
                self.max_stage = stage
            self.last_change_stage = time.time()
        return stage

    def _get_moving_entities(self, game_frame):
        moving = []
        inputs = [self.rolling_barrel_sprite, self.falling_barrel_sprite, self.flammy_sprite]
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = {executor.submit(self._multiple_locate, sprite, game_frame): sprite for sprite in inputs}
            for future in concurrent.futures.as_completed(futures):
                moving = moving + future.result()
        return moving

    def get_projection_matrix(self, game_frame, location):
        reduced_frame = None
        units_array = None
        if (location != None):
            temp = game_frame.frame[location[0]-self.HEIGHT*self.n_HEIGHT:location[2],location[1]-self.WIDTH*self.n_WIDTH:location[3]+self.WIDTH*self.n_WIDTH]
            reduced_frame = GameFrame(temp)
            units_array = self._projection(reduced_frame, location)
            nx, ny = units_array.shape
            units_array = units_array.reshape(nx*ny)
            orientation = self._get_orientation(location)
            units_array = np.insert(units_array, len(units_array), orientation)

        return (reduced_frame, units_array)

    def _get_orientation(self, location):
        level = self._get_level(location[0])
        return self.level_direction[level]


    def _projection(self, game_frame, global_mario_positions):
        mario_location = self.sprite_locator.locate(sprite=self.mario_sprite, game_frame=game_frame)
        moving_entities = self._get_moving_entities(game_frame)

        units_array = np.zeros((1+self.n_HEIGHT, 1+2*self.n_WIDTH))
        units_array[self.n_HEIGHT][self.n_WIDTH] = self.MARIO

        ladders = self._get_ladders(global_mario_positions[0])
        for ladder in ladders:
            if (abs(ladder - global_mario_positions[1]) <= self.LADDER_DELTA):
                pos_ladder = self.n_WIDTH
            elif (ladder < global_mario_positions[1]):
                # ladder on left
                pos_ladder = self.n_WIDTH - (int((global_mario_positions[1]-ladder)/self.WIDTH)+1)
            else :
                # ladder on right
                pos_ladder = int((ladder - global_mario_positions[1])/self.WIDTH)
                if (pos_ladder == 0):
                    pos_ladder = 1
                pos_ladder = pos_ladder + self.n_WIDTH

            if(pos_ladder >= 0 and pos_ladder <= (2*self.n_WIDTH)):
                units_array[self.n_HEIGHT][pos_ladder] = self.LADDER

        for entity in moving_entities:
            if (entity[3] <= mario_location[1]):
                # left
                posX = entity[3] 
            elif (entity[1] >= mario_location[3]):
                # right
                posX = entity[1]
            else :
                # centered on Mario
                posX = self.n_WIDTH*self.WIDTH

            if (entity[0] >= mario_location[2]):
                # bottom
                posY = entity[0]
            elif (entity[2] <= mario_location[0]):
                # up
                posY = entity[2]
            else:
                # centered on Mario
                posY = self.n_HEIGHT*self.HEIGHT

            units_array[int(posY/self.HEIGHT)][int(posX/self.WIDTH)] = self.MOVING_ENTITY

        return units_array

    def _multiple_locate(self, sprite=None, game_frame=None, screen_region=None, use_global_location=True, forced=False):
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
            if (forced and len(locations) > 0):
                break

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
            if(not locations[i][0] in temp and not locations[i][0]-1 in temp and not locations[i][0]+1 in temp):
                temp.append(locations[i][0])
                epurated.append(locations[i])
        return epurated

    def get_score_value(self, location):
        values = [-1000,-1000,-1000,-1000,-1000]
        if (location != None):
            values[0] = self._get_level(location[0])
            ladders = self._get_ladders(location[0])
            minimum_distance = int(abs(ladders[0]-location[3]))
            for ladder in ladders :
                if (abs(ladder - location[1]) <= self.LADDER_DELTA):
                    distance = 0
                elif (ladder < location[1]) :
                    distance = int(abs(ladder-location[1]))
                else:
                    distance = int(abs(ladder-location[3]))
                if (distance < minimum_distance):
                    minimum_distance = distance

            values[1] = -1 * minimum_distance
            values[2] = self.max_stage
            values[3] = self.useless_actions
            if (self._is_on_ladder(values[0],location)):
                values[4] = 1
            else:
                values[4] = 0

        self.last_change_stage = 0
        self.last_stage = 0
        self.max_stage = 0
        self.useless_actions = 0

        return values

    def _is_on_ladder(self, level, location):
        ladders = self.ladders_positions[level]
        for ladder in ladders:
            if (abs(ladder-location[1]) <= self.LADDER_DELTA):
                couple = (level, ladder)
                if (couple in self.on_ladders):
                    extremity = self.on_ladders[couple]
                    if (location[0] <= extremity[0] and location[0] > extremity[1]):
                        return True
        return False

    def get_death_location(self, game_frame):
        return self.sprite_locator.locate(sprite=self.death_sprite, game_frame=game_frame)

    def analyze_action(self, inputs, outputs):
        ### FILTRE LES JUMPS INUTILES
        # N = self.n_WIDTH * 2 + 1
        # row = self.n_HEIGHT * N

        # has_obstacle = False

        # for i in range(N):
        #     if(inputs[row+i] == self.MOVING_ENTITY):
        #         has_obstacle = True
        #         break;

        # if (not has_obstacle and outputs[len(outputs)-1] == 1):
        #     self.useless_actions = self.useless_actions + 1
        if (outputs[len(outputs)-1] == 1):
            self.useless_actions = self.useless_actions + 1


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

    def has_won(self):
        return self.navigationGameFSM.current == "has_won"

    def run(self):
        self.navigationGameFSM.run()

    def next(self):
        self.navigationGameFSM.next()

    def win(self):
        self.navigationGameFSM.win()

    class MyAPINamespace:

        @classmethod
        def my_namespaced_api_function(cls):
            api = DonkeyKongAPI.instance