import pygame

from dino_runner.utils.constants import (
    BG,
    ICON,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TITLE,
    FPS,
    FONT_ARIAL)
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.power_ups.power_up_manager import PowerUpManager
from dino_runner.components.player_hearts.heart_manager import HeartManager


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.points = 0
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()
        self.heart_manager = HeartManager()


    def increase_score(self):
        self.points += 1
        if self.points % 100 == 0:
            self.game_speed += 1
        
        self.player.check_invincibility()

    def run(self):
        # Game loop: events - update - draw
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()
        pygame.quit()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self.game_speed, self)
        self.power_up_manager.update(self.points, self.game_speed, self.player)
        self.increase_score()
        

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255)) #RGB
        if self.points % 100 == 500:
            self.screen.fill((255, 0, 0))
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.power_up_manager.draw(self.screen)
        self.draw_score()
        self.heart_manager.draw(self.screen)
        pygame.display.update()
        pygame.display.flip()
 
    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed
    #    else not show(game_over)
    

    def draw_score(self):
        font = pygame.font.Font(FONT_ARIAL, 30)
        surface = font.render(str(self.points), True, (0, 0, 0))
        rect = surface.get_rect()
        rect.x = 1000
        rect.y = 10
        self.screen.blit(surface, rect)
        print("score")

  #  def reset_game(self):
   #     self.obstacle_manager.reset_obstacles()
    #    self.score = 0
     #   self.game_speed = 20
      #  self.power_ups_manager.reset_power_ups()