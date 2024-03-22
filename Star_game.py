import pygame as py
import random
import time

py.init()

WIDTH, HEIGHT = 800, 700
WIN = py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption("Space Dodge")

background = py.transform.scale(py.image.load("pictures/game.jpg"), (WIDTH, HEIGHT))
player_pic = py.transform.scale(py.image.load("pictures/player.png"), (50, 50))
star_enemy = py.transform.scale(py.image.load("pictures/enemy.png"), (50, 50))

stars = []
score = 0

player = py.Rect(WIDTH/2, HEIGHT-50, 50, 50)
player_val = 5
star_speed = 3

clock = py.time.Clock()

def draw(player, elapsed_time, stars):
    WIN.blit(background, (0,0))
    WIN.blit(player_pic, player)
    time_text = py.font.SysFont("comicsans", 30).render(f"Time: {round(elapsed_time)}s", 1, (255, 255, 255))
    WIN.blit(time_text, (10,10))
    for star in stars:
        WIN.blit(star_enemy, star)

    py.display.flip()
    py.display.update()

def spawn_star(num):
    for _ in range(num):
        x = random.randint(0, WIDTH-50)
        y = random.randint(-50, -10)
        stars.append(py.Rect(x, y, 50, 50))

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
        again_text = py.font.SysFont("comicsans", 30).render("Play again? (Y/N)", 1, (255, 255, 255))
        WIN.blit(again_text, (WIDTH//2 - again_text.get_width()//2, HEIGHT//2 + 50))
        py.display.update()

def main():
    global stars
    while True:
        stars = []
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
            if keys[py.K_RIGHT] and player.x + player_val + player.width < WIDTH:
                player.x += player_val

            for star in stars:
                star.y += star_speed
                if star.colliderect(player):
                    run = False

            draw(player, elapsed_time, stars)
            if random.randint(1, 100) <= 2:
                if elapsed_time > 30:
                    spawn_star(2)
                elif elapsed_time > 60:
                    spawn_star(3)
                elif elapsed_time > 120:
                    spawn_star(4)
                else:
                    spawn_star(1)

        play_again = game_over(elapsed_time)
        if not play_again:
            return

    py.quit()

main()