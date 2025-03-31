import pygame
import random

# 初始化 Pygame
pygame.init()

# 設定遊戲視窗
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("漢堡餐車遊戲")

# 顏色定義
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)

# 設定字型（使用微軟正黑體或其他支援中文字的字體）
font = pygame.font.Font("msjh.ttc", 36)  # 主要字型
small_font = pygame.font.Font("msjh.ttc", 20)  # 縮小字型
extra_small_font = pygame.font.Font("msjh.ttc", 16)  # 額外縮小字型

# 遊戲變數
starting_money = 500  # 初始金錢
money = starting_money  # 當前金錢
round_time = 60  # 每回合 60 秒
customer_interval = 5  # 每 5 秒來一位客人
waiting_time = 10  # 客人最大等待時間
rounds = 5  # 設定 5 回合
current_round = 1
customers = []
counter = 0  # 計時器
time_left = round_time  # 倒數計時器

# 食材選項與成本
ingredient_prices = {"麵包": 5, "肉餅": 10, "生菜": 3, "酸黃瓜": 4, "番茄醬": 3, "芥末醬": 3, "起司": 6}
ingredient_stock = {ingredient: 0 for ingredient in ingredient_prices}  # 初始庫存為 0
available_ingredients = list(ingredient_prices.keys())[2:]
selected_ingredients = []  # 玩家選擇的食材

# 遊戲開始前的購買食材畫面
def buy_ingredients():
    global money
    buying = True
    while buying:
        screen.fill(WHITE)
        title_text = font.render("購買食材 (按 Enter 開始遊戲)", True, BLACK)
        screen.blit(title_text, (200, 50))
        
        for i, (ingredient, price) in enumerate(ingredient_prices.items()):
            stock_text = small_font.render(f"{ingredient} ({i+1}): {ingredient_stock[ingredient]} 個 | {price} 元", True, BLACK)
            screen.blit(stock_text, (100, 150 + i * 30))
        
        money_text = font.render(f"金錢: {money} 元", True, BLACK)
        screen.blit(money_text, (20, 20))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    buying = False
                elif pygame.K_1 <= event.key <= pygame.K_7:
                    ingredient = list(ingredient_prices.keys())[event.key - pygame.K_1]
                    if money >= ingredient_prices[ingredient]:
                        money -= ingredient_prices[ingredient]
                        ingredient_stock[ingredient] += 1

buy_ingredients()

def show_result():
    screen.fill(WHITE)
    money_diff = money - starting_money
    money_color = GREEN if money_diff >= 0 else RED
    result_text = font.render(f"遊戲結束！最終金額: {money} 元", True, BLACK)
    diff_text = font.render(f"({money_diff:+})", True, money_color)
    screen.blit(result_text, (200, 250))
    screen.blit(diff_text, (200 + result_text.get_width() + 10, 250))  # 調整間距
    pygame.display.flip()
    pygame.time.delay(3000)  # 顯示結算畫面 3 秒後退出

def generate_order():
    return ["麵包", "肉餅"] + random.sample(available_ingredients, random.randint(0, len(available_ingredients)))

def calculate_price(ingredients):
    return sum(ingredient_prices[i] for i in ingredients) + 5  # 售價 = 成本 + 利潤

# 遊戲主迴圈
running = True
clock = pygame.time.Clock()
while running:
    screen.fill(WHITE)
    
    # 生成客人
    if counter % (customer_interval * 30) == 0:
        customers.append({"order": generate_order()})
    counter += 1
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if pygame.K_1 <= event.key <= pygame.K_7:
                ingredient = list(ingredient_prices.keys())[event.key - pygame.K_1]
                if ingredient_stock[ingredient] > 0:
                    selected_ingredients.append(ingredient)
                    ingredient_stock[ingredient] -= 1
            elif event.key == pygame.K_RETURN:
                if "麵包" in selected_ingredients and "肉餅" in selected_ingredients:
                    if customers:
                        customer = customers.pop(0)
                        if sorted(selected_ingredients) == sorted(customer["order"]):
                            profit = calculate_price(selected_ingredients)
                            money += profit
                        selected_ingredients = []  # 重置選擇
    
    # 更新倒數計時
    time_left -= 1 / 30
    if time_left <= 0:
        running = False
    
    # 顯示時間
    time_text = small_font.render(f"時間: {int(time_left)} 秒", True, BLACK)
    screen.blit(time_text, (20, 20))
    
    # 顯示客人點餐資訊
    for i, customer in enumerate(customers):
        order_text = small_font.render(f"客人點單: {', '.join(customer['order'])}", True, BLACK)
        screen.blit(order_text, (20, 50 + i * 30))
    
    # 顯示食材庫存與鍵盤數字
    for i, (ingredient, stock) in enumerate(ingredient_stock.items()):
        stock_text = extra_small_font.render(f"{ingredient} ({i+1}): {stock} 個", True, BLACK)
        screen.blit(stock_text, (600, 50 + i * 20))
    
    # 顯示已選擇的食材
    selected_text = small_font.render(f"已選擇: {', '.join(selected_ingredients)}", True, BLACK)
    screen.blit(selected_text, (20, 500))
    
    pygame.display.flip()
    clock.tick(30)

show_result()
pygame.quit()


