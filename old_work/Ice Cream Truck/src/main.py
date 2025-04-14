import pygame
import sys
from frontend.menu import Menu
from frontend.game_screen import GameScreen
from frontend.result_screen import ResultScreen
from backend.game_logic import GameLogic

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))  # 改回原始大小
        pygame.display.set_caption("Ice Cream Truck")
        self.clock = pygame.time.Clock()
        self.game_logic = GameLogic()
        
        # 初始化各個畫面
        self.current_screen = "menu"
        self.menu = Menu(self.screen)
        self.game_screen = GameScreen(self.screen, self.game_logic)
        self.result_screen = ResultScreen(self.screen)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
            if self.current_screen == "menu":
                self.current_screen = self.menu.run()
            elif self.current_screen == "game":
                self.current_screen, game_data = self.game_screen.run()
                if self.current_screen == "result":
                    self.result_screen.set_results(game_data)
            elif self.current_screen == "result":
                self.current_screen = self.result_screen.run()
            
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.run() 