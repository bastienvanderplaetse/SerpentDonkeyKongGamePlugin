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