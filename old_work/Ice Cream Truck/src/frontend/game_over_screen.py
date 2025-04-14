def draw(self):
    self.screen.fill((255, 255, 255))
    
    stats = self.game_logic.get_final_stats()
    
    # 顯示遊戲結束標題
    title = self.font.render("Game Over!", True, (0, 0, 0))
    self.screen.blit(title, (300, 100))
    
    # 顯示最終統計
    revenue_text = self.font.render(f"Total Revenue: ${stats['total_revenue']}", True, (0, 0, 0))
    costs_text = self.font.render(f"Total Costs: ${stats['total_costs']}", True, (0, 0, 0))
    profit_text = self.font.render(f"Net Profit: ${stats['net_profit']}", True, (0, 0, 0))
    
    self.screen.blit(revenue_text, (250, 200))
    self.screen.blit(costs_text, (250, 250))
    self.screen.blit(profit_text, (250, 300))
    
    # 繼續按鈕
    continue_text = self.font.render("Click anywhere to continue", True, (0, 0, 0))
    self.screen.blit(continue_text, (250, 400)) 