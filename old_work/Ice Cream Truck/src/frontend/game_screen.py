import pygame
import sys
import time

class GameScreen:
    def __init__(self, screen, game_logic):
        self.screen = screen
        self.game_logic = game_logic
        self.font = pygame.font.Font(None, 32)
        self.clock = pygame.time.Clock()
        
        # 冰淇淋口味
        self.flavors = ["Vanilla", "Chocolate", "Milk", "Mint Chocolate"]
        
        # 當前製作的冰淇淋
        self.current_ice_cream = {
            'flavors': {},
            'has_cone': False,
            'total_scoops': 0
        }
        
        # 遊戲開始時間
        self.start_time = time.time()
        
        # 初始化所有按鈕列表
        self.flavor_buttons = []
        self.cone_button = None
        self.make_button = None
        self.discard_button = None
        self.deliver_buttons = []
        self.delete_freezer_buttons = []

    def run(self):
        running = True
        last_time = time.time()
        
        while running:
            current_time = time.time()
            dt = current_time - last_time
            last_time = current_time
            
            # 更新遊戲邏輯，檢查是否遊戲結束
            if self.game_logic.update(dt):
                return self.show_game_over()  # 返回結算畫面的結果
            
            # 清空屏幕
            self.screen.fill((255, 255, 255))
            
            # 繪製遊戲界面
            self.draw_game_interface()
            
            # 事件處理
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
            
            # 更新顯示
            pygame.display.flip()
            self.clock.tick(60)
        
        return "QUIT"

    def draw_game_interface(self):
        # 先畫背景
        self.screen.fill((255, 255, 255))
        
        # 畫狀態欄（調整高度和位置）
        self.draw_status_bar()
        
        # 畫主要遊戲區域
        self.draw_customers()
        self.draw_freezer()
        self.draw_ice_cream_maker()

    def draw_status_bar(self):
        status_bar = pygame.Rect(0, 0, 800, 50)
        pygame.draw.rect(self.screen, (220, 220, 220), status_bar)
        
        status_font = pygame.font.Font(None, 28)
        
        # 計算剩餘時間
        remaining_time = max(0, self.game_logic.max_game_time - self.game_logic.game_time)
        minutes = int(remaining_time) // 60
        seconds = int(remaining_time) % 60
        
        # 第一行：財務和時間信息
        revenue_text = status_font.render(f"Revenue: ${self.game_logic.money}", True, (0, 0, 0))
        costs_text = status_font.render(f"Costs: ${self.game_logic.costs}", True, (0, 0, 0))
        profit_text = status_font.render(f"Profit: ${self.game_logic.money - self.game_logic.costs}", True, (0, 0, 0))
        # 時間顯示格式改為 MM:SS
        time_text = status_font.render(f"Time: {minutes:02d}:{seconds:02d}", True, 
                                     (255, 0, 0) if remaining_time <= 30 else (0, 0, 0))  # 最後30秒顯示紅色
        
        # 第二行：客人統計
        customers_text = status_font.render(
            f"Served: {self.game_logic.served_customers} | Lost: {self.game_logic.lost_customers}", 
            True, 
            (0, 100, 0) if self.game_logic.served_customers > self.game_logic.lost_customers else (150, 0, 0)
        )
        
        # 繪製第一行
        self.screen.blit(revenue_text, (10, 5))
        self.screen.blit(costs_text, (200, 5))
        self.screen.blit(profit_text, (400, 5))
        self.screen.blit(time_text, (600, 5))
        
        # 繪製第二行
        self.screen.blit(customers_text, (10, 28))

    def draw_customers(self):
        customer_area = pygame.Rect(10, 50, 480, 280)
        pygame.draw.rect(self.screen, (230, 230, 230), customer_area)
        
        small_font = pygame.font.Font(None, 24)
        
        for i, customer in enumerate(self.game_logic.customers):
            y_pos = 60 + i * 90
            customer_box = pygame.Rect(20, y_pos, 460, 80)
            pygame.draw.rect(self.screen, (255, 255, 255), customer_box)
            
            # 計算剩餘時間（去除小數點）
            current_time = time.time()
            remaining_time = max(0, int(customer.wait_time - (current_time - customer.arrival_time)))
            
            # 用紅色顯示等待時間
            wait_text = self.font.render(f"{remaining_time}s", True, (255, 0, 0))
            self.screen.blit(wait_text, (30, y_pos + 10))
            
            # 訂單信息
            order_text = "Wants: "
            flavors_text = []
            for flavor, count in customer.order['flavors'].items():
                flavors_text.append(f"{count}x {flavor}")
            order_line1 = small_font.render(order_text + ", ".join(flavors_text), True, (0, 0, 0))
            
            cone_text = "with cone" if customer.order['has_cone'] else "no cone"
            order_line2 = small_font.render(cone_text, True, (0, 0, 0))
            
            self.screen.blit(order_line1, (30, y_pos + 35))
            self.screen.blit(order_line2, (30, y_pos + 55))

    def draw_freezer(self):
        freezer_area = pygame.Rect(10, 340, 480, 250)
        pygame.draw.rect(self.screen, (200, 220, 255), freezer_area)
        
        title = self.font.render("Freezer (max 5)", True, (0, 0, 0))
        self.screen.blit(title, (20, 350))
        
        # 清空按鈕列表
        self.deliver_buttons = []
        self.delete_freezer_buttons = []
        
        # 顯示冷凍櫃中的冰淇淋
        for i, ice_cream in enumerate(self.game_logic.freezer_ice_creams):
            y_pos = 380 + i * 40
            ice_cream_text = ""
            
            # 顯示口味和數量
            for flavor, count in ice_cream['flavors'].items():
                ice_cream_text += f"{count}x {flavor} "
            if ice_cream['has_cone']:
                ice_cream_text += "+ cone"
            
            # 繪製冰淇淋信息
            text = self.font.render(ice_cream_text, True, (0, 0, 0))
            self.screen.blit(text, (30, y_pos))
            
            # 添加交付和刪除按鈕
            deliver_button = pygame.Rect(300, y_pos, 80, 30)
            delete_button = pygame.Rect(390, y_pos, 80, 30)
            
            pygame.draw.rect(self.screen, (150, 220, 150), deliver_button)
            pygame.draw.rect(self.screen, (220, 150, 150), delete_button)
            
            deliver_text = self.font.render("Deliver", True, (0, 0, 0))
            delete_text = self.font.render("Delete", True, (0, 0, 0))
            
            self.screen.blit(deliver_text, (310, y_pos + 5))
            self.screen.blit(delete_text, (400, y_pos + 5))
            
            self.deliver_buttons.append((deliver_button, i))
            self.delete_freezer_buttons.append((delete_button, i))

    def draw_ice_cream_maker(self):
        # 製作區域（右側）
        maker_area = pygame.Rect(500, 50, 290, 540)
        pygame.draw.rect(self.screen, (240, 240, 240), maker_area)
        
        # 重置按鈕列表
        self.flavor_buttons = []
        
        # 當前製作狀態
        status = []
        for flavor, scoops in self.current_ice_cream['flavors'].items():
            status.append(f"{scoops}x {flavor}")
        status_text = " + ".join(status)
        if self.current_ice_cream['has_cone']:
            status_text += " + Cone"
            
        status = self.font.render(status_text if status_text else "Select flavors", True, (0, 0, 0))
        self.screen.blit(status, (510, 60))
        
        # 口味按鈕
        flavors = ["Vanilla", "Chocolate", "Milk", "Mint Chocolate"]  # 確保包含所有口味
        for i, flavor in enumerate(flavors):
            button_rect = pygame.Rect(510, 100 + i * 45, 270, 35)
            color = (180, 220, 180) if flavor in self.current_ice_cream['flavors'] else (220, 220, 220)
            pygame.draw.rect(self.screen, color, button_rect)
            text = self.font.render(flavor, True, (0, 0, 0))
            self.screen.blit(text, (520, 108 + i * 45))
            self.flavor_buttons.append((button_rect, flavor))
        
        # 甜筒按鈕
        cone_y = 100 + len(flavors) * 45  # 根據口味數量調整位置
        self.cone_button = pygame.Rect(510, cone_y, 270, 35)
        color = (180, 220, 180) if self.current_ice_cream['has_cone'] else (220, 220, 220)
        pygame.draw.rect(self.screen, color, self.cone_button)
        text = self.font.render("Add Cone", True, (0, 0, 0))
        self.screen.blit(text, (520, cone_y + 8))
        
        # 製作和丟棄按鈕
        make_y = cone_y + 45
        self.make_button = pygame.Rect(510, make_y, 130, 35)
        self.discard_button = pygame.Rect(650, make_y, 130, 35)
        
        pygame.draw.rect(self.screen, (150, 220, 150), self.make_button)
        pygame.draw.rect(self.screen, (220, 150, 150), self.discard_button)
        
        make_text = self.font.render("Make", True, (0, 0, 0))
        discard_text = self.font.render("Discard", True, (0, 0, 0))
        
        self.screen.blit(make_text, (540, make_y + 8))
        self.screen.blit(discard_text, (680, make_y + 8))

    def handle_click(self, pos):
        # 檢查口味按鈕
        for button, flavor in self.flavor_buttons:
            if button.collidepoint(pos):
                total_scoops = sum(self.current_ice_cream['flavors'].values())
                if total_scoops < 3:
                    current = self.current_ice_cream['flavors'].get(flavor, 0)
                    self.current_ice_cream['flavors'][flavor] = current + 1
                return True

        # 檢查甜筒按鈕
        if self.cone_button and self.cone_button.collidepoint(pos):
            self.current_ice_cream['has_cone'] = not self.current_ice_cream['has_cone']
            return True

        # 檢查製作按鈕 - 這裡計算成本
        if self.make_button and self.make_button.collidepoint(pos):
            if (len(self.game_logic.freezer_ice_creams) < 5 and 
                self.current_ice_cream['flavors']):
                # 計算成本並添加到總成本中
                cost = 0
                for flavor, count in self.current_ice_cream['flavors'].items():
                    cost += count * 5  # 每球5元
                if self.current_ice_cream['has_cone']:
                    cost += 1  # 甜筒1元
                self.game_logic.costs += cost
                
                self.game_logic.freezer_ice_creams.append(dict(self.current_ice_cream))
                self.current_ice_cream = {
                    'flavors': {},
                    'has_cone': False
                }
            return True

        # 檢查丟棄按鈕 - 製作區的丟棄，不計算成本
        if self.discard_button and self.discard_button.collidepoint(pos):
            self.current_ice_cream = {
                'flavors': {},
                'has_cone': False
            }
            return True

        # 檢查冷凍庫按鈕
        for button, index in self.deliver_buttons:
            if button.collidepoint(pos) and self.game_logic.customers:
                self.deliver_ice_cream(index)
                return True

        # 檢查刪除冷凍庫按鈕 - 直接刪除，不重複計算成本
        for button, index in self.delete_freezer_buttons:
            if button.collidepoint(pos):
                if index < len(self.game_logic.freezer_ice_creams):
                    self.game_logic.freezer_ice_creams.pop(index)
                return True

        return False

    def deliver_ice_cream(self, index):
        if index >= len(self.game_logic.freezer_ice_creams):
            return
        
        ice_cream = self.game_logic.freezer_ice_creams[index]
        delivered = False
        
        for customer in self.game_logic.customers:
            # 檢查是否匹配並交付
            if (ice_cream['has_cone'] == customer.order['has_cone'] and 
                ice_cream['flavors'] == customer.order['flavors']):
                
                # 計算售價（根據球數）
                total_scoops = sum(ice_cream['flavors'].values())
                price = total_scoops * 10  # 每球10元
                
                # 更新收入
                self.game_logic.money += price
                self.game_logic.served_customers += 1
                
                # 移除冰淇淋和客人
                self.game_logic.freezer_ice_creams.pop(index)
                self.game_logic.customers.remove(customer)
                delivered = True
                break
            
        return delivered

    def show_game_over(self):
        running = True
        try:
            # 使用較大字體顯示遊戲結束
            title_font = pygame.font.Font(None, 48)
            stats_font = pygame.font.Font(None, 36)
            button_font = pygame.font.Font(None, 32)
            
            while running:
                self.screen.fill((255, 255, 255))
                
                # 顯示最終統計
                title = title_font.render("Game Over!", True, (0, 0, 0))
                revenue_text = stats_font.render(f"Total Revenue: ${self.game_logic.money}", True, (0, 0, 0))
                costs_text = stats_font.render(f"Total Costs: ${self.game_logic.costs}", True, (0, 0, 0))
                profit_text = stats_font.render(f"Final Profit: ${self.game_logic.money - self.game_logic.costs}", True, (0, 0, 0))
                
                # 添加客人服務統計
                served_text = stats_font.render(f"Customers Served: {self.game_logic.served_customers}", True, (0, 100, 0))
                lost_text = stats_font.render(f"Customers Lost: {self.game_logic.lost_customers}", True, (150, 0, 0))
                
                # 計算服務率
                total_customers = self.game_logic.served_customers + self.game_logic.lost_customers
                if total_customers > 0:
                    service_rate = (self.game_logic.served_customers / total_customers) * 100
                    service_text = stats_font.render(f"Service Rate: {service_rate:.1f}%", True, (0, 0, 150))
                else:
                    service_text = stats_font.render("Service Rate: N/A", True, (0, 0, 150))
                
                # 創建返回按鈕
                return_button = pygame.Rect(300, 480, 200, 40)
                pygame.draw.rect(self.screen, (200, 200, 200), return_button)
                return_text = button_font.render("Return to Menu", True, (0, 0, 0))
                return_text_rect = return_text.get_rect(center=return_button.center)
                
                # 顯示所有統計信息
                self.screen.blit(title, (320, 150))
                self.screen.blit(revenue_text, (250, 220))
                self.screen.blit(costs_text, (250, 260))
                self.screen.blit(profit_text, (250, 300))
                self.screen.blit(served_text, (250, 340))
                self.screen.blit(lost_text, (250, 380))
                self.screen.blit(service_text, (250, 420))
                self.screen.blit(return_text, return_text_rect)
                
                # 更新顯示
                pygame.display.flip()
                
                # 事件處理
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return "QUIT"
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if return_button.collidepoint(event.pos):
                            return "MENU"
                            
                # 控制幀率
                self.clock.tick(60)
                
        except Exception as e:
            print(f"Error in show_game_over: {e}")
            return "MENU"
        
        return "MENU" 