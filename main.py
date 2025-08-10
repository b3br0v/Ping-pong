import pygame
import sys

pygame.init()


font20 = pygame.font.Font('freesansbold.ttf', 20)
font40 = pygame.font.Font('freesansbold.ttf', 40)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GRAY = (180, 180, 180)

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

clock = pygame.time.Clock()
FPS = 60

class Striker:
    def __init__(self, posx, posy, width, height, speed, color):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color
        self.geekRect = pygame.Rect(posx, posy, width, height)

    def display(self):
        pygame.draw.rect(screen, self.color, self.geekRect)

    def update(self, yFac):
        self.posy += self.speed * yFac
        self.posy = max(0, min(self.posy, HEIGHT - self.height))
        self.geekRect = pygame.Rect(self.posx, self.posy, self.width, self.height)

    def displayScore(self, text, score, x, y, color):
        text = font20.render(text + str(score), True, color)
        screen.blit(text, text.get_rect(center=(x, y)))

    def getRect(self):
        return self.geekRect

class Ball:
    def __init__(self, posx, posy, radius, speed, color):
        self.posx = posx
        self.posy = posy
        self.radius = radius
        self.speed = speed
        self.original_speed = speed
        self.color = color
        self.xFac = 1
        self.yFac = -1
        self.ball = pygame.draw.circle(screen, self.color, (self.posx, self.posy), self.radius)
        self.firstTime = 1

    def display(self):
        self.ball = pygame.draw.circle(screen, self.color, (self.posx, self.posy), self.radius)

    def update(self):
        self.posx += self.speed * self.xFac
        self.posy += self.speed * self.yFac

        if self.posy <= 0 or self.posy >= HEIGHT:
            self.yFac *= -1

        if self.posx <= 0 and self.firstTime:
            self.firstTime = 0
            return 1
        elif self.posx >= WIDTH and self.firstTime:
            self.firstTime = 0
            return -1
        else:
            return 0

    def reset(self):
        self.posx = WIDTH // 2
        self.posy = HEIGHT // 2
        self.speed = self.original_speed
        self.xFac *= -1
        self.firstTime = 1

    def hit(self):
        self.xFac *= -1
        self.speed += 0.5 

    def getRect(self):
        return self.ball

def show_start_menu():
    while True:
        screen.fill(BLACK)
        title = font40.render("PING-PONG", True, WHITE)
        play = font20.render("Грати", True, BLACK)
        quit_game = font20.render("Вийти", True, BLACK)

        pygame.draw.rect(screen, GRAY, [WIDTH // 2 - 100, HEIGHT // 2 - 40, 200, 40])
        pygame.draw.rect(screen, GRAY, [WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 40])

        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 100))
        screen.blit(play, (WIDTH // 2 - play.get_width() // 2, HEIGHT // 2 - 35))
        screen.blit(quit_game, (WIDTH // 2 - quit_game.get_width() // 2, HEIGHT // 2 + 25))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if WIDTH // 2 - 100 < x < WIDTH // 2 + 100:
                    if HEIGHT // 2 - 40 < y < HEIGHT // 2:
                        return  
                    elif HEIGHT // 2 + 20 < y < HEIGHT // 2 + 60:
                        pygame.quit(); sys.exit()

def show_game_over_menu(winner):
    while True:
        screen.fill(BLACK)
        title = font40.render(f"{winner} переміг!", True, WHITE)
        again = font20.render("Грати ще раз", True, BLACK)
        quit_game = font20.render("Вийти", True, BLACK)

        pygame.draw.rect(screen, GRAY, [WIDTH // 2 - 100, HEIGHT // 2 - 40, 200, 40])
        pygame.draw.rect(screen, GRAY, [WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 40])

        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 100))
        screen.blit(again, (WIDTH // 2 - again.get_width() // 2, HEIGHT // 2 - 35))
        screen.blit(quit_game, (WIDTH // 2 - quit_game.get_width() // 2, HEIGHT // 2 + 25))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if WIDTH // 2 - 100 < x < WIDTH // 2 + 100:
                    if HEIGHT // 2 - 40 < y < HEIGHT // 2:
                        main()  
                        return
                    elif HEIGHT // 2 + 20 < y < HEIGHT // 2 + 60:
                        pygame.quit(); sys.exit()

def main():
    geek1 = Striker(20, 0, 10, 100, 10, GREEN)
    geek2 = Striker(WIDTH - 30, 0, 10, 100, 10, GREEN)
    ball = Ball(WIDTH // 2, HEIGHT // 2, 7, 5, WHITE)

    geek1Score, geek2Score = 0, 0
    geek1YFac, geek2YFac = 0, 0
    listOfGeeks = [geek1, geek2]

    running = True

    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP: geek2YFac = -1
                if event.key == pygame.K_DOWN: geek2YFac = 1
                if event.key == pygame.K_w: geek1YFac = -1
                if event.key == pygame.K_s: geek1YFac = 1
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_UP, pygame.K_DOWN]: geek2YFac = 0
                if event.key in [pygame.K_w, pygame.K_s]: geek1YFac = 0

        for geek in listOfGeeks:
            if pygame.Rect.colliderect(ball.getRect(), geek.getRect()):
                ball.hit()

        geek1.update(geek1YFac)
        geek2.update(geek2YFac)
        point = ball.update()

        if point == -1:
            geek1Score += 1
        elif point == 1:
            geek2Score += 1

        if point:
            ball.reset()

        if geek1Score >= 15:
            show_game_over_menu("Гравець 1")
            return
        elif geek2Score >= 15:
            show_game_over_menu("Гравець 2")
            return

        geek1.display()
        geek2.display()
        ball.display()

        geek1.displayScore("Гравець 1: ", geek1Score, 100, 20, WHITE)
        geek2.displayScore("Гравець 2: ", geek2Score, WIDTH - 100, 20, WHITE)

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    show_start_menu()
    main()
    
    pygame.display.flip()