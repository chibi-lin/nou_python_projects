import pygame

class ResultScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 48)
        self.results = None
        
    def set_results(self, results):
        self.results = results
        
    def run(self):
        while True:
            self.screen.fill((255, 255, 255))
            
            if self.results:
                # 繪製標題
                title = self.font.render("Game over!", True, (0, 0, 0))
                title_rect = title.get_rect(center=(400, 100))
                self.screen.blit(title, title_rect)
                
                # 繪製金錢結果
                money_text = self.small_font.render(f"總收入: {self.results['money']} 元", True, (0, 0, 0))
                money_rect = money_text.get_rect(center=(400, 250))
                self.screen.blit(money_text, money_rect)
                
                # 繪製客流量結果
                customer_text = self.small_font.render(f"服務客人數: {self.results['customer_count']} 人", True, (0, 0, 0))
                customer_rect = customer_text.get_rect(center=(400, 350))
                self.screen.blit(customer_text, customer_rect)
                
                # 繪製重新開始按鈕
                restart_text = self.font.render("重新開始", True, (0, 0, 0))
                restart_rect = restart_text.get_rect(center=(400, 500))
                self.screen.blit(restart_text, restart_rect)
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        if restart_rect.collidepoint(mouse_pos):
                            return "menu"
            
            pygame.display.flip() 