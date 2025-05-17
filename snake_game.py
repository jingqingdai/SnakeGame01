import pygame
import random

# 初始化pygame
pygame.init()

# 游戏窗口大小
WIDTH, HEIGHT = 600, 400
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("贪吃蛇游戏")

# 颜色定义
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
LIGHT_GREEN = (144, 238, 144)
RED = (255, 0, 0)
LIGHT_RED = (255, 99, 71)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)
BLUE = (0, 120, 255)
LIGHT_BLUE = (135, 206, 250)
YELLOW = (255, 255, 0)
LIGHT_YELLOW = (255, 255, 224)

# 难度设置
DIFFICULTY_EASY = 0
DIFFICULTY_MEDIUM = 1
DIFFICULTY_HARD = 2

# 各难度对应的速度
SPEED_EASY = 3
SPEED_MEDIUM = 5
SPEED_HARD = 10

# 当前难度
current_difficulty = DIFFICULTY_MEDIUM

# 按钮类
class Button:
    """
    按钮类，用于创建可点击的按钮
    """
    def __init__(self, text, x, y, width, height, color, hover_color, text_color=BLACK, font_size=20):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = pygame.font.SysFont('SimHei', font_size)
        self.rect = pygame.Rect(x, y, width, height)
        
    def draw(self, surface):
        # 检查鼠标是否悬停在按钮上
        mouse_pos = pygame.mouse.get_pos()
        current_color = self.hover_color if self.is_hover(mouse_pos) else self.color
        
        # 绘制按钮（带透明度的磨砂效果）
        button_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(button_surface, (*current_color, 200), (0, 0, self.width, self.height), border_radius=10)
        
        # 绘制文本
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=(self.width/2, self.height/2))
        button_surface.blit(text_surface, text_rect)
        
        # 添加按钮边框
        pygame.draw.rect(button_surface, (*self.text_color, 150), (0, 0, self.width, self.height), 2, border_radius=10)
        
        surface.blit(button_surface, (self.x, self.y))
        
    def is_hover(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
        
    def is_clicked(self, mouse_pos, mouse_click):
        return self.rect.collidepoint(mouse_pos) and mouse_click

# 贪吃蛇初始参数
def reset_game():
    global snake_pos, snake_dir, change_to, speed, food_pos, food_spawn, score
    # 让蛇在屏幕中央，且向右移动
    snake_pos = [
        [WIDTH // 2, HEIGHT // 2],
        [WIDTH // 2 - 10, HEIGHT // 2],
        [WIDTH // 2 - 20, HEIGHT // 2]
    ]
    snake_dir = 'RIGHT'
    change_to = snake_dir
    
    # 根据难度设置速度
    if current_difficulty == DIFFICULTY_EASY:
        speed = SPEED_EASY
    elif current_difficulty == DIFFICULTY_MEDIUM:
        speed = SPEED_MEDIUM
    else:
        speed = SPEED_HARD
        
    food_pos = [random.randrange(1, (WIDTH // 10)) * 10,
                random.randrange(1, (HEIGHT // 10)) * 10]
    food_spawn = True
    score = 0

reset_game()

# 字体
font = pygame.font.SysFont('SimHei', 25)

# 游戏状态
STATE_INIT = 0  # 等待开始
STATE_RUNNING = 1  # 运行中
STATE_PAUSED = 2  # 暂停
STATE_OVER = 3  # 结束

game_state = STATE_INIT

# 创建按钮
start_button = Button('开始游戏', WIDTH//2 - 75, HEIGHT//2 - 20, 150, 50, LIGHT_GREEN, GREEN, BLACK)
end_button = Button('结束游戏', WIDTH - 120, 10, 100, 40, LIGHT_RED, RED, BLACK)

# 创建难度选择按钮（减小按钮大小并向下移动）
easy_button = Button('简单', WIDTH//2 - 150, HEIGHT//2 + 70, 90, 35, LIGHT_BLUE, BLUE, BLACK)
medium_button = Button('中等', WIDTH//2 - 45, HEIGHT//2 + 70, 90, 35, LIGHT_GREEN, GREEN, BLACK)
hard_button = Button('困难', WIDTH//2 + 60, HEIGHT//2 + 70, 90, 35, LIGHT_RED, RED, BLACK)

# 磨砂背景效果
def draw_frosted_background():
    """
    绘制磨砂风格的背景
    """
    background = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    background.fill((240, 240, 240, 200))
    
    # 添加一些随机的半透明小圆点，增加磨砂质感
    for _ in range(100):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        radius = random.randint(1, 3)
        alpha = random.randint(30, 100)
        pygame.draw.circle(background, (255, 255, 255, alpha), (x, y), radius)
    
    return background

def show_score():
    """
    显示当前分数
    """
    # 创建一个半透明的磨砂背景
    score_bg = pygame.Surface((120, 40), pygame.SRCALPHA)
    score_bg.fill((255, 255, 255, 150))  # 白色半透明
    win.blit(score_bg, (5, 5))
    
    score_surface = font.render(f'分数: {score}', True, BLACK)
    win.blit(score_surface, (10, 10))

def show_difficulty():
    """
    显示当前难度
    """
    difficulty_text = ""
    if current_difficulty == DIFFICULTY_EASY:
        difficulty_text = "难度: 简单"
    elif current_difficulty == DIFFICULTY_MEDIUM:
        difficulty_text = "难度: 中等"
    else:
        difficulty_text = "难度: 困难"
    
    # 创建一个半透明的磨砂背景
    diff_bg = pygame.Surface((100, 30), pygame.SRCALPHA)
    diff_bg.fill((255, 255, 255, 150))  # 白色半透明
    win.blit(diff_bg, (5, 50))  # 将难度显示放在分数下方
    
    # 使用比分数小一号的字体
    small_font = pygame.font.SysFont('SimHei', 18)
    diff_surface = small_font.render(difficulty_text, True, BLACK)
    win.blit(diff_surface, (10, 55))  # 调整纵向位置

def show_message(message, color=BLACK, y_offset=0, font_size=25):
    """
    在屏幕中央显示一条消息，带磨砂背景
    """
    custom_font = pygame.font.SysFont('SimHei', font_size)
    msg_surface = custom_font.render(message, True, color)
    
    # 创建一个比文本略大的半透明背景
    text_width, text_height = msg_surface.get_size()
    padding = 20
    text_bg = pygame.Surface((text_width + padding*2, text_height + padding), pygame.SRCALPHA)
    text_bg.fill((255, 255, 255, 180))  # 白色半透明
    
    # 计算位置并绘制
    bg_rect = text_bg.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    rect = msg_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    
    win.blit(text_bg, bg_rect)
    win.blit(msg_surface, rect)

def game_over():
    """
    游戏结束时显示提示（不再阻塞等待input）
    """
    global game_state
    win.fill(WHITE)
    show_message('游戏结束', RED)
    show_score()
    pygame.display.flip()
    game_state = STATE_OVER

# 游戏主循环
clock = pygame.time.Clock()
running = True
background = draw_frosted_background()  # 预先生成磨砂背景

while running:
    # 鼠标点击检测
    mouse_click = False
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_state == STATE_INIT:
                if event.key == pygame.K_RETURN:
                    reset_game()
                    game_state = STATE_RUNNING
            elif game_state == STATE_RUNNING:
                if event.key == pygame.K_UP and snake_dir != 'DOWN':
                    change_to = 'UP'
                elif event.key == pygame.K_DOWN and snake_dir != 'UP':
                    change_to = 'DOWN'
                elif event.key == pygame.K_LEFT and snake_dir != 'RIGHT':
                    change_to = 'LEFT'
                elif event.key == pygame.K_RIGHT and snake_dir != 'LEFT':
                    change_to = 'RIGHT'
                elif event.key == pygame.K_SPACE:
                    game_state = STATE_PAUSED
                elif event.key == pygame.K_ESCAPE:
                    running = False
            elif game_state == STATE_PAUSED:
                if event.key == pygame.K_SPACE:
                    game_state = STATE_RUNNING
                elif event.key == pygame.K_ESCAPE:
                    running = False
            elif game_state == STATE_OVER:
                if event.key == pygame.K_RETURN:
                    reset_game()
                    game_state = STATE_INIT
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 左键点击
                mouse_click = True

    # 背景
    win.blit(background, (0, 0))
    
    if game_state == STATE_INIT:
        # 游戏标题使用大字体
        title_font = pygame.font.SysFont('SimHei', 40)
        title_surface = title_font.render('贪吃蛇游戏', True, DARK_GRAY)
        title_rect = title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        
        # 创建一个比文本略大的半透明背景
        title_width, title_height = title_surface.get_size()
        title_padding = 25
        title_bg = pygame.Surface((title_width + title_padding*2, title_height + title_padding), pygame.SRCALPHA)
        title_bg.fill((255, 255, 255, 180))
        title_bg_rect = title_bg.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        
        win.blit(title_bg, title_bg_rect)
        win.blit(title_surface, title_rect)
        
        # 将 "请选择难度" 的提示向下移动，并缩小字体
        prompt_font = pygame.font.SysFont('SimHei', 20)
        prompt_surface = prompt_font.render('请选择难度', True, BLACK)
        prompt_rect = prompt_surface.get_rect(center=(WIDTH // 2, HEIGHT//2 + 45))
        win.blit(prompt_surface, prompt_rect)
        
        # 绘制难度选择按钮
        easy_button.draw(win)
        medium_button.draw(win)
        hard_button.draw(win)
        
        start_button.draw(win)
        
        # 显示当前选择的难度，优化显示位置
        difficulty_text = ""
        if current_difficulty == DIFFICULTY_EASY:
            difficulty_text = "难度: 简单"
        elif current_difficulty == DIFFICULTY_MEDIUM:
            difficulty_text = "难度: 中等"
        else:
            difficulty_text = "难度: 困难"
        
        # 创建磨砂背景，放在左上角更整洁的位置
        diff_bg = pygame.Surface((120, 40), pygame.SRCALPHA)
        diff_bg.fill((255, 255, 255, 150))
        win.blit(diff_bg, (10, 10))
        
        # 使用与主界面匹配的字体
        diff_surface = pygame.font.SysFont('SimHei', 22).render(difficulty_text, True, BLACK)
        win.blit(diff_surface, (20, 18))
        
        # 检测难度按钮点击
        if easy_button.is_clicked(mouse_pos, mouse_click):
            current_difficulty = DIFFICULTY_EASY
        elif medium_button.is_clicked(mouse_pos, mouse_click):
            current_difficulty = DIFFICULTY_MEDIUM
        elif hard_button.is_clicked(mouse_pos, mouse_click):
            current_difficulty = DIFFICULTY_HARD
        
        # 检测开始按钮点击
        if start_button.is_clicked(mouse_pos, mouse_click):
            reset_game()
            game_state = STATE_RUNNING
            
        pygame.display.update()
        clock.tick(10)
        continue
    elif game_state == STATE_PAUSED:
        show_message('游戏已暂停', RED)
        show_score()
        show_difficulty()
        pygame.display.update()
        clock.tick(10)
        continue
    elif game_state == STATE_OVER:
        show_message('游戏结束，按回车重新开始', RED)
        show_score()
        show_difficulty()
        start_button.draw(win)
        
        # 检测开始按钮点击（在游戏结束界面也可以点击开始）
        if start_button.is_clicked(mouse_pos, mouse_click):
            reset_game()
            game_state = STATE_RUNNING
            
        pygame.display.update()
        clock.tick(10)
        continue

    # 只有在STATE_RUNNING时才执行游戏逻辑
    if game_state == STATE_RUNNING:
        snake_dir = change_to

        # 移动蛇头 - 重要修复：要先创建新头部位置，然后将其添加到snake_pos[0]位置
        new_head = list(snake_pos[0])  # 获取当前蛇头位置的副本
        
        # 根据方向更新新头部的位置
        if snake_dir == 'UP':
            new_head[1] -= 10
        elif snake_dir == 'DOWN':
            new_head[1] += 10
        elif snake_dir == 'LEFT':
            new_head[0] -= 10
        elif snake_dir == 'RIGHT':
            new_head[0] += 10
            
        # 在蛇身体的前端添加新头部
        snake_pos.insert(0, new_head)

        # 判断是否吃到食物
        if snake_pos[0][0] == food_pos[0] and snake_pos[0][1] == food_pos[1]:
            score += 1
            food_spawn = False
        else:
            snake_pos.pop()  # 只有没吃到食物时才移除尾部

        # 重新生成食物
        if not food_spawn:
            food_pos = [random.randrange(1, (WIDTH // 10)) * 10,
                        random.randrange(1, (HEIGHT // 10)) * 10]
        food_spawn = True

        # 判断游戏结束
        if (snake_pos[0][0] < 0 or snake_pos[0][0] >= WIDTH or
            snake_pos[0][1] < 0 or snake_pos[0][1] >= HEIGHT):
            game_state = STATE_OVER
        for block in snake_pos[1:]:
            if snake_pos[0] == block:
                game_state = STATE_OVER
                
        # 游戏中绘制结束按钮
        end_button.draw(win)
        
        # 检测结束按钮点击
        if end_button.is_clicked(mouse_pos, mouse_click):
            game_state = STATE_INIT

    # 画蛇（磨砂风格）
    for i, pos in enumerate(snake_pos):
        if i == 0:  # 蛇头
            # 蛇头用略深的颜色
            snake_part = pygame.Surface((10, 10), pygame.SRCALPHA)
            pygame.draw.rect(snake_part, (0, 180, 0, 220), (0, 0, 10, 10), border_radius=3)
            win.blit(snake_part, (pos[0], pos[1]))
        else:  # 蛇身
            # 蛇身透明度随着身体位置变化，创造渐变效果
            alpha = max(100, 220 - i * 5)
            snake_part = pygame.Surface((10, 10), pygame.SRCALPHA)
            pygame.draw.rect(snake_part, (0, 150, 0, alpha), (0, 0, 10, 10), border_radius=2)
            win.blit(snake_part, (pos[0], pos[1]))

    # 画食物（磨砂风格）
    food_surface = pygame.Surface((10, 10), pygame.SRCALPHA)
    pygame.draw.circle(food_surface, (220, 0, 0, 200), (5, 5), 5)
    # 添加一个小高光效果
    pygame.draw.circle(food_surface, (255, 255, 255, 150), (3, 3), 1)
    win.blit(food_surface, (food_pos[0], food_pos[1]))

    # 显示分数和难度 - 在主循环最后部分
    show_score()
    show_difficulty()
    
    pygame.display.update()
    clock.tick(speed)

if not running:
    pygame.quit()
    quit() 