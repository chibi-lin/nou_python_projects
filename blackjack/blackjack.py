import pygame
import random
import time
import os

# Initialize pygame
pygame.init()
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blackjack")
clock = pygame.time.Clock()

# Color scheme
COLORS = {
    'background_top': (34, 139, 34),
    'background_bottom': (20, 80, 20),
    'card': (255, 255, 255),
    'text': (236, 240, 241),
    'button': (50, 50, 50, 200),
    'button_hover': (80, 80, 80, 220),
    'win': (46, 204, 113),
    'lose': (231, 76, 60),
    'gold': (241, 196, 15),
    'shadow': (0, 0, 0, 100),
    'frame': (255, 215, 0, 180),
    'info_bg': (20, 80, 20, 180)
}

# Check and create folder
if not os.path.exists("cards"):
    os.makedirs("cards")

# Load fonts
FONT = pygame.font.SysFont("Segoe UI Symbol", 26, bold=True)
FONT_LARGE = pygame.font.SysFont("Segoe UI Symbol", 48, bold=True)
CARD_FONT = pygame.font.SysFont("Segoe UI Symbol", 24, bold=True)

# Deck
suits = ["♠", "♥", "♦", "♣"]
ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
deck = [(suit, rank) for suit in suits for rank in ranks]

# Calculate card value
def card_value(card):
    rank = card[1]
    if rank in ["J", "Q", "K"]: return 10
    elif rank == "A": return 11
    return int(rank)

