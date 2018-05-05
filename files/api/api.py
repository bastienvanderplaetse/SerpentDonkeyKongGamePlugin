from serpent.game_api import GameAPI
from serpent.sprite_locator import SpriteLocator
from serpent.sprite import Sprite

from skimage import io

import numpy as np

from .navigation_game_fsm import NavigationGameFSM
from fysom import Fysom


class DonkeyKongAPI(GameAPI):

    def __init__(self, game=None):
        super().__init__(game=game)

        self.navigationGameFSM = NavigationGameFSM()

        self._prepare_sprites()

        self.sprite_locator = SpriteLocator()


    def _prepare_sprites(self):
    	path = './plugins/SerpentDonkeyKongGamePlugin/files/data/sprites/death_'
    	image = io.imread(path + str(1) + '.png')
    	self.death_sprite = Sprite("DEATH", image_data=image[...,np.newaxis])
    	image = io.imread(path + str(2) + '.png')
    	self.death_sprite.append_image_data(image[...,np.newaxis])
    	image = io.imread(path + str(3) + '.png')
    	self.death_sprite.append_image_data(image[...,np.newaxis])
    	image = io.imread(path + str(4) + '.png')
    	self.death_sprite.append_image_data(image[...,np.newaxis])
    	image = io.imread(path + str(5) + '.png')
    	self.death_sprite.append_image_data(image[...,np.newaxis])
    	image = io.imread(path + str(6) + '.png')
    	self.death_sprite.append_image_data(image[...,np.newaxis])
    	image = io.imread(path + str(7) + '.png')
    	self.death_sprite.append_image_data(image[...,np.newaxis])
    	image = io.imread(path + str(8) + '.png')
    	self.death_sprite.append_image_data(image[...,np.newaxis])
    	image = io.imread(path + str(9) + '.png')
    	self.death_sprite.append_image_data(image[...,np.newaxis])
    	image = io.imread(path + str(10) + '.png')
    	self.death_sprite.append_image_data(image[...,np.newaxis])

    	image = io.imread('./plugins/SerpentDonkeyKongTestGamePlugin/files/data/sprites/mario_1.png')
    	self.mario_sprite = Sprite("MARIO", image_data=image[...,np.newaxis])
    	image = io.imread('./plugins/SerpentDonkeyKongTestGamePlugin/files/data/sprites/mario_2.png')
    	self.mario_sprite.append_image_data(image[...,np.newaxis])
    	image = io.imread('./plugins/SerpentDonkeyKongTestGamePlugin/files/data/sprites/mario_3.png')
    	self.mario_sprite.append_image_data(image[...,np.newaxis])
    	image = io.imread('./plugins/SerpentDonkeyKongTestGamePlugin/files/data/sprites/mario_4.png')
    	self.mario_sprite.append_image_data(image[...,np.newaxis])
    	image = io.imread('./plugins/SerpentDonkeyKongTestGamePlugin/files/data/sprites/mario_5.png')
    	self.mario_sprite.append_image_data(image[...,np.newaxis])
    	image = io.imread('./plugins/SerpentDonkeyKongTestGamePlugin/files/data/sprites/mario_6.png')
    	self.mario_sprite.append_image_data(image[...,np.newaxis])
    	image = io.imread('./plugins/SerpentDonkeyKongTestGamePlugin/files/data/sprites/mario_7.png')
    	self.mario_sprite.append_image_data(image[...,np.newaxis])
    	image = io.imread('./plugins/SerpentDonkeyKongTestGamePlugin/files/data/sprites/mario_8.png')
    	self.mario_sprite.append_image_data(image[...,np.newaxis])
    	image = io.imread('./plugins/SerpentDonkeyKongTestGamePlugin/files/data/sprites/mario_9.png')
    	self.mario_sprite.append_image_data(image[...,np.newaxis])
    	image = io.imread('./plugins/SerpentDonkeyKongTestGamePlugin/files/data/sprites/mario_10.png')
    	self.mario_sprite.append_image_data(image[...,np.newaxis])
    	image = io.imread('./plugins/SerpentDonkeyKongTestGamePlugin/files/data/sprites/mario_11.png')
    	self.mario_sprite.append_image_data(image[...,np.newaxis])
    	image = io.imread('./plugins/SerpentDonkeyKongTestGamePlugin/files/data/sprites/mario_12.png')
    	self.mario_sprite.append_image_data(image[...,np.newaxis])
    	image = io.imread('./plugins/SerpentDonkeyKongTestGamePlugin/files/data/sprites/mario_13.png')
    	self.mario_sprite.append_image_data(image[...,np.newaxis])
    	image = io.imread('./plugins/SerpentDonkeyKongTestGamePlugin/files/data/sprites/mario_14.png')
    	self.mario_sprite.append_image_data(image[...,np.newaxis])
    	image = io.imread('./plugins/SerpentDonkeyKongTestGamePlugin/files/data/sprites/mario_15.png')
    	self.mario_sprite.append_image_data(image[...,np.newaxis])
    	image = io.imread('./plugins/SerpentDonkeyKongTestGamePlugin/files/data/sprites/mario_16.png')
    	self.mario_sprite.append_image_data(image[...,np.newaxis])
    	image = io.imread('./plugins/SerpentDonkeyKongTestGamePlugin/files/data/sprites/mario_17.png')
    	self.mario_sprite.append_image_data(image[...,np.newaxis])
    	image = io.imread('./plugins/SerpentDonkeyKongTestGamePlugin/files/data/sprites/mario_18.png')
    	self.mario_sprite.append_image_data(image[...,np.newaxis])
    	image = io.imread('./plugins/SerpentDonkeyKongTestGamePlugin/files/data/sprites/mario_19.png')
    	self.mario_sprite.append_image_data(image[...,np.newaxis])
    	image = io.imread('./plugins/SerpentDonkeyKongTestGamePlugin/files/data/sprites/mario_20.png')
    	self.mario_sprite.append_image_data(image[...,np.newaxis])
    	image = io.imread('./plugins/SerpentDonkeyKongTestGamePlugin/files/data/sprites/mario_21.png')
    	self.mario_sprite.append_image_data(image[...,np.newaxis])
    	image = io.imread('./plugins/SerpentDonkeyKongTestGamePlugin/files/data/sprites/mario_22.png')
    	self.mario_sprite.append_image_data(image[...,np.newaxis])
    	image = io.imread('./plugins/SerpentDonkeyKongTestGamePlugin/files/data/sprites/mario_23.png')
    	self.mario_sprite.append_image_data(image[...,np.newaxis])
    	image = io.imread('./plugins/SerpentDonkeyKongTestGamePlugin/files/data/sprites/mario_24.png')
    	self.mario_sprite.append_image_data(image[...,np.newaxis])
    	image = io.imread('./plugins/SerpentDonkeyKongTestGamePlugin/files/data/sprites/mario_25.png')
    	self.mario_sprite.append_image_data(image[...,np.newaxis])
    	image = io.imread('./plugins/SerpentDonkeyKongTestGamePlugin/files/data/sprites/mario_26.png')
    	self.mario_sprite.append_image_data(image[...,np.newaxis])
    	image = io.imread('./plugins/SerpentDonkeyKongTestGamePlugin/files/data/sprites/mario_27.png')
    	self.mario_sprite.append_image_data(image[...,np.newaxis])
    	image = io.imread('./plugins/SerpentDonkeyKongTestGamePlugin/files/data/sprites/mario_28.png')
    	self.mario_sprite.append_image_data(image[...,np.newaxis])
    	image = io.imread('./plugins/SerpentDonkeyKongTestGamePlugin/files/data/sprites/mario_29.png')
    	self.mario_sprite.append_image_data(image[...,np.newaxis])

    	image = io.imread('./plugins/SerpentDonkeyKongGamePlugin/files/data/sprites/sprite_main_menu_splash_screen.png')
    	self.splash_screen = Sprite("SPLASH", image_data=image[...,np.newaxis])

    def analyze_frame(self, game_frame):
    	if (self.navigationGameFSM.current == "black_screen"):
    		#spriteLocator = SpriteLocator()
    		location = self.sprite_locator.locate(sprite=self.death_sprite, game_frame=game_frame)
    		if (location == None):
    			location = self.sprite_locator.locate(sprite=self.mario_sprite, game_frame=game_frame)
    			if (location != None):
    				self.navigationGameFSM.play()
    	elif (self.navigationGameFSM.current == "playing"):
    		#self.sprite_locator = SpriteLocator()
    		location = self.sprite_locator.locate(sprite=self.mario_sprite, game_frame=game_frame)
    		if (location != None):
    			# reduce frame
    			pass
    		location = self.sprite_locator.locate(sprite=self.death_sprite, game_frame=game_frame)
    		if (location != None):
    			self.navigationGameFSM.die()
    	elif (self.navigationGameFSM.current == "lost"):
    		# image = io.imread('./plugins/SerpentDonkeyKongGamePlugin/files/data/sprites/sprite_main_menu_splash_screen.png')
    		# sprite_to_locate = Sprite("QUERY", image_data=image[...,np.newaxis])
    		#spriteLocator = SpriteLocator()
    		location = self.sprite_locator.locate(sprite=self.splash_screen, game_frame=game_frame)
    		if (location != None):
    			self.navigationGameFSM.run()

    def get_mario_frame(self, game_frame):
    	#sprite_locator = SpriteLocator()
    	location = self.sprite_locator.locate(sprite=self.mario_sprite, game_frame=game_frame)
    	if (location != None):
    		return (game_frame, None)
    	return (None, None)



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