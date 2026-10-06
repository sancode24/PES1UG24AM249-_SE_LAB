import pygame
from game.maze import CELL

SPEED = 2

class Player:
    def __init__(self, r, c):
        self.r, self.c = r, c
        cx, cy = c*CELL+CELL//2, r*CELL+CELL//2
        self.rect = pygame.Rect(cx-10, cy-10, 20, 20)
        self.color = (60, 120, 220)

    def move(self, keys, walls, rows, cols):
        dx=dy=0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: dx=-SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx=SPEED
        if keys[pygame.K_UP] or keys[pygame.K_w]: dy=-SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]: dy=SPEED
        nr = self.rect.move(dx,0)
        if self._valid(nr, walls, rows, cols): self.rect=nr
        nr = self.rect.move(0,dy)
        if self._valid(nr, walls, rows, cols): self.rect=nr

    def _valid(self, rect, walls, rows, cols):
        # Bounds check (unchanged)
        for px,py in [(rect.left,rect.top),(rect.right-1,rect.top),(rect.left,rect.bottom-1),(rect.right-1,rect.bottom-1)]:
            cr,cc=py//CELL,px//CELL
            if not(0<=cr<rows and 0<=cc<cols): return False

        # Wall collision: check every cell the rect overlaps, plus 1 cell around it
        T = 3  # wall thickness in px
        half = T // 2
        r_min = max(0, rect.top // CELL - 1)
        r_max = min(rows - 1, (rect.bottom - 1) // CELL + 1)
        c_min = max(0, rect.left // CELL - 1)
        c_max = min(cols - 1, (rect.right - 1) // CELL + 1)
        for r in range(r_min, r_max + 1):
            for c in range(c_min, c_max + 1):
                x, y = c * CELL, r * CELL
                top, bottom, right, left = walls[r][c]
                if top and rect.colliderect(pygame.Rect(x - half, y - half, CELL + 2*half, T)):
                    return False
                if bottom and rect.colliderect(pygame.Rect(x - half, y + CELL - half, CELL + 2*half, T)):
                    return False
                if right and rect.colliderect(pygame.Rect(x + CELL - half, y - half, T, CELL + 2*half)):
                    return False
                if left and rect.colliderect(pygame.Rect(x - half, y - half, T, CELL + 2*half)):
                    return False
        return True

    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, self.rect)

class Enemy:
    def __init__(self, r, c, color=(220, 60, 60)):
        self.r, self.c = r, c
        cx, cy = c*CELL+CELL//2, r*CELL+CELL//2
        self.rect = pygame.Rect(cx-12, cy-12, 24, 24)
        self.color = color
        self.timer = 0
        self.move_interval = 20  # frames between cell moves

    def update(self, walls, player, rows, cols):
        from game.maze import bfs
        self.timer += 1
        if self.timer >= self.move_interval:
            self.timer = 0
            pr, pc = player.rect.centery//CELL, player.rect.centerx//CELL
            step = bfs(walls, (self.r, self.c), (pr, pc), rows, cols)
            if step:
                dr, dc = step
                self.r
