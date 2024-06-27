import pygame
import random

class Base_Fighter():
  def __init__(self, player, x, y, flip, data, image_paths, frames, sound):
    self.player = player
    self.width = data[0][0]
    self.height = data[0][1]
    self.scale = data[1]
    self.offset = data[2]
    self.flip = flip
    self.action = 0
    self.frame_index = 0
    self.frames = frames
    self.animations = self.load_images(image_paths, frames)
    self.image = self.animations[self.action][self.frame_index]
    self.update_time = pygame.time.get_ticks()
    self.rect = pygame.Rect((x, y, 80, 180))
    self.x_velocity = 10
    self.y_velocity = 0
    self.running = False
    self.jump = False
    self.attacking = False
    self.attack_sound = sound
    self.hit = False
    self.alive = True
    self.health = 100
    self.attack_type = 0
    self.attack_cooldown = 0



  def load_images(self, images, frames):
        animation_list = []
        for y,animation in enumerate(frames):
          temp_img_list = []
          for x in range(animation):
            frame = pygame.image.load(images[y]).convert_alpha()
            temp_img = frame.subsurface(x * self.width, 0, self.width, self.height)
            temp_img_list.append(pygame.transform.scale(temp_img, (self.width * self.scale, self.height * self.scale)))
          animation_list.append(temp_img_list)
        return animation_list

  def move(self, screen_width, screen_height, target, round_over):
    GRAVITY = 2
    dx = 0
    dy = 0
    self.running = False
    self.attack_type = 0
  
    if target.rect.centerx + dx > self.rect.centerx:
      self.flip = False
    else:
      self.flip = True



    self.y_velocity += GRAVITY
    dy += self.y_velocity

    #ensure player stays on screen
    if self.rect.left + dx < 0:
      dx = -self.rect.left
    if self.rect.right + dx > screen_width:
      dx = screen_width - self.rect.right
    if self.rect.bottom + dy > screen_height - 20:
      self.rect.bottom = screen_height - 20
      dy = 0
      self.jump = False
      self.y_velocity = 0


    #apply attack cooldown
    if self.attack_cooldown > 0:
      self.attack_cooldown -= 1

    #update player position
    self.rect.x += dx
    self.rect.y += dy

  #handle animation
  def update(self):
        # Handle death
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(7)  
        # Handle being hit
        elif self.hit:
            self.update_action(6)
        # Handle attacking
        elif self.attacking:
            if self.attack_type == 1:
                self.update_action(4)
            elif self.attack_type == 2:
                self.update_action(5)
        # Handle jumping
        elif self.jump:
            if self.y_velocity >=0:
                self.update_action(3)
            else:
                self.update_action(2)
        # Handle running
        elif self.running:
            self.update_action(1)
        # Default to idle
        else:
            self.update_action(0)

        # Animation update
        animation_cooldown = 80
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            if self.frame_index >= len(self.animations[self.action]):
                if self.alive:
                    self.frame_index = 0
                    if self.action in [4, 5, 6]:  # Reset attacking or being hit
                      self.attacking = False
                      self.hit = False
                      self.attack_cooldown = 20
                else:
                    self.frame_index = len(self.animations[self.action]) - 1
            self.update_time = pygame.time.get_ticks()
            self.image = self.animations[self.action][self.frame_index]

  def attack(self, target):
    if self.attack_cooldown == 0:
        self.attacking = True
        self.attack_sound.play()

        attacking_rect = pygame.Rect(self.rect.centerx - (3 * self.rect.width * self.flip), self.rect.y, self.rect.width * 3, self.rect.height * 1.5)
        if attacking_rect.colliderect(target.rect):
            if self.player == 1:
                target.health -= 8
                target.hit = True
            if self.player == 2:
                if self.attack_type == 1:
                    target.health -= 10
                    target.hit = True
                else:
                    target.health -= 10
                    target.hit = True

            self.attack_cooldown = 20



  def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

  def draw(self, surface):
    img = pygame.transform.flip(self.image, self.flip, False)
    surface.blit(img, (self.rect.x - (self.offset[0] * self.scale), self.rect.y - (self.offset[1] * self.scale)))





class HumanFighter(Base_Fighter):
    def __init__(self, player, x, y, flip, data, image_paths, frames, sound):
        super().__init__(player, x, y, flip, data, image_paths, frames, sound)

    def move(self, screen_width, screen_height, target, round_over):
        super().move(screen_width, screen_height, target, round_over)
        key = pygame.key.get_pressed()
        dx = 0

        if not self.attacking and self.alive and not round_over:
            if self.player == 1:
                if key[pygame.K_a]:
                    dx = -self.x_velocity
                    self.running = True
                if key[pygame.K_d]:
                    dx = self.x_velocity
                    self.running = True
                if key[pygame.K_w] and not self.jump:
                    self.y_velocity = -30
                    self.jump = True
                if key[pygame.K_r]:
                    self.attack_type = 1
                    self.attack(target)
                if key[pygame.K_t]:
                    self.attack_type = 2
                    self.attack(target)

            elif self.player == 2:
                if key[pygame.K_LEFT]:
                    dx = -self.x_velocity
                    self.running = True
                if key[pygame.K_RIGHT]:
                    dx = self.x_velocity
                    self.running = True
                if key[pygame.K_UP] and not self.jump:
                    self.y_velocity = -30
                    self.jump = True
                if key[pygame.K_i]:
                    self.attack_type = 1
                    self.attack(target)
                if key[pygame.K_o]:
                    self.attack_type = 2
                    self.attack(target)     

        self.rect.x += dx


    def attack(self, target):
        super().attack(target)
        self.update()

    def update(self):
        super().update()

    def draw(self, surface):
        super().draw(surface)

    def update_action(self, new_action):
        super().update_action(new_action)




class ComputerFighter(Base_Fighter):
    def __init__(self, player, x, y, flip, data, image_paths, frames, sound):
        super().__init__(player, x, y, flip, data, image_paths, frames, sound)
        self.ai_decision_interval = 300
        self.last_decision_time = 0
        self.last_jump_time = 0
        self.jump_cooldown = 2000
        self.attack_cooldown = 20

    def move(self, screen_width, screen_height, target, round_over):
        self.update()
        current_time = pygame.time.get_ticks()
        if current_time - self.last_decision_time > self.ai_decision_interval:
            self.decide(screen_width, screen_height, target, round_over)
            self.last_decision_time = current_time

        if not self.attacking and self.alive and not round_over:
            self.rect.x += self.x_velocity

        super().move(screen_width, screen_height, target, round_over)

    def decide(self, screen_width, screen_height, target, round_over):
        if not self.attacking and self.alive and not round_over:
            distance = target.rect.x - self.rect.x
            abs_distance = abs(distance)

            # Move towards the player
            if distance < 0:
                self.running = True
                self.x_velocity = -abs(self.x_velocity)
            else:
                self.running = True
                self.x_velocity = abs(self.x_velocity)

            # Jump if far away from the player
            current_time = pygame.time.get_ticks()
            if abs_distance > 150 and not self.jump and current_time - self.last_jump_time > self.jump_cooldown:
                self.y_velocity = -30
                self.jump = True
                self.last_jump_time = current_time
            if abs_distance < 480 and self.attack_cooldown == 0:
                self.attack_type = random.choice([1, 2])
                self.attack(target)

    def attack(self, target):
      super().attack(target)
      self.update()


    def update(self):
        super().update()

    def update_action(self, new_action):
        super().update_action(new_action)
    def draw(self, surface):
        super().draw(surface)


