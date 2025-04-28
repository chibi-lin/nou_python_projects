import pygame
import sys
from pygame.locals import *
import game  # 導入遊戲模組

# 初始化 Pygame
pygame.init()

# 定義所有變數
# 視窗與遊戲設定
WIDTH = 800
HEIGHT = 600
FPS = 60

# 字體設定
FONT = pygame.font.SysFont(None, 48)  # 按鈕文字
LARGE_FONT = pygame.font.SysFont(None, 72)  # 大字體
SMALL_FONT = pygame.font.SysFont(None, 36)  # 滑桿標籤

# 音量初始值
MUSIC_VOLUME = 0.3
SOUND_VOLUME = 0.3

# 按鈕與滑桿座標 (x, y) 格式
START_BUTTON_POS = (WIDTH // 2 - 125, HEIGHT // 2 + 10)  # (275, 310)
START_BUTTON_SIZE = (250, 60)
START_BUTTON_TEXT_POS = (WIDTH // 2 - 85, HEIGHT // 2 + 25)  # (340, 320)

SETTINGS_BUTTON_POS = (WIDTH // 2 - 125, HEIGHT // 2 + 90)  # (275, 390)
SETTINGS_BUTTON_SIZE = (250, 60)
SETTINGS_BUTTON_TEXT_POS = (WIDTH // 2 - 70, HEIGHT // 2 + 105)  # (340, 400)

EXIT_BUTTON_POS = (WIDTH // 2 - 125, HEIGHT // 2 + 170)  # (275, 470)
EXIT_BUTTON_SIZE = (250, 60)
EXIT_BUTTON_TEXT_POS = (WIDTH // 2 - 85, HEIGHT // 2 + 185)  # (340, 480)

MAIN_MENU_BUTTON_POS = (WIDTH // 2 - 125, HEIGHT // 2 + 100)  # (275, 400)
MAIN_MENU_BUTTON_SIZE = (250, 60)
MAIN_MENU_BUTTON_TEXT_POS = (WIDTH // 2 - 85, HEIGHT // 2 + 115)  # (340, 410)

MUSIC_SLIDER_POS = (WIDTH // 2 - 35, HEIGHT // 2 - 40)  # (300, 280)
MUSIC_SLIDER_SIZE = (200, 20)
MUSIC_SLIDER_LABEL_POS = (MUSIC_SLIDER_POS[0] - 180, MUSIC_SLIDER_POS[1] - 5)  # (120, 275)

SOUND_SLIDER_POS = (WIDTH // 2 - 35, HEIGHT // 2 + 10)  # (300, 320)
SOUND_SLIDER_SIZE = (200, 20)
SOUND_SLIDER_LABEL_POS = (SOUND_SLIDER_POS[0] - 180, SOUND_SLIDER_POS[1] - 5)  # (120, 315)

SETTINGS_TITLE_POS = (WIDTH // 2 - 80, HEIGHT // 2 - 250)  # (320, 50)

# 設定遊戲視窗
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Heavy Eater - Main Menu")
clock = pygame.time.Clock()

# 初始化音效模組
pygame.mixer.init()

# 載入背景音樂
pygame.mixer.music.load('sound/bgm.mp3')
pygame.mixer.music.set_volume(MUSIC_VOLUME)
pygame.mixer.music.play(-1)

# 載入音效
click_sound = pygame.mixer.Sound("sound/click.mp3")
bye_bye_sound = pygame.mixer.Sound("sound/bye_bye.mp3")
click_sound.set_volume(SOUND_VOLUME)
bye_bye_sound.set_volume(SOUND_VOLUME)

# 全局音量變數
music_volume = MUSIC_VOLUME
sound_volume = SOUND_VOLUME

# 滑桿初始位置
music_slider_pos = MUSIC_SLIDER_POS[0] + (music_volume * MUSIC_SLIDER_SIZE[0])
sound_slider_pos = SOUND_SLIDER_POS[0] + (sound_volume * SOUND_SLIDER_SIZE[0])
dragging_music_slider = False
dragging_sound_slider = False

# 檢查表面是否有效
def check_surface(surface, name):
    if surface.get_width() == 0 or surface.get_height() == 0:
        print(f"Image {name} failed to load: Invalid surface")
        sys.exit()
    expected_width, expected_height = WIDTH, HEIGHT
    if name in ['loading'] and (surface.get_width() != expected_width or surface.get_height() != expected_height):
        print(f"Warning: Image {name} size is {surface.get_width()}x{surface.get_height()}, expected {expected_width}x{expected_height}")
    return surface

# 載入圖片資源
try:
    loading_img = check_surface(pygame.image.load('assest/loading.png').convert_alpha(), 'loading')
except FileNotFoundError as e:
    print(f"Failed to load image: {e}")
    sys.exit()

# 定義按鈕區域
start_button = pygame.Rect(*START_BUTTON_POS, *START_BUTTON_SIZE)
settings_button = pygame.Rect(*SETTINGS_BUTTON_POS, *SETTINGS_BUTTON_SIZE)
exit_button = pygame.Rect(*EXIT_BUTTON_POS, *EXIT_BUTTON_SIZE)
main_menu_button = pygame.Rect(*MAIN_MENU_BUTTON_POS, *MAIN_MENU_BUTTON_SIZE)

# 滑桿區域
music_slider_rect = pygame.Rect(*MUSIC_SLIDER_POS, *MUSIC_SLIDER_SIZE)
sound_slider_rect = pygame.Rect(*SOUND_SLIDER_POS, *SOUND_SLIDER_SIZE)

# 繪製文字的函數
def draw_text(text, pos, font=FONT, color=(0, 0, 0)):
    img = font.render(text, True, color)
    screen.blit(img, pos)

# 繪製滑桿
def draw_slider(rect, pos, label, label_pos, font=SMALL_FONT):
    pygame.draw.rect(screen, (150, 150, 150), rect, border_radius=5)
    pygame.draw.circle(screen, (50, 100, 150), (int(pos), rect.centery), 10)
    draw_text(label, label_pos, font, (255, 255, 255))

# 繪製主畫面
def draw_main_menu():
    screen.blit(loading_img, (0, 0))
    
    mouse_pos = pygame.mouse.get_pos()
    start_color = (100, 150, 200) if start_button.collidepoint(mouse_pos) else (50, 100, 150)
    settings_color = (100, 150, 200) if settings_button.collidepoint(mouse_pos) else (50, 100, 150)
    exit_color = (100, 150, 200) if exit_button.collidepoint(mouse_pos) else (50, 100, 150)

    pygame.draw.rect(screen, start_color, start_button, border_radius=15)
    draw_text("Start Game", START_BUTTON_TEXT_POS, color=(255, 255, 255))
    pygame.draw.rect(screen, settings_color, settings_button, border_radius=15)
    draw_text("Settings", SETTINGS_BUTTON_TEXT_POS, color=(255, 255, 255))
    pygame.draw.rect(screen, exit_color, exit_button, border_radius=15)
    draw_text("Exit Game", EXIT_BUTTON_TEXT_POS, color=(255, 255, 255))

# 繪製設定選單
def draw_settings_menu():
    global music_volume, sound_volume, music_slider_pos, sound_slider_pos

    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    
    draw_text("Settings", SETTINGS_TITLE_POS, LARGE_FONT, (255, 255, 255))
    
    draw_slider(music_slider_rect, music_slider_pos, "Music Volume", MUSIC_SLIDER_LABEL_POS)
    draw_slider(sound_slider_rect, sound_slider_pos, "Sound Volume", SOUND_SLIDER_LABEL_POS)
    
    mouse_pos = pygame.mouse.get_pos()
    main_menu_color = (100, 150, 200) if main_menu_button.collidepoint(mouse_pos) else (50, 100, 150)
    pygame.draw.rect(screen, main_menu_color, main_menu_button, border_radius=15)
    draw_text("Main Menu", MAIN_MENU_BUTTON_TEXT_POS, color=(255, 255, 255))

# 主畫面迴圈
def main_menu():
    global music_volume, sound_volume, music_slider_pos, sound_slider_pos, dragging_music_slider, dragging_sound_slider

    in_main_menu = True
    in_settings = False

    while in_main_menu:
        if in_settings:
            draw_settings_menu()
        else:
            draw_main_menu()

        for event in pygame.event.get():
            if event.type == QUIT:
                bye_bye_sound.play()
                pygame.time.delay(int(bye_bye_sound.get_length() * 1000))
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if in_settings:
                    music_slider_circle = pygame.Rect(music_slider_pos - 10, music_slider_rect.y - 10, 20, 20)
                    sound_slider_circle = pygame.Rect(sound_slider_pos - 10, sound_slider_rect.y - 10, 20, 20)
                    if music_slider_circle.collidepoint(pos):
                        dragging_music_slider = True
                    elif sound_slider_circle.collidepoint(pos):
                        dragging_sound_slider = True
                    elif main_menu_button.collidepoint(pos):
                        click_sound.play()
                        in_settings = False
                else:
                    if start_button.collidepoint(pos):
                        click_sound.play()
                        in_main_menu = False
                        game.main(music_volume, sound_volume)
                        in_main_menu = True
                    elif settings_button.collidepoint(pos):
                        click_sound.play()
                        in_settings = True
                    elif exit_button.collidepoint(pos):
                        click_sound.play()
                        bye_bye_sound.play()
                        pygame.time.delay(int(bye_bye_sound.get_length() * 1000))
                        pygame.quit()
                        sys.exit()
            elif event.type == MOUSEBUTTONUP:
                dragging_music_slider = False
                dragging_sound_slider = False
            elif event.type == MOUSEMOTION and in_settings:
                if dragging_music_slider:
                    new_pos = event.pos[0]
                    new_pos = max(music_slider_rect.x, min(new_pos, music_slider_rect.x + music_slider_rect.width))
                    music_slider_pos = new_pos
                    music_volume = (music_slider_pos - music_slider_rect.x) / music_slider_rect.width
                    pygame.mixer.music.set_volume(music_volume)
                elif dragging_sound_slider:
                    new_pos = event.pos[0]
                    new_pos = max(sound_slider_rect.x, min(new_pos, sound_slider_rect.x + sound_slider_rect.width))
                    sound_slider_pos = new_pos
                    sound_volume = (sound_slider_pos - sound_slider_rect.x) / sound_slider_rect.width
                    click_sound.set_volume(sound_volume)
                    bye_bye_sound.set_volume(sound_volume)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main_menu()