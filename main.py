import pygame
import random

# Инициализация Pygame
pygame.init()

# Настройки окна
screen_width = 600
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Параметры игрового поля
paddle_width = 100
paddle_height = 15
ball_radius = 10

# Скорость мяча (уменьшена на 10%)
ball_speed_x = 4 * random.choice((1, -1)) * 0.9  # Уменьшаем на 10%
ball_speed_y = -4 * 0.9  # Уменьшаем на 10%

# Скорость ракетки
paddle_speed = 6

# Параметры блока
block_width = 60
block_height = 20
blocks = []

# Функция для создания блоков
def create_blocks():
    blocks.clear()
    for row in range(5):
        for col in range(10):
            block = pygame.Rect(col * (block_width + 10) + 20, row * (block_height + 5) + 40, block_width, block_height)
            blocks.append(block)

# Создание объектов
def reset_game():
    global paddle, ball, ball_speed_x, ball_speed_y
    paddle = pygame.Rect(screen_width // 2 - paddle_width // 2, screen_height - 30, paddle_width, paddle_height)
    ball = pygame.Rect(screen_width // 2 - ball_radius, screen_height // 2 - ball_radius, ball_radius * 2, ball_radius * 2)
    ball_speed_x = 4 * random.choice((1, -1)) * 0.9
    ball_speed_y = -4 * 0.9
    create_blocks()

# Функция для отображения экрана завершения игры
def game_over():
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over!", True, WHITE)
    restart_text = pygame.font.Font(None, 36).render("Press R to Restart or Q to Quit", True, WHITE)
    
    screen.fill(BLACK)
    screen.blit(text, (screen_width // 3, screen_height // 3))
    screen.blit(restart_text, (screen_width // 4, screen_height // 2))
    pygame.display.flip()

# Функция для экрана начала игры
def game_start():
    font = pygame.font.Font(None, 36)
    instructions = font.render("Press Enter to Start", True, WHITE)
    controls = font.render("Use Left and Right arrows to move", True, WHITE)
    
    screen.fill(BLACK)
    screen.blit(instructions, (screen_width // 3, screen_height // 3))
    screen.blit(controls, (screen_width // 3 - 10, screen_height // 3 + 50))
    
    pygame.display.flip()

# Главный игровой цикл
running = True
game_started = False
restart = False

# Инициализация игры
reset_game()

while running:
    if not game_started:
        game_start()

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_started = True  # Начинаем игру при нажатии Enter

    else:
        # Обработка событий во время игры
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Управление ракеткой
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle.left > 0:
            paddle.x -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle.right < screen_width:
            paddle.x += paddle_speed

        # Двигаем мяч
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        # Столкновение с границами экрана
        if ball.left <= 0 or ball.right >= screen_width:
            ball_speed_x = -ball_speed_x
        if ball.top <= 0:
            ball_speed_y = -ball_speed_y
        if ball.bottom >= screen_height:
            game_over()  # Показываем экран завершения игры

            # Ожидаем действий пользователя для рестарта или выхода
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        # Перезапуск игры
                        reset_game()
                        game_started = True
                    elif event.key == pygame.K_q:
                        running = False  # Выход из игры

        # Столкновение с ракеткой
        if ball.colliderect(paddle):
            ball_speed_y = -ball_speed_y

        # Столкновение с блоками
        for block in blocks[:]:
            if ball.colliderect(block):
                ball_speed_y = -ball_speed_y
                blocks.remove(block)

        # Отображение на экране
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, paddle)
        pygame.draw.ellipse(screen, RED, ball)
        
        for block in blocks:
            pygame.draw.rect(screen, WHITE, block)

        pygame.display.flip()

        # Частота обновления экрана
        pygame.time.Clock().tick(60)

# Закрытие Pygame
pygame.quit()