# Create card surface
def create_card_surface(card, is_back=False, angle=0):
    card_width, card_height = 100, 150
    surface = pygame.Surface((int(card_width * 1.3), int(card_height * 1.3)), pygame.SRCALPHA)
    
    shadow = pygame.Surface((card_width, card_height), pygame.SRCALPHA)
    pygame.draw.rect(shadow, COLORS['shadow'], (0, 0, card_width, card_height), border_radius=10)
    
    card_surface = pygame.Surface((card_width, card_height), pygame.SRCALPHA)
    pygame.draw.rect(card_surface, COLORS['card'], (0, 0, card_width, card_height), border_radius=10)
    pygame.draw.rect(card_surface, (200, 200, 200), (0, 0, card_width, card_height), 2, border_radius=10)
    
    if is_back:
        pattern_color = (50, 50, 50)
        for i in range(0, card_width, 15):
            for j in range(0, card_height, 15):
                pygame.draw.rect(card_surface, pattern_color, (i, j, 8, 8))
    else:
        suit_color = (255, 0, 0) if card[0] in ["♥", "♦"] else (0, 0, 0)
        rank_text = CARD_FONT.render(card[1], True, suit_color)
        suit_text = CARD_FONT.render(card[0], True, suit_color)
        
        corners = [(10, 5), (card_width-30, 5), 
                  (10, card_height-40), (card_width-30, card_height-40)]
        for corner in corners:
            card_surface.blit(rank_text, corner)
        
        center_text = pygame.transform.scale(suit_text, 
            (int(suit_text.get_width()*1.2), int(suit_text.get_height()*1.2)))
        card_surface.blit(center_text, (card_width//2 - center_text.get_width()//2,
                                      card_height//2 - center_text.get_height()//2 - 10))
    
    rotated_shadow = pygame.transform.rotate(shadow, angle)
    rotated_card = pygame.transform.rotate(card_surface, angle)
    
    shadow_pos = ((surface.get_width() - rotated_shadow.get_width())//2 + 5,
                 (surface.get_height() - rotated_shadow.get_height())//2 + 5)
    card_pos = ((surface.get_width() - rotated_card.get_width())//2,
                (surface.get_height() - rotated_card.get_height())//2)
    
    surface.blit(rotated_shadow, shadow_pos)
    surface.blit(rotated_card, card_pos)
    return surface

# Deal animation
def animate_deal(card_surface, start_pos, end_pos, speed=20):
    current_pos = list(start_pos)
    scale = 0.5
    fixed_angle = random.randint(-5, 5)
    
    initial_screen = screen.copy()
    
    while abs(current_pos[0] - end_pos[0]) > speed or abs(current_pos[1] - end_pos[1]) > speed or scale < 1:
        if current_pos[0] < end_pos[0]: current_pos[0] += speed
        if current_pos[0] > end_pos[0]: current_pos[0] -= speed
        if current_pos[1] < end_pos[1]: current_pos[1] += speed
        if current_pos[1] > end_pos[1]: current_pos[1] -= speed
        scale = min(1, scale + 0.1)
        
        scaled_card = pygame.transform.scale(card_surface, 
            (int(card_surface.get_width() * scale), int(card_surface.get_height() * scale)))
        
        screen.blit(initial_screen, (0, 0))
        screen.blit(scaled_card, current_pos)
        pygame.display.flip()
        clock.tick(60)
    
    return end_pos, fixed_angle

# Create button
def create_button(text, width=200, height=50, color=None, hover=False):
    if color is None:
        color = COLORS['button_hover'] if hover else COLORS['button']
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(surface, color, (0, 0, width, height), border_radius=20)
    pygame.draw.rect(surface, (255, 255, 255, 30), (0, 0, width, height), 2, border_radius=20)
    text_surface = FONT.render(text, True, COLORS['text'])
    text_rect = text_surface.get_rect(center=(width//2, height//2))
    surface.blit(text_surface, text_rect)
    return surface

# Button class
class Button:
    def __init__(self, x, y, text, width=200, height=50):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.width = width
        self.height = height
        self.hovered = False
        
    def draw(self, screen):
        button_surface = create_button(self.text, self.width, self.height, hover=self.hovered)
        screen.blit(button_surface, self.rect)
        
    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)
        return self.hovered
        
    def is_clicked(self, mouse_pos, mouse_click):
        return self.rect.collidepoint(mouse_pos) and mouse_click

# Gradient background
def draw_background():
    for y in range(HEIGHT):
        r = int(COLORS['background_top'][0] + (COLORS['background_bottom'][0] - COLORS['background_top'][0]) * y / HEIGHT)
        g = int(COLORS['background_top'][1] + (COLORS['background_bottom'][1] - COLORS['background_top'][1]) * y / HEIGHT)
        b = int(COLORS['background_top'][2] + (COLORS['background_bottom'][2] - COLORS['background_top'][2]) * y / HEIGHT)
        pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

# Container structure
class Container:
    def __init__(self, x, y, width, height, padding=20):
        self.rect = pygame.Rect(x, y, width, height)
        self.padding = padding
        self.items = []
        self.buttons = []

    def add_item(self, surface, offset_y):
        self.items.append((surface, offset_y))
    
    def add_button(self, button):
        self.buttons.append(button)

    def draw(self, screen):
        pygame.draw.rect(screen, COLORS['info_bg'], self.rect, 0, border_radius=10)
        pygame.draw.rect(screen, COLORS['frame'], self.rect, 3, border_radius=10)
        
        if self.items:
            total_height = sum(item[1] for item in self.items) - self.items[0][1] + self.items[0][0].get_height()
            y_start = self.rect.y + (self.rect.height - total_height) // 2
            y_pos = y_start
            for surface, offset in self.items:
                screen.blit(surface, (self.rect.x + (self.rect.width - surface.get_width()) // 2, y_pos))
                y_pos += offset
        
        for button in self.buttons:
            button.draw(screen)

# Slider class
class Slider:
    def __init__(self, x, y, width, height, min_value, max_value, initial_value, label, value_format="{:.0f}"):
        self.rect = pygame.Rect(x, y, width, height)
        self.track_rect = pygame.Rect(x, y + height//2 - 4, width, 8)
        self.handle_radius = 12
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value
        self.dragging = False
        self.label = label
        self.value_format = value_format
        self.update_handle_pos()
    
    def update_handle_pos(self):
        value_range = self.max_value - self.min_value
        if value_range == 0:
            value_range = 1
        value_percent = (self.value - self.min_value) / value_range
        self.handle_x = self.rect.x + int(value_percent * self.rect.width)
        self.handle_y = self.rect.y + self.rect.height // 2
    
    def draw(self, screen):
        label_surface = FONT.render(self.label, True, COLORS['text'])
        screen.blit(label_surface, (self.rect.x, self.rect.y - 30))
        
        value_text = self.value_format.format(self.value)
        value_surface = FONT.render(value_text, True, COLORS['gold'])
        screen.blit(value_surface, (self.rect.right - value_surface.get_width(), self.rect.y - 30))
        
        pygame.draw.rect(screen, (100, 100, 100), self.track_rect, border_radius=4)
        
        filled_width = self.handle_x - self.rect.x
        if filled_width > 0:
            filled_rect = pygame.Rect(self.rect.x, self.track_rect.y, filled_width, self.track_rect.height)
            pygame.draw.rect(screen, COLORS['gold'], filled_rect, border_radius=4)
        
        pygame.draw.circle(screen, COLORS['text'], (self.handle_x, self.handle_y), self.handle_radius)
        pygame.draw.circle(screen, COLORS['gold'], (self.handle_x, self.handle_y), self.handle_radius - 2)
    
    def is_handle_clicked(self, pos):
        handle_rect = pygame.Rect(
            self.handle_x - self.handle_radius,
            self.handle_y - self.handle_radius,
            self.handle_radius * 2,
            self.handle_radius * 2
        )
        return handle_rect.collidepoint(pos)
    
    def is_track_clicked(self, pos):
        return self.track_rect.collidepoint(pos)
    
    def set_value_from_pos(self, x_pos):
        pos_percent = max(0, min(1, (x_pos - self.rect.x) / self.rect.width))
        self.value = self.min_value + pos_percent * (self.max_value - self.min_value)
        self.update_handle_pos()
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_handle_clicked(event.pos):
                self.dragging = True
                return True
            elif self.is_track_clicked(event.pos):
                self.set_value_from_pos(event.pos[0])
                self.dragging = True
                return True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.set_value_from_pos(event.pos[0])
            return True
        return False

# Start screen
def show_start_screen():
    draw_background()
    
    title = FONT_LARGE.render("Blackjack", True, COLORS['gold'])
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
    
    container = Container(WIDTH//2 - 300, HEIGHT//2 - 200, 600, 400, padding=30)
    
    instructions = [
        "Game Rules:",
        "1. Get close to 21 without going over",
        "2. 2-10 = face value, J/Q/K = 10, A = 11",
        "3. Click 'Hit' for another card, 'Stand' to stop",
        "4. Dealer must hit on 16 or less"
    ]
    
    y_offset = 40
    for i, line in enumerate(instructions):
        text = FONT.render(line, True, COLORS['text'])
        if i == 0:
            container.add_item(text, y_offset)
        else:
            padded_surface = pygame.Surface((container.rect.width - 60, text.get_height()), pygame.SRCALPHA)
            padded_surface.blit(text, (40, 0))
            container.add_item(padded_surface, y_offset)
    
    button_x = container.rect.x + (container.rect.width - 200) // 2
    button_y = container.rect.y + container.rect.height - 80
    start_button = Button(button_x, button_y, "Start Game")
    container.add_button(start_button)
    
    waiting = True
    while waiting:
        mouse_pos = pygame.mouse.get_pos()
        start_button.check_hover(mouse_pos)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_button.is_clicked(mouse_pos, True):
                    waiting = False
        
        draw_background()
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
        container.draw(screen)
        pygame.display.flip()
        clock.tick(60)
    
    return True

# Betting screen
def show_betting_screen(balance):
    draw_background()
    
    title = FONT_LARGE.render("Place Your Bet", True, COLORS['gold'])
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
    
    balance_text = FONT.render(f"Your Balance: ${balance}", True, COLORS['text'])
    screen.blit(balance_text, (WIDTH//2 - balance_text.get_width()//2, 120))
    
    container = Container(WIDTH//2 - 300, HEIGHT//2 - 180, 600, 380, padding=30)
    
    amount_slider = Slider(
        container.rect.x + 50, 
        container.rect.y + 60,
        container.rect.width - 100, 
        40, 
        10, 
        min(balance, 500),
        50,
        "Bet Amount: $",
        "${:.0f}"
    )
    
    multiplier_slider = Slider(
        container.rect.x + 50, 
        container.rect.y + 140,
        container.rect.width - 100, 
        40, 
        1, 
        5,
        1,
        "Multiplier:",
        "{:.1f}x"
    )
    
    bet_button = Button(
        container.rect.x + (container.rect.width - 200) // 2,
        container.rect.y + 220,
        "Place Bet"
    )
    
    restart_button = Button(
        container.rect.x + (container.rect.width - 200) // 2,
        container.rect.y + 280,
        "Restart Game"
    )
    
    container.add_button(bet_button)
    container.add_button(restart_button)
    
    total_bet = amount_slider.value
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        bet_button.check_hover(mouse_pos)
        restart_button.check_hover(mouse_pos)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None, None
            amount_slider.handle_event(event)
            multiplier_slider.handle_event(event)
            total_bet = amount_slider.value
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if bet_button.is_clicked(mouse_pos, True):
                    if total_bet <= balance:
                        return total_bet, multiplier_slider.value
                elif restart_button.is_clicked(mouse_pos, True):
                    return "restart", None
        
        draw_background()
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
        screen.blit(balance_text, (WIDTH//2 - balance_text.get_width()//2, 120))
        container.draw(screen)
        amount_slider.draw(screen)
        multiplier_slider.draw(screen)
        
        total_text = FONT.render(f"Total Bet: ${total_bet:.0f}", True, COLORS['gold'])
        screen.blit(total_text, (container.rect.x + (container.rect.width - total_text.get_width()) // 2, container.rect.y + 180))
        
        if total_bet > balance:
            disabled_surface = pygame.Surface((bet_button.width, bet_button.height), pygame.SRCALPHA)
            disabled_surface.fill((100, 100, 100, 150))
            screen.blit(disabled_surface, bet_button.rect)
        
        pygame.display.flip()
        clock.tick(60)

# End menu
def show_end_menu(player_total, dealer_total, balance, bet, multiplier, rounds):
    winnings = 0
    if player_total > 21:
        result_text = "Bust! You lose!"
        winnings = -bet
    elif dealer_total > 21 or player_total > dealer_total:
        result_text = "You win!"
        winnings = bet * multiplier
    else:
        result_text = "Dealer wins!"
        winnings = -bet
    
    balance += winnings
    
    draw_background()
    title = FONT_LARGE.render("Round Result", True, COLORS['gold'])
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
    
    round_info = FONT.render(f"Round {rounds}/10", True, COLORS['text'])
    screen.blit(round_info, (WIDTH//2 - round_info.get_width()//2, 120))
    
    container = Container(WIDTH//2 - 300, HEIGHT//2 - 180, 600, 380, padding=30)
    
    points = FONT.render(f"Your Points: {player_total}  Dealer: {dealer_total}", True, COLORS['gold'])
    result = FONT.render(result_text, True, COLORS['win'] if winnings > 0 else COLORS['lose'])
    winnings_text = FONT.render(f"Winnings: ${winnings}", True, COLORS['text'])
    
    container.add_item(points, 40)
    container.add_item(result, 40)
    container.add_item(winnings_text, 60)
    
    button_x = container.rect.x + (container.rect.width - 200) // 2
    next_button = Button(button_x, container.rect.y + 250, "Next Round")
    exit_button = Button(button_x, container.rect.y + 310, "Exit")
    
    container.add_button(next_button)
    container.add_button(exit_button)
    
    next_disabled = balance <= 0 or rounds >= 10
    
    if rounds >= 10:
        round_complete_text = FONT.render("10 rounds completed! Click Exit to see final results.", True, COLORS['gold'])
        container.add_item(round_complete_text, 60)
    
    action = None
    
    while action is None:
        mouse_pos = pygame.mouse.get_pos()
        next_button.check_hover(mouse_pos)
        exit_button.check_hover(mouse_pos)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "exit", balance
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if next_button.is_clicked(mouse_pos, True) and not next_disabled:
                    action = "next"
                elif exit_button.is_clicked(mouse_pos, True):
                    action = "complete" if rounds >= 10 else "exit"
        
        draw_background()
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
        screen.blit(round_info, (WIDTH//2 - round_info.get_width()//2, 120))
        container.draw(screen)
        
        if next_disabled:
            disabled_surface = pygame.Surface((next_button.width, next_button.height), pygame.SRCALPHA)
            disabled_surface.fill((100, 100, 100, 150))
            screen.blit(disabled_surface, next_button.rect)
        
        pygame.display.flip()
        clock.tick(60)
    
    return action, balance

# Final result screen
def show_final_result(balance, initial_balance, rounds_completed=10):
    draw_background()
    
    title = FONT_LARGE.render("Game Over - Final Result", True, COLORS['gold'])
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
    
    rounds_text = FONT.render(f"Rounds Completed: {rounds_completed}", True, COLORS['text'])
    screen.blit(rounds_text, (WIDTH//2 - rounds_text.get_width()//2, 120))
    
    container = Container(WIDTH//2 - 300, HEIGHT//2 - 180, 600, 380, padding=30)
    
    initial_text = FONT.render(f"Initial Balance: ${initial_balance}", True, COLORS['text'])
    final_text = FONT.render(f"Final Balance: ${balance}", True, COLORS['text'])
    profit_text = FONT.render(f"Profit: ${balance - initial_balance}", True, 
                             COLORS['win'] if balance > initial_balance else COLORS['lose'])
    
    container.add_item(initial_text, 60)
    container.add_item(final_text, 50)
    container.add_item(profit_text, 60)
    
    button_x = container.rect.x + (container.rect.width - 200) // 2
    continue_button = Button(button_x, container.rect.y + 220, "Continue Game")
    restart_button = Button(button_x, container.rect.y + 280, "Restart Game")
    exit_button = Button(button_x, container.rect.y + 340, "Exit")
    
    container.add_button(continue_button)
    container.add_button(restart_button)
    container.add_button(exit_button)
    
    result = None
    
    while result is None:
        mouse_pos = pygame.mouse.get_pos()
        continue_button.check_hover(mouse_pos)
        restart_button.check_hover(mouse_pos)
        exit_button.check_hover(mouse_pos)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "exit"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if continue_button.is_clicked(mouse_pos, True):
                    result = "continue"
                elif restart_button.is_clicked(mouse_pos, True):
                    result = "restart"
                elif exit_button.is_clicked(mouse_pos, True):
                    result = "exit"
        
        draw_background()
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
        screen.blit(rounds_text, (WIDTH//2 - rounds_text.get_width()//2, 120))
        container.draw(screen)
        pygame.display.flip()
        clock.tick(60)
    
    return result

# Main game
def main():
    balance = 1000
    initial_balance = balance
    rounds = 0
    total_rounds = 0
    
    show_game_rules = True
    game_running = True
    
    while game_running:
        rounds = 0
        
        while rounds < 10 and balance > 0 and game_running:
            if show_game_rules:
                if not show_start_screen():
                    return
                show_game_rules = False
            
            bet, multiplier = show_betting_screen(balance)
            
            if bet == "restart":
                balance = 1000
                initial_balance = balance
                rounds = 0
                total_rounds = 0
                show_game_rules = True
                continue
            elif bet is None:
                game_running = False
                break
            
            bet = round(bet)
            multiplier = round(multiplier * 10) / 10
            
            rounds += 1
            total_rounds += 1
            random.shuffle(deck)
            player_hand = []
            dealer_hand = []
            player_card_angles = []
            dealer_card_angles = []
            deck_pos = (50, 50)
            
            draw_background()
            dealer_frame = pygame.Rect(WIDTH//2 - 340, 150, 680, 200)
            player_frame = pygame.Rect(WIDTH//2 - 340, 400, 680, 200)
            
            title = FONT_LARGE.render(f"Round {rounds}/10", True, COLORS['gold'])
            screen.blit(title, (WIDTH//2 - title.get_width()//2, 20))
            
            balance_text = FONT.render(f"Balance: ${balance}", True, COLORS['text'])
            screen.blit(balance_text, (20, 20))
            
            total_rounds_text = FONT.render(f"Total Rounds: {total_rounds}", True, COLORS['text'])
            screen.blit(total_rounds_text, (WIDTH - total_rounds_text.get_width() - 20, 20))
            
            pygame.draw.rect(screen, COLORS['frame'], dealer_frame, 3, border_radius=15)
            dealer_label = FONT.render("Dealer", True, COLORS['text'])
            screen.blit(dealer_label, (dealer_frame.x + dealer_frame.width//2 - dealer_label.get_width()//2, dealer_frame.y - 40))
            
            pygame.draw.rect(screen, COLORS['frame'], player_frame, 3, border_radius=15)
            player_label = FONT.render("Player", True, COLORS['text'])
            screen.blit(player_label, (player_frame.x + player_frame.width//2 - player_label.get_width()//2, player_frame.y - 40))
            
            pygame.display.flip()
            
            for i in range(2):
                player_card = deck.pop()
                player_pos = (player_frame.x + 50 + i * 120, player_frame.y + 25)
                player_card_surface = create_card_surface(player_card, angle=0)
                player_pos, angle = animate_deal(player_card_surface, deck_pos, player_pos)
                player_hand.append(player_card)
                player_card_angles.append(angle)
                
                dealer_card = deck.pop()
                dealer_pos = (dealer_frame.x + 50 + i * 120, dealer_frame.y + 25)
                dealer_card_surface = create_card_surface(dealer_card, is_back=(i == 1), angle=0)
                dealer_pos, angle = animate_deal(dealer_card_surface, deck_pos, dealer_pos)
                dealer_hand.append(dealer_card)
                dealer_card_angles.append(angle)
                pygame.time.wait(100)
            
            player_total = sum(card_value(card) for card in player_hand)
            running = True
            
            hit_button = Button(player_frame.right + 70, player_frame.y + 120, "Hit", 100, 50)
            stand_button = Button(player_frame.right + 70, player_frame.y + 180, "Stand", 100, 50)
            
            while running and player_total <= 21:
                mouse_pos = pygame.mouse.get_pos()
                hit_button.check_hover(mouse_pos)
                stand_button.check_hover(mouse_pos)
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if hit_button.is_clicked(mouse_pos, True):
                            new_card = deck.pop()
                            pos = (player_frame.x + 50 + len(player_hand) * 120, player_frame.y + 25)
                            card_surface = create_card_surface(new_card, angle=0)
                            pos, angle = animate_deal(card_surface, deck_pos, pos)
                            player_hand.append(new_card)
                            player_card_angles.append(angle)
                            player_total += card_value(new_card)
                        elif stand_button.is_clicked(mouse_pos, True):
                            running = False
                
                draw_background()
                screen.blit(title, (WIDTH//2 - title.get_width()//2, 20))
                screen.blit(balance_text, (20, 20))
                screen.blit(total_rounds_text, (WIDTH - total_rounds_text.get_width() - 20, 20))
                
                pygame.draw.rect(screen, COLORS['frame'], dealer_frame, 3, border_radius=15)
                screen.blit(dealer_label, (dealer_frame.x + dealer_frame.width//2 - dealer_label.get_width()//2, dealer_frame.y - 40))
                
                for i, card in enumerate(dealer_hand):
                    card_surface = create_card_surface(card, is_back=(i == 1), angle=dealer_card_angles[i])
                    screen.blit(card_surface, (dealer_frame.x + 50 + i * 120, dealer_frame.y + 25))
                
                pygame.draw.rect(screen, COLORS['frame'], player_frame, 3, border_radius=15)
                screen.blit(player_label, (player_frame.x + player_frame.width//2 - player_label.get_width()//2, player_frame.y - 40))
                
                for i, card in enumerate(player_hand):
                    card_surface = create_card_surface(card, angle=player_card_angles[i])
                    screen.blit(card_surface, (player_frame.x + 50 + i * 120, player_frame.y + 25))
                
                info_container = Container(player_frame.right + 20, player_frame.y, 250, 100, padding=20)
                score_text = FONT.render(f"Points: {player_total}", True, COLORS['gold'])
                bet_text = FONT.render(f"Bet: ${bet} (x{multiplier})", True, COLORS['text'])
                
                info_container.add_item(score_text, 40)
                info_container.add_item(bet_text, 40)
                info_container.draw(screen)
                
                hit_button.draw(screen)
                stand_button.draw(screen)
                
                pygame.display.flip()
                clock.tick(60)
            
            dealer_total = sum(card_value(card) for card in dealer_hand)
            while dealer_total < 17:
                new_card = deck.pop()
                pos = (dealer_frame.x + 50 + len(dealer_hand) * 120, dealer_frame.y + 25)
                card_surface = create_card_surface(new_card, angle=0)
                pos, angle = animate_deal(card_surface, deck_pos, pos)
                dealer_hand.append(new_card)
                dealer_card_angles.append(angle)
                dealer_total += card_value(new_card)
                
                draw_background()
                screen.blit(title, (WIDTH//2 - title.get_width()//2, 20))
                screen.blit(balance_text, (20, 20))
                screen.blit(total_rounds_text, (WIDTH - total_rounds_text.get_width() - 20, 20))
                
                pygame.draw.rect(screen, COLORS['frame'], dealer_frame, 3, border_radius=15)
                screen.blit(dealer_label, (dealer_frame.x + dealer_frame.width//2 - dealer_label.get_width()//2, dealer_frame.y - 40))
                
                for i, card in enumerate(dealer_hand):
                    card_surface = create_card_surface(card, angle=dealer_card_angles[i])
                    screen.blit(card_surface, (dealer_frame.x + 50 + i * 120, dealer_frame.y + 25))
                
                pygame.draw.rect(screen, COLORS['frame'], player_frame, 3, border_radius=15)
                screen.blit(player_label, (player_frame.x + player_frame.width//2 - player_label.get_width()//2, player_frame.y - 40))
                
                for i, card in enumerate(player_hand):
                    card_surface = create_card_surface(card, angle=player_card_angles[i])
                    screen.blit(card_surface, (player_frame.x + 50 + i * 120, player_frame.y + 25))
                
                dealer_info = Container(player_frame.right + 20, dealer_frame.y, 250, 80, padding=20)
                dealer_score = FONT.render(f"Dealer Points: {dealer_total}", True, COLORS['gold'])
                dealer_info.add_item(dealer_score, 0)
                dealer_info.draw(screen)
                
                pygame.display.flip()
                pygame.time.wait(300)
            
            action, balance = show_end_menu(player_total, dealer_total, balance, bet, multiplier, rounds)
            if action == "exit":
                game_running = False
                break
            elif action == "complete":
                break
        
        if game_running:
            result = show_final_result(balance, initial_balance, total_rounds)
            if result == "continue":
                rounds = 0
            elif result == "restart":
                balance = 1000
                initial_balance = balance
                total_rounds = 0
                show_game_rules = True
            else:
                game_running = False

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"遊戲發生錯誤: {e}")
        import traceback
        traceback.print_exc()
    finally:
        pygame.quit()