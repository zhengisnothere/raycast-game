import pygame
import math

class Raycaster():

  def __init__(self, map_width, map_height, tile_image_size):
    self.max_distance = 50
    self.fov = 80
    self.res = 1
    self.wall_height = 2
    self.dv = 0
    self.map_width = map_width
    self.map_height = map_height
    self.tile_image_size = tile_image_size
    self.aim=False

  def draw_texture_line(self, screen, sp, ep, texture, texture_x, half_start, brightness):
    sx, sy = sp
    ex, ey = ep
    tx = self.tile_image_size / 2 * (texture_x + half_start) - 1
    line = texture.subsurface(pygame.Rect(tx, 0, 1, self.tile_image_size))
    height = abs(sy - ey)
    stretched_line = pygame.transform.scale(line, (self.res, height))
    if self.aim:
      scr_w=screen.get_width()
      max_height=math.sqrt((scr_w*0.2)**2-(sx-scr_w*0.5)**2)*2
      if height > max_height:
        sy+=(height-max_height)/2
        stretched_line=stretched_line.subsurface(pygame.Rect(0,(height-max_height)/2,1,max_height))
    # stretched_line.set_alpha(brightness)
    screen.blit(stretched_line, (sx, sy))

  def draw_wall_line(self, screen, scr_x, distance, texture, texture_x, half_start):
    scr_w, scr_h = screen.get_size()
    half_wall_height = self.wall_height * self.dv / distance / 2
    draw_start_y = scr_h / 2 - half_wall_height
    draw_end_y = scr_h / 2 + half_wall_height
    brightness = max(0, min(255, 255 - distance * 255 / self.max_distance))
    self.draw_texture_line(screen, (scr_x, draw_start_y), (scr_x, draw_end_y), texture, texture_x, half_start, brightness)

  def single_ray(self,ray_screen,scr_x,v_ray_dir,player_dir,player_pos,map_group):
    # use DDA algorithm
    v_ray_start = player_pos
    mapx, mapy = int(v_ray_start.x), int(v_ray_start.y)
    v_unit_step = pygame.math.Vector2(
        abs(1 / v_ray_dir.x) if v_ray_dir.x != 0 else float('inf'),
        abs(1 / v_ray_dir.y) if v_ray_dir.y != 0 else float('inf'))
    v_ray_length = pygame.math.Vector2()
    stepx = -1 if v_ray_dir.x < 0 else 1
    v_ray_length.x = (v_ray_start.x - mapx) * v_unit_step.x if v_ray_dir.x < 0 else (mapx + 1 - v_ray_start.x) * v_unit_step.x
    stepy = -1 if v_ray_dir.y < 0 else 1
    v_ray_length.y = (v_ray_start.y - mapy) * v_unit_step.y if v_ray_dir.y < 0 else (mapy + 1 - v_ray_start.y) * v_unit_step.y

    hit = False
    travel_distance = 0
    side = 0

    while not hit and 0 <= mapx < self.map_width and 0 <= mapy < self.map_height and travel_distance <= self.max_distance:
      if v_ray_length.x < v_ray_length.y:
        mapx += stepx
        travel_distance = v_ray_length.x
        v_ray_length.x += v_unit_step.x
        side = 0
      else:
        mapy += stepy
        travel_distance = v_ray_length.y
        v_ray_length.y += v_unit_step.y
        side = 1

      if 0 <= mapx < self.map_width and 0 <= mapy < self.map_height:
        tile = map_group.matrix[mapy][mapx]
      if tile.type == 'wall':
        hit = True

    if hit:
      v_intersection = v_ray_start + v_ray_dir * travel_distance
      texture = tile.image
      if side == 0:
        texture_x = v_intersection.y - tile.index_y if v_ray_dir.x > 0 else 1 + tile.index_y - v_intersection.y
        half_start = tile.index_y % 2
      else:
        texture_x = 1 - v_intersection.x + tile.index_x if v_ray_dir.y > 0 else v_intersection.x - tile.index_x
        half_start = tile.index_x % 2
      distance = (v_ray_length.x - v_unit_step.x) if side == 0 else (v_ray_length.y - v_unit_step.y)
      distance *= math.cos(-math.atan2(v_ray_dir.y, v_ray_dir.x) - math.atan2(player_dir.y, player_dir.x))
      self.draw_wall_line(ray_screen, scr_x, distance, texture, texture_x, half_start)

  def raycast(self,ray_screen,player_dir,player_pos,map_group):
    self.aim=False
    self.fov=80
    ray_scr_w, ray_scr_h = ray_screen.get_size()
    ray_scr_x = 0
    ray_num = ray_scr_w // self.res
    self.dv = ray_scr_w / 2 / math.tan(math.radians(self.fov / 2))
    for i in range(ray_num):
      
      dir_angle = math.atan2(player_dir.y, player_dir.x) + math.atan((ray_scr_w / 2 - ray_scr_x) / self.dv)      
      v_ray_dir = pygame.math.Vector2(math.cos(dir_angle), math.sin(-dir_angle)).normalize()
      self.single_ray(ray_screen,ray_scr_x,v_ray_dir,player_dir,player_pos,map_group)
      ray_scr_x+=self.res
    if not self.aim:
      pygame.draw.rect(ray_screen, (0, 255, 0),(ray_scr_w/2-1, ray_scr_h/2-1, 2, 2))
    ray_scr_x = ray_scr_w*0.3
    ray_num = int(ray_scr_w*0.4 // self.res)
    if pygame.mouse.get_pressed()[2]:
      self.aim=True
    if self.aim:
      self.fov=40
      self.dv = ray_scr_w / 2 / math.tan(math.radians(self.fov / 2))
      pygame.draw.circle(ray_screen,(0,0,0),(ray_scr_w/2,ray_scr_h/2),ray_scr_w*0.2+10,10)
      pygame.draw.circle(ray_screen,(200,200,200),(ray_scr_w/2,ray_scr_h/2),ray_scr_w*0.2)
      for i in range(ray_num):
        dir_angle = math.atan2(player_dir.y, player_dir.x) + math.atan((ray_scr_w / 2 - ray_scr_x) / self.dv)      
        v_ray_dir = pygame.math.Vector2(math.cos(dir_angle), math.sin(-dir_angle)).normalize()
        self.single_ray(ray_screen,ray_scr_x,v_ray_dir,player_dir,player_pos,map_group)
        ray_scr_x+=self.res
      pygame.draw.circle(ray_screen,(255,0,0),(ray_scr_w/2,ray_scr_h/2),10,2)
      pygame.draw.circle(ray_screen,(255,0,0),(ray_scr_w/2,ray_scr_h/2),1)