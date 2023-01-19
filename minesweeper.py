import pygame
import random
import sys
import os
import time

class Cell:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
        self.is_opened = False
        self.is_flagged = False

class Minesweeper:
    def __init__(self, rows, columns, mines):
        self.rows = rows
        self.columns = columns
        self.mines = mines
        self.mines_remaining = self.mines
        # генерация клеток поля
        self.board = [[Cell(i, j, 0) for j in range(columns)] for i in range(rows)]
        self.place_mines()
        self.calculate_neighbors()
        self.running = True
        self.game_over = False
        self.game_won = False
        self.font = pygame.font.Font(None, 36)
        self.font_gameover = pygame.font.Font(None, 72)
        self.font_gamewon = pygame.font.Font(None, 72)
        self.mixer = pygame.mixer
        self.mixer.music.load("data/explosion-sound.mp3")
        self.mixer.music.set_volume(0.03)
        # кол-во секунд для отображения партиклов от взрыва
        self.secs = 5
                    
    def place_mines(self):
        while self.mines_remaining != 0:
            x, y = random.randint(0, self.rows-1), random.randint(0, self.columns-1)
            if self.board[x][y].value != -1:
                self.board[x][y].value = -1
                self.mines_remaining -= 1

    def calculate_neighbors(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j].value == -1:
                    for x in range(i-1, i+2):
                        for y in range(j-1, j+2):
                            if x < 0 or x >= self.rows or y < 0 or y >= self.columns:
                                continue
                            if self.board[x][y].value != -1:
                                self.board[x][y].value += 1

    def open_empty_cells(self, x, y):
        if self.board[x][y].is_opened or self.board[x][y].is_flagged:
            return
        self.board[x][y].is_opened = True
        # вычисление пустого места на доске
        if self.board[x][y].value == 0:
            for i in range(x-1, x+2):
                for j in range(y-1, y+2):
                    if i < 0 or i >= self.rows or j < 0 or j >= self.columns:
                        continue
                    self.open_empty_cells(i, j)

    def draw_text(self, x, y, string, color, font):
        font = font
        text = font.render(string, 1, color)
        text_rect = text.get_rect()
        text_rect.center = (x, y)
        screen.blit(text, text_rect)

    def check_win(self):
        mines_to_win = 0
        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j].value == -1 and not self.board[i][j].is_flagged:
                    mines_to_win += 1
        if mines_to_win == 0:
            self.game_won = True
                

    def render(self):
        screen.fill((255, 255, 255))
        if not self.game_over:
            for i in range(self.rows):
                for j in range(self.columns):
                    if self.board[i][j].is_opened:
                        if self.board[i][j].value == -1:
                            pygame.draw.rect(screen, (255, 0, 0), (i*60, j*60, 60, 60), 100)
                        else:
                            pygame.draw.rect(screen, (200, 200, 200), (i*60, j*60, 60, 60), 1)
                            if self.board[i][j].value > 0:
                                text = self.font.render(str(self.board[i][j].value), 1, (0, 0, 0))
                                screen.blit(text, (i*60+20, j*60+20))
                            elif self.board[i][j].is_flagged:
                                pygame.draw.rect(screen, (0, 0, 255), (i*60, j*60, 60, 60), 100)
                    else:
                        if self.board[i][j].is_flagged:
                            pygame.draw.rect(screen, (0, 0, 255), (i*60, j*60, 60, 60), 100)
                        else:
                            pygame.draw.rect(screen, (180, 180, 180), (i*60, j*60, 60, 60), 100)
        if self.game_over:
            if self.secs != 0:
                all_sprites.update()
                all_sprites.draw(screen)
                pygame.display.flip()
                clock.tick(50)
                self.secs -= 1
            # делал много вызовов, чтобы создать сам текст и тень вокруг него
            self.draw_text((screen.get_width()/2)+1, (screen.get_height()/2)-1, "Game Over", 'black', self.font_gameover)
            self.draw_text((screen.get_width()/2)+1, (screen.get_height()/2)-1, "Game Over", 'black', self.font_gameover)
            self.draw_text((screen.get_width()/2)-1, (screen.get_height()/2)+1, "Game Over", 'black', self.font_gameover)
            self.draw_text((screen.get_width()/2)-1, (screen.get_height()/2)+1, "Game Over", 'black', self.font_gameover)
            self.draw_text((screen.get_width()/2), (screen.get_height()/2), "Game Over", 'red', self.font_gameover)
            self.draw_text((screen.get_width()/2)+1, (screen.get_height()/2)+49, "To restart press R", 'black', self.font_gameover)
            self.draw_text((screen.get_width()/2)+1, (screen.get_height()/2)+49, "To restart press R", 'black', self.font_gameover)
            self.draw_text((screen.get_width()/2)-1, (screen.get_height()/2)+51, "To restart press R", 'black', self.font_gameover)
            self.draw_text((screen.get_width()/2)-1, (screen.get_height()/2)+51, "To restart press R", 'black', self.font_gameover)
            self.draw_text((screen.get_width()/2), (screen.get_height()/2)+50, "To restart press R", 'red', self.font_gameover)
        if self.game_won:
            screen.fill((255, 255, 255))
            self.draw_text((screen.get_width()/2)+1, (screen.get_height()/2)-1, "You're won!", 'black', self.font_gameover)
            self.draw_text((screen.get_width()/2)+1, (screen.get_height()/2)-1, "You're won!", 'black', self.font_gameover)
            self.draw_text((screen.get_width()/2)-1, (screen.get_height()/2)+1, "You're won!", 'black', self.font_gameover)
            self.draw_text((screen.get_width()/2)-1, (screen.get_height()/2)+1, "You're won!", 'black', self.font_gameover)
            self.draw_text((screen.get_width()/2), (screen.get_height()/2), "You're won!", 'red', self.font_gameover)
            self.draw_text((screen.get_width()/2)+1, (screen.get_height()/2)+49, "To restart press R", 'black', self.font_gameover)
            self.draw_text((screen.get_width()/2)+1, (screen.get_height()/2)+49, "To restart press R", 'black', self.font_gameover)
            self.draw_text((screen.get_width()/2)-1, (screen.get_height()/2)+51, "To restart press R", 'black', self.font_gameover)
            self.draw_text((screen.get_width()/2)-1, (screen.get_height()/2)+51, "To restart press R", 'black', self.font_gameover)
            self.draw_text((screen.get_width()/2), (screen.get_height()/2)+50, "To restart press R", 'red', self.font_gameover)
        pygame.display.flip()

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Particle(pygame.sprite.Sprite):
    sparkle = [load_image("sparkle.png")]
    sprite = pygame.sprite.Sprite()
    sprite.image = load_image("sparkle.png")
    all_sprites = pygame.sprite.Group()
    sprite.rect = sprite.image.get_rect()
    all_sprites.add(sprite)
    for scale in (5, 10, 20):
        sparkle.append(pygame.transform.scale(sparkle[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.image = random.choice(self.sparkle)
        self.rect = self.image.get_rect()
        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
        self.gravity = 5
        
    def update(self):
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещение частицы
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(screen_rect):
            self.kill()

def create_particles(position):
    # количество создаваемых частиц
    particle_count = 25
    # скорости частиц
    numbers = range(-5, 8)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))

if __name__ == '__main__':
    pygame.init()
    all_sprites = pygame.sprite.Group()
    screen = pygame.display.set_mode((600, 600))
    screen_rect = (0, 0, 600, 600)
    screen.fill((0, 0, 0))
    pygame.display.set_caption("Сапёр")
    game = Minesweeper(10, 10, 15)
    clock = pygame.time.Clock()
    FPS = 50
    while game.running:
        game.render()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                create_particles(pygame.mouse.get_pos())
                all_sprites.update()
                all_sprites.draw(screen)    
                clock.tick(FPS)
                x, y = event.pos
                x = x // 60
                y = y // 60
                if event.button == 1 and not game.game_over and not game.game_won:
                    if game.board[x][y].value == -1 and not game.board[x][y].is_flagged:
                        game.open_empty_cells(x, y)
                        game.game_over = True
                        game.mixer.music.play()
                        create_particles(pygame.mouse.get_pos())
                    else:
                        game.open_empty_cells(x, y)
                elif event.button == 3 and not game.game_over and not game.game_won:
                    game.board[x][y].is_flagged = not game.board[x][y].is_flagged
                    game.check_win()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game.game_over = False
                    game.__init__(game.rows, game.columns, game.mines)
            game.check_win()
        game.render()
        clock.tick(FPS)
    pygame.quit()
    sys.exit()
