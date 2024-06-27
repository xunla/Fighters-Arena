import pygame
import sys
from fighter import HumanFighter, ComputerFighter

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1000, 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Warrior's Arena")
clock = pygame.time.Clock()

RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BRIGHT_RED = (238, 75, 43)
GREEN = (0, 255, 0)


#define player stats
P1_SIZE = [160, 111]
P1_SCALE = 4
P1_OFFSET = [73, 60]
P1_DATA = [P1_SIZE, P1_SCALE, P1_OFFSET]
P2_SIZE = [231, 190]
P2_SCALE = 2.4
P2_OFFSET = [105, 65]
P2_DATA = [P2_SIZE, P2_SCALE, P2_OFFSET]

#music
pygame.mixer.music.load("assets/audio/music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)
sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
sword_fx.set_volume(0.5)
magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
magic_fx.set_volume(0.75)
player_die = pygame.mixer.Sound("assets/audio/die.mp3")
player_die.set_volume(1)

#load background image
backgroundImage = pygame.image.load("assets/images/background/background.webp").convert_alpha()


#victory image
victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()
defeat_img = pygame.image.load("assets/images/icons/defeat.png").convert_alpha()

#define font
count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)


p1_animation_paths = {
    0: "assets/images/linn/Sprites/Idle.png",
    1: "assets/images/linn/Sprites/Run.png",
    2: "assets/images/linn/Sprites/Jump.png",
    3: "assets/images/linn/Sprites/Fall.png",
    4: "assets/images/linn/Sprites/Attack1.png",
    5: "assets/images/linn/Sprites/Attack2.png",
    6: "assets/images/linn/Sprites/Take Hit.png",
    7: "assets/images/linn/Sprites/Death.png"
}

p2_animation_paths = {
   0: "assets/images/wizard/Sprites/Idle.png",
    1: "assets/images/wizard/Sprites/Run.png",
    2: "assets/images/wizard/Sprites/Jump.png",
    3: "assets/images/wizard/Sprites/Fall.png",
    4: "assets/images/wizard/Sprites/Attack1.png",
    5: "assets/images/wizard/Sprites/Attack2.png",
    6: "assets/images/wizard/Sprites/Hit.png",
    7: "assets/images/wizard/Sprites/Death.png"
}

p1_frames = [8, 8, 2, 2, 4, 4, 4, 6]
p2_frames = [6, 8, 2, 2, 8, 8, 4, 7]




class Game():
  def __init__(self):
    self.state = ''
    self.introCount = 3
    self.last_count_update = pygame.time.get_ticks()
    self.countdown_active = True
      

  def dtext(self, text, font, colour, x, y):
    img = font.render(text, True, colour)
    screen.blit(img, (x, y))

  def bg(self):
    scaled_bg = pygame.transform.scale(backgroundImage, (WIDTH, HEIGHT))
    screen.blit(scaled_bg, (0, 0))

  def health(self, health, x, y):
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, GREEN, (x, y, 4 * health, 30))

  def handle_countdown(self):
        if self.countdown_active:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_count_update >= 1000:
                self.introCount -= 1
                self.last_count_update = current_time
                if self.introCount <= 0:
                    self.countdown_active = False

  def start_game(self, state):
    self.state = state
    if self.state == 'intro':
        self.start_menu()
    elif self.state == 'human' or self.state == 'computer':
      self.main_game()
  
  def start_menu(self):
    title_font = pygame.font.Font("assets/fonts/turok.ttf", 100)
    button_font = pygame.font.Font("assets/fonts/turok.ttf", 40)
    while self.state == 'intro':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.bg()
        # Title
        self.dtext("Warrior's Arena", title_font, RED, WIDTH // 2 - 340, HEIGHT // 6)

        # VS Human Button
        button_human = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)
        self.button_interaction(button_human, "VS Human", lambda: self.start_game("human"))

        # VS Computer Button
        button_computer = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
        self.button_interaction(button_computer, "VS AI", lambda: self.start_game("computer"))

        # Quit Game Button
        button_quit = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 150, 200, 50)
        self.button_interaction(button_quit, "Quit", sys.exit)

        pygame.display.update()
        clock.tick(60)
  
  def button_interaction(self, button, text, action):
    mx, my = pygame.mouse.get_pos()
    if button.collidepoint((mx, my)):
        pygame.draw.rect(screen, BRIGHT_RED, button)  # Brighter color on hover
        if pygame.mouse.get_pressed()[0]:
            action()
    else:
        pygame.draw.rect(screen, RED, button)
    self.dtext(text, pygame.font.Font("assets/fonts/turok.ttf", 40), WHITE, button.x + 10, button.y + 3)

  def pause_menu(self):
    self.prestate = self.state
    self.state = 'paused'
    while self.state == 'paused':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.state = self.prestate
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        self.bg()  # Draw background
        self.dtext("PAUSED", count_font, RED, WIDTH // 2 - 100, HEIGHT // 2 - 120)
        self.dtext("Press 'P' to Resume or 'Q' to Quit", score_font, WHITE, WIDTH // 2 - 210, HEIGHT // 2 + 20)
        pygame.display.update()
        clock.tick(30)

  def main_game(self):
      fighter1 = HumanFighter(1, 120, 400, False, P1_DATA, p1_animation_paths, p1_frames, sword_fx)
      if self.state == 'human':
        fighter2 = HumanFighter(2, 800, 400, True, P2_DATA, p2_animation_paths, p2_frames, magic_fx)
      elif self.state == 'computer':
         fighter2 = ComputerFighter(2, 800, 400, True, P2_DATA, p2_animation_paths, p2_frames, magic_fx)
      round_over = False
      score = [0, 0]
      while self.state == 'human' or self.state == 'computer':
        clock.tick(60)
        #show player stats
        self.bg()
        self.health(fighter1.health, 20, 20)
        self.health(fighter2.health, 580, 20)
        self.dtext("P1: " + str(score[0]), score_font, RED, 20, 60)
        self.dtext("P2: " + str(score[1]), score_font, RED, 580, 60)

        #update countdown
        if not self.countdown_active:
          #move fighters
          fighter1.move(WIDTH, HEIGHT, fighter2, round_over)
          fighter2.move(WIDTH, HEIGHT, fighter1, round_over)
        else:
          self.handle_countdown()
          self.dtext(str(self.introCount), count_font, RED, WIDTH / 2, HEIGHT / 3)

        #update fighters
        fighter1.update()
        fighter2.update()

        #draw fighters
        fighter1.draw(screen)
        fighter2.draw(screen)

        if round_over == False:
          if fighter1.alive == False:
            player_die.play()
            score[1] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()

          elif fighter2.alive == False:
            score[0] += 1
            player_die.play()
            round_over = True
            round_over_time = pygame.time.get_ticks()
        else:
          if fighter1.alive == False and self.state == 'computer':
             screen.blit(defeat_img, (360, 150))
          else:
            screen.blit(victory_img, (360, 150))
          if pygame.time.get_ticks() - round_over_time > 2000:
            round_over = False
            fighter1 = HumanFighter(1, 200, 400, False, P1_DATA, p1_animation_paths, p1_frames, sword_fx)
            if self.state == 'human':
              fighter2 = HumanFighter(2, 800, 400, True, P2_DATA, p2_animation_paths, p2_frames, magic_fx)
            elif self.state == 'computer':
              fighter2 = ComputerFighter(2, 800, 400, True, P2_DATA, p2_animation_paths, p2_frames, magic_fx)

        for event in pygame.event.get():
          if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
          if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.pause_menu()


        pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.start_game("intro")
