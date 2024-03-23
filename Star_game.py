import pygame as py
import random
import time

py.init()

WIDTH, HEIGHT = 800, 700
WIN = py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption("Stars Game")

background = py.transform.scale(py.image.load("pictures/game.jpg"), (WIDTH, HEIGHT))
player_pic = py.transform.scale(py.image.load("pictures/player.webp"), (50, 50))
star_enemy = py.transform.scale(py.image.load("pictures/dimond.webp"), (50, 50))
dimonds_pic = py.transform.scale(py.image.load("pictures/enemy.png"), (50, 50))
start_screen_img = py.transform.scale(py.image.load("pictures/startBG.jpg"), (WIDTH, HEIGHT))


dimonds = []
skulls = []
score = 0
health = 100
health_decrement = 10
health_increment = 1

player = py.Rect(WIDTH/2, HEIGHT-50, 50, 50)
player_val = 5
star_speed = 3
dimond_speed = 2

clock = py.time.Clock()

def health_bar():
    global health
    py.draw.rect(WIN, (255, 0, 0), (10, HEIGHT-30, 200, 20))
    py.draw.rect(WIN, (0, 255, 0), (10, HEIGHT-30, int(200 * (health / 100)), 20))

def draw(player, elapsed_time, skulls, dimonds):
    WIN.blit(background, (0,0))
    WIN.blit(player_pic, player)
    health_bar()
    time_text = py.font.SysFont("comicsans", 30).render(f"Time: {round(elapsed_time)}s", 1, (255, 255, 255))
    score_text = py.font.SysFont("comicsans", 30).render(f"Score: {score}", 1, (255, 255, 255))
    WIN.blit(score_text, (WIDTH - score_text.get_width() - 10, 10))
    WIN.blit(time_text, (10,10))
    for star in skulls:
        WIN.blit(star_enemy, star)
    for dimond in dimonds:
        WIN.blit(dimonds_pic, dimond)

    py.display.flip()
    py.display.update()

def spawn_dimond(num):
    for _ in range(num):
        x = random.randint(0, WIDTH-50)
        y = random.randint(-50, -10)
        dimonds.append(py.Rect(x, y, 50, 50))

def spawn_star(num):
    for _ in range(num):
        x = random.randint(0, WIDTH-50)
        y = random.randint(-50, -10)
        skulls.append(py.Rect(x, y, 20, 20))

def game_over(elapsed_time):
    run = True
    while run:
        for event in py.event.get():
            if event.type == py.QUIT:
                return False
            elif event.type == py.KEYDOWN:
                if event.key == py.K_y:
                    return True
                elif event.key == py.K_n:
                    return False

        WIN.fill((0, 0, 0))
        end_text = py.font.SysFont("comicsans", 30).render(f"Game Over! Time Survived: {round(elapsed_time)}s", 1, (255, 0, 0))
        WIN.blit(end_text, (WIDTH//2 - end_text.get_width()//2, HEIGHT//2 - end_text.get_height()//2))
        scor_text = py.font.SysFont("comicsans", 30).render(f"Score: {score}", 1, (255, 255, 255))
        WIN.blit(scor_text, (WIDTH//2 - scor_text.get_width()//2, HEIGHT//2 - scor_text.get_height()//2 + 50))
        again_text = py.font.SysFont("comicsans", 30).render("Play again? (Y/N)", 1, (255, 255, 255))
        WIN.blit(again_text, (WIDTH//2 - again_text.get_width()//2, HEIGHT//2 + 70))
        py.display.update()

def start_screen():
    WIN.blit(start_screen_img, (0, 0))
    start_text = py.font.SysFont("comicsans", 50).render("Press S to start the Game", 1, (255, 255, 255))
    info_text = py.font.SysFont("comicsans", 20).render("Game made by Mahgoub Mohamed (pq00p)", 1, (255, 255, 255))
    WIN.blit(info_text, (WIDTH - info_text.get_width()//2-600, HEIGHT//2 - info_text.get_height()//2 + 300))
    WIN.blit(start_text, (WIDTH//2 - start_text.get_width()//2, HEIGHT//2 - start_text.get_height()//2))
    py.display.update()
    waiting = True
    while waiting:
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
            elif event.type == py.KEYDOWN:
                if event.key == py.K_s:
                    waiting = False

def main():
    start_screen()
    global score
    global skulls
    global health
    global health_increment
    global health_decrement
    while True:
        skulls = []
        spawn_star(num=1)
        start_time = time.time()
        run = True
        while run:
            clock.tick(60)
            elapsed_time = time.time() - start_time
            for event in py.event.get():
                if event.type == py.QUIT:
                    return
            keys = py.key.get_pressed()
            if keys[py.K_LEFT] and player.x - player_val > 0:
                player.x -= player_val
            elif keys[py.K_RIGHT] and player.x + player_val + player.width < WIDTH:
                player.x += player_val
            elif keys[py.K_UP] and player.y - player_val > 0:
                player.y -= player_val
            elif keys[py.K_DOWN] and player.y + player_val + player.height < HEIGHT:
                player.y += player_val
            
            health_bar()

            for enemy in skulls[:]:
                enemy.y += star_speed
                if enemy.colliderect(player):
                    health -= health_decrement
                    skulls.remove(enemy)
                if health <= 0:
                    run = False
                    break
            for dim in dimonds[:]:
                dim.y += dimond_speed
                if dim.colliderect(player):
                    health += health_increment
                    score += 1
                    dimonds.remove(dim)

            draw(player, elapsed_time, skulls, dimonds)
            if random.randint(1, 100) <= 2:
                if elapsed_time > 30:
                    health_decrement = 15
                    spawn_star(2)
                    spawn_dimond(1)
                elif elapsed_time > 60:
                    health_decrement = 20
                    spawn_star(3)
                    spawn_dimond(2)
                elif elapsed_time > 120:
                    health_decrement = 25
                    spawn_dimond(3)
                    spawn_star(4)
                else:
                    spawn_dimond(1)
                    spawn_star(1)

        play_again = game_over(elapsed_time)
        if not play_again:
            return

    py.quit()

main()