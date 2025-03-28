import pygame

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.title_font = pygame.font.Font(None, 80)  # 縮小標題字體
        self.font = pygame.font.Font(None, 48)        # 縮小按鈕字體
        self.instruction_font = pygame.font.Font(None, 32)  # 說明文字字體
        
    def run(self):
        while True:
            self.screen.fill((255, 255, 255))
            
            # 繪製標題
            title = self.title_font.render("Ice Cream Truck", True, (0, 0, 0))
            title_rect = title.get_rect(center=(400, 100))  # 調整標題位置
            self.screen.blit(title, title_rect)
            
            # 繪製遊戲說明
            instructions = [
                "- Serve ice cream to customers within their waiting time",
                "- Each customer may order 1-3 scoops",
                "- Some customers want cone, some don't",
                "- Each scoop costs $10, cone costs $5",
                "- You can store up to 5 ice creams",
                "- Game time: 5 minutes"
            ]
            
            for i, text in enumerate(instructions):
                instruction = self.instruction_font.render(text, True, (0, 0, 0))
                self.screen.blit(instruction, (150, 180 + i * 35))  # 調整說明文字位置和間距
            
            # 繪製開始按鈕
            start_button = pygame.Rect(250, 420, 300, 50)  # 調整按鈕位置和大小
            pygame.draw.rect(self.screen, (150, 220, 150), start_button)
            start_text = self.font.render("Start Game", True, (0, 0, 0))
            start_rect = start_text.get_rect(center=(400, 445))
            self.screen.blit(start_text, start_rect)
            
            # 繪製退出按鈕
            quit_button = pygame.Rect(250, 490, 300, 50)  # 調整按鈕位置和大小
            pygame.draw.rect(self.screen, (220, 150, 150), quit_button)
            quit_text = self.font.render("Quit", True, (0, 0, 0))
            quit_rect = quit_text.get_rect(center=(400, 515))
            self.screen.blit(quit_text, quit_rect)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if start_button.collidepoint(mouse_pos):
                        return "game"
                    if quit_button.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()
            
            pygame.display.flip() 