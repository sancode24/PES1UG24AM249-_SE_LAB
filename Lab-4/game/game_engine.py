import random
import pygame
from game.maze import generate_maze, CELL
from game.entities import Player, Enemy

COLS, ROWS = 13, 11
WIDTH = COLS * CELL
HUD_HEIGHT = 60
HEIGHT = ROWS * CELL + HUD_HEIGHT
FPS = 60

FREEZE_FRAMES = 300          # 5 seconds at 60 FPS
TIER_FRAMES = 15 * FPS       # enemies speed up every 15 seconds

# (row, col, color) for each enemy: red, orange, purple
ENEMY_STARTS = [
    (ROWS-1, COLS-1, (220, 60, 60)),
    (0, COLS-1, (240, 150, 40)),
    (ROWS-1, 0, (150, 70, 200)),
]

class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Maze Chase")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("monospace", 22)
        self.small_font = pygame.font.SysFont("monospace", 13, bold=True)
        self.big_font = pygame.font.SysFont("monospace", 38, bold=True)
        self.reset()

    def reset(self):
        self.walls = generate_maze(COLS, ROWS)
        self.player = Player(0, 0)
        self.enemies = [Enemy(r, c, color) for r, c, color in ENEMY_STARTS]
        self.exit_rect = pygame.Rect((COLS//2)*CELL+5, (ROWS//2)*CELL+5, CELL-10, CELL-10)

        # Power pellet: random cell, excluding player start, exit, and enemy corners
        excluded = {(0, 0), (ROWS//2, COLS//2)} | {(r, c) for r, c, _ in ENEMY_STARTS}
        choices = [(r, c) for r in range(ROWS) for c in range(COLS) if (r, c) not in excluded]
        pr, pc = random.choice(choices)
        self.pellet_rect = pygame.Rect(0, 0, 16, 16)
        self.pellet_rect.center = (pc*CELL + CELL//2, pr*CELL + CELL//2)
        self.pellet_active = True

        self.caught = False
        self.won = False
        self.speed_tier = 0
        self.score = 0   # frames survived

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r: self.reset()
        return True

    def update(self):
        if self.caught or self.won: return

        # Survival score: +1 per frame while the game is running
        self.score += 1

        # Difficulty ramp (frame-based, same clock as score and freeze timer)
        tier = self.score // TIER_FRAMES
        if tier != self.speed_tier:
            self.speed_tier = tier
            for enemy in self.enemies:
                enemy.set_speed_tier(tier)

        keys = pygame.key.get_pressed()
        self.player.move(keys, self.walls, ROWS, COLS)

        # Power pellet pickup (checked before enemy collisions)
        if self.pellet_active and self.player.rect.colliderect(self.pellet_rect):
            self.pellet_active = False
            for enemy in self.enemies:
                enemy.frozen = True
                enemy.freeze_timer = FREEZE_FRAMES

        for enemy in self.enemies:
            occupied = {(e.r, e.c) for e in self.enemies if e is not enemy}
            enemy.update(self.walls, self.player, ROWS, COLS, occupied)
            if not enemy.frozen and self.player.rect.colliderect(enemy.rect):
                self.caught = True

        # Being caught takes priority over reaching the exit on the same frame
        if not self.caught and self.player.rect.colliderect(self.exit_rect):
            self.won = True

    def draw(self):
        self.screen.fill((230, 220, 210))
        wc=(50,40,60)
        for r in range(ROWS):
            for c in range(COLS):
                x,y=c*CELL,r*CELL
                w=self.walls[r][c]
                if w[0]: pygame.draw.line(self.screen,wc,(x,y),(x+CELL,y),3)
                if w[1]: pygame.draw.line(self.screen,wc,(x,y+CELL),(x+CELL,y+CELL),3)
                if w[2]: pygame.draw.line(self.screen,wc,(x+CELL,y),(x+CELL,y+CELL),3)
                if w[3]: pygame.draw.line(self.screen,wc,(x,y),(x,y+CELL),3)
        pygame.draw.rect(self.screen,(80,200,80),self.exit_rect,border_radius=4)
        lbl=self.small_font.render("EXIT",True,(20,80,20))
        self.screen.blit(lbl,lbl.get_rect(center=self.exit_rect.center))
        if self.pellet_active:
            pygame.draw.circle(self.screen,(255,220,0),self.pellet_rect.center,self.pellet_rect.width//2)
        self.player.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)

        # HUD (60px, two lines)
        hud=pygame.Rect(0,ROWS*CELL,WIDTH,HUD_HEIGHT)
        pygame.draw.rect(self.screen,(30,30,50),hud)
        line1_y = ROWS*CELL + 6
        line2_y = ROWS*CELL + 32
        info=self.font.render("Reach EXIT! R=Restart",True,(200,200,200))
        self.screen.blit(info,(8,line1_y))
        tier=self.font.render(f"Speed: Tier {self.speed_tier}",True,(240,200,80))
        self.screen.blit(tier,(WIDTH-tier.get_width()-8,line1_y))
        surv=self.font.render(f"Survived: {self.score // FPS}s",True,(200,200,200))
        self.screen.blit(surv,(8,line2_y))

        if self.caught:
            self._overlay("CAUGHT!", (220,60,60))
        elif self.won:
            self._overlay("ESCAPED!", (80,220,80))
        pygame.display.flip()

    def _overlay(self, text, color):
        surf=pygame.Surface((WIDTH,ROWS*CELL),pygame.SRCALPHA)
        surf.fill((0,0,0,140))
        self.screen.blit(surf,(0,0))
        msg=self.big_font.render(text,True,color)
        sub=self.font.render("Press R to Restart",True,(200,200,200))
        final=self.font.render(f"Final score: {self.score // FPS}s",True,(200,200,200))
        self.screen.blit(msg,(WIDTH//2-msg.get_width()//2,ROWS*CELL//2-30))
        self.screen.blit(sub,(WIDTH//2-sub.get_width()//2,ROWS*CELL//2+20))
        self.screen.blit(final,(WIDTH//2-final.get_width()//2,ROWS*CELL//2+50))

    def run(self):
        running=True
        while running:
            running=self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
