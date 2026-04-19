from pygame import *

class GameSprite(sprite.Sprite):
    def __init__(self, color, width, height, player_x, player_y, player_speed):
        super().__init__()
        self.image = Surface((width, height))
        self.image.fill(color)
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update_l(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < 400:
            self.rect.y += self.speed
    
    def update_r(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < 400:
            self.rect.y += self.speed

class Ball(GameSprite):
    def __init__(self, color, width, height, player_x, player_y, player_speed):
        super().__init__(color, width, height, player_x, player_y, player_speed)
        self.direction_x = 1
        self.direction_y = 1
    
    def update(self):
        self.rect.x += self.speed * self.direction_x
        self.rect.y += self.speed * self.direction_y
        
        if self.rect.y <= 0 or self.rect.y >= 450:
            self.direction_y *= -1
        
        if self.rect.colliderect(rocket_left.rect) and self.direction_x < 0:
            self.direction_x *= -1
        
        if self.rect.colliderect(rocket_right.rect) and self.direction_x > 0:
            self.direction_x *= -1
        
        if self.rect.x <= 0:
            return "right_score"
        
        if self.rect.x >= 750:
            return "left_score"
        
        return None

window = display.set_mode((800, 500))
display.set_caption("Ping-Pong")
background = Surface((800, 500))
background.fill((0, 0, 0))

rocket_left = Player((255, 255, 255), 20, 100, 30, 200, 5)
rocket_right = Player((255, 255, 255), 20, 100, 750, 200, 5)
ball = Ball((255, 255, 255), 20, 20, 400, 250, 4)

score_left = 0
score_right = 0
font.init()
font_score = font.Font(None, 50)
font_win = font.Font(None, 70)

game = True
pause = False
winner = None
FPS = 60
clock = time.Clock()

while game:
    clock.tick(FPS)
    
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                pause = not pause
            if e.key == K_r and winner:
                winner = None
                score_left = 0
                score_right = 0
                ball.rect.x = 400
                ball.rect.y = 250
                ball.direction_x = 1
                ball.direction_y = 1
    
    if not pause and not winner:
        rocket_left.update_l()
        rocket_right.update_r()
        result = ball.update()
        
        if result == "left_score":
            score_left += 1
            ball.rect.x = 400
            ball.rect.y = 250
            ball.direction_x = 1
            time.wait(500)
        elif result == "right_score":
            score_right += 1
            ball.rect.x = 400
            ball.rect.y = 250
            ball.direction_x = -1
            time.wait(500)
        
        if score_left >= 1:
            winner = "Левый игрок победил!"
        elif score_right >= 1:
            winner = "Правый игрок победил!"
    
    window.blit(background, (0, 0))
    draw.line(window, (255, 255, 255), (400, 0), (400, 500), 2)
    
    rocket_left.reset()
    rocket_right.reset()
    ball.reset()
    
    score_text = font_score.render(f"{score_left} : {score_right}", True, (255, 255, 255))
    window.blit(score_text, (366, 20))
    
    if pause and not winner:
        pause_text = font_win.render("PAUSE", True, (255, 255, 0))
        window.blit(pause_text, (330, 200))
    
    if winner:
        win_text = font_win.render(winner, True, (255, 215, 0))
        window.blit(win_text, (150, 200))
        restart_text = font_score.render("Press R to restart", True, (255, 255, 255))
        window.blit(restart_text, (260, 280))
    
    display.update()

quit()