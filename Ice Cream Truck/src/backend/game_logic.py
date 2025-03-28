import pygame
import random
import time

class Customer:
    def __init__(self):
        self.order = {
            'flavors': {},  # 確保訂單包含 'flavors' 字典
            'has_cone': False
        }
        self.wait_time = random.uniform(15, 25)  # 增加等待時間範圍
        self.arrival_time = time.time()  # 添加到達時間
        self.generate_order()
    
    def generate_order(self):
        flavors = ["Vanilla", "Chocolate", "Milk", "Mint Chocolate"]
        total_scoops = random.randint(1, 3)
        
        # 清空並重新生成訂單
        self.order['flavors'] = {}
        
        # 生成指定數量的球數
        for _ in range(total_scoops):
            flavor = random.choice(flavors)
            self.order['flavors'][flavor] = self.order['flavors'].get(flavor, 0) + 1
            
        self.order['has_cone'] = random.choice([True, False])

class GameLogic:
    def __init__(self):
        self.money = 0
        self.costs = 0
        self.customers = []
        self.freezer_ice_creams = []
        self.game_time = 0
        self.max_game_time = 180  # 3分鐘 = 180秒
        self.max_customers = 3
        # 添加統計數據
        self.served_customers = 0  # 成功服務的客人
        self.lost_customers = 0    # 走掉的客人
        self.last_customer_time = time.time()  # 記錄上次生成客人的時間
        self.customer_interval = 5  # 每5秒檢查是否需要生成新客人
        
        # 初始生成客人
        self.generate_initial_customers()

    def generate_initial_customers(self):
        # 遊戲開始時生成3個客人
        while len(self.customers) < self.max_customers:
            self.customers.append(Customer())

    def update(self, dt):
        self.game_time += dt
        
        # 檢查遊戲是否結束
        if self.game_time >= self.max_game_time:
            return True  # 返回True表示遊戲結束
            
        current_time = time.time()
        
        # 更新現有客人
        remaining_customers = []
        for customer in self.customers:
            if current_time - customer.arrival_time > customer.wait_time:
                self.lost_customers += 1
            else:
                remaining_customers.append(customer)
        self.customers = remaining_customers

        # 檢查是否需要生成新客人
        if (current_time - self.last_customer_time >= self.customer_interval and 
            len(self.customers) < self.max_customers):
            self.customers.append(Customer())
            self.last_customer_time = current_time
            
        return False  # 返回False表示遊戲繼續

    def add_customer(self):
        if len(self.customers) >= 3:
            return False
            
        # 找出空位置
        used_positions = {customer.y for customer in self.customers}
        available_positions = [y for y in self.y_positions if y not in used_positions]
        
        if available_positions:
            new_customer = Customer(20, available_positions[0])
            self.customers.append(new_customer)
            return True
        return False

    def remove_customer(self, customer):
        if customer in self.customers:
            self.customers.remove(customer)

    def draw_customers(self, screen):
        font = pygame.font.Font(None, 36)
        for customer in self.customers:
            # 繪製客人
            pygame.draw.rect(screen, (200, 200, 200), (customer.x, customer.y, 50, 50))
            
            # 繪製客人需求
            order_text = font.render(f"{customer.order}", True, (0, 0, 0))
            screen.blit(order_text, (customer.x + 60, customer.y))
            
            # 繪製等待時間
            wait_time = int(customer.wait_time - (time.time() - customer.arrival_time))
            time_text = font.render(f"等待: {wait_time}秒", True, (0, 0, 0))
            screen.blit(time_text, (customer.x + 60, customer.y + 30))
    
    def serve_customer(self, customer):
        if customer in self.customers:
            self.money += customer.total_price
            self.customer_count += 1
            self.customers.remove(customer)
    
    def calculate_costs(self, ice_cream):
        # 計算成本
        cost = 0
        for flavor, count in ice_cream['flavors'].items():
            cost += count * 5  # 每球5元
        if ice_cream['has_cone']:
            cost += 1  # 甜筒1元
        return cost
    
    def deliver_ice_cream(self, ice_cream, customer):
        # 檢查訂單是否匹配
        if (ice_cream['has_cone'] == customer.order['has_cone'] and 
            ice_cream['flavors'] == customer.order['flavors']):
            
            # 計算售價（根據球數）
            total_scoops = sum(ice_cream['flavors'].values())
            price = total_scoops * 10  # 1球10元，2球20元，3球30元
            
            self.money += price
            self.served_customers += 1
            return True
        return False
    
    def calculate_price(self, ice_cream):
        # 輔助方法：計算售價
        total_scoops = sum(ice_cream['flavors'].values())
        return total_scoops * 10
    
    def get_final_stats(self):
        return {
            'revenue': self.money,
            'costs': self.costs,
            'profit': self.money - self.costs
        }

    def get_game_data(self):
        return {
            "money": self.money,
            "customer_count": self.customer_count,
            "negative_count": self.negative_count
        } 