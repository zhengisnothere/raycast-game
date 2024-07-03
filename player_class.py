import pygame


class Player():

  def __init__(self,x,y):
    self.dir = pygame.math.Vector2(1,0)
    self.speed = 0.12
    self.sensitivity=0.6
    self.pos=pygame.math.Vector2(x,y)

  def draw(self,screen,map_tile_size):
    scr_w,scr_h=screen.get_size()
    pygame.draw.circle(screen,(255,0,0),(scr_w/2,scr_h/2),1)
    self.draw_dir(screen,scr_w/2,scr_h/2,map_tile_size)

  def collison(self, map_group):
    pass

  def movement(self, map_width, map_height):
    key = pygame.key.get_pressed()
    if key[pygame.K_w]:
      self.pos.x += self.dir.x * self.speed
      self.pos.y -= self.dir.y * self.speed
    elif key[pygame.K_s]:
      self.pos.x += -self.dir.x * self.speed
      self.pos.y -= -self.dir.y * self.speed
    if key[pygame.K_d]:
      self.pos.x += self.dir.y * self.speed
      self.pos.y -= -self.dir.x * self.speed
    elif key[pygame.K_a]:
      self.pos.x += -self.dir.y * self.speed
      self.pos.y -= self.dir.x * self.speed
    self.pos.x = max(0, min(map_width, self.pos.x))
    self.pos.y = max(0, min(map_height, self.pos.y))

  def rotate(self):
    # key = pygame.key.get_pressed()
    # if key[pygame.K_LEFT]:
    #   self.dir.rotate_ip(self.rotate_speed)
    # elif key[pygame.K_RIGHT]:
    #   self.dir.rotate_ip(-self.rotate_speed)
    x_rel=pygame.mouse.get_rel()[0]
    if x_rel!=0:
      self.dir.rotate_ip(-x_rel*self.sensitivity)

  def draw_dir(self,screen,x,y,map_tile_size):
    front_x = x + self.dir.x * 6
    front_y = y - self.dir.y * 6
    pygame.draw.line(screen, (0, 255, 0), (x,y),(front_x, front_y),2)

  def update(self,map_width,map_height):
    self.rotate()
    self.movement(map_width,map_height)
