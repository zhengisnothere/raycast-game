import pygame
import sys

from raycaster_class_optimized import Raycaster
from player_class import Player
from grid_class import Grid_Map

pygame.init()
big_tile_size=2
map_width=20
map_height=20
map_tile_size=6
map_show_size=14
map_scr_w, map_scr_h = map_show_size * map_tile_size, map_show_size * map_tile_size
game_scr_w, game_scr_h = 600, 400
win_w, win_h = game_scr_w, game_scr_h
map_screen = pygame.Surface((map_scr_w, map_scr_h))
game_screen = pygame.Surface((game_scr_w, game_scr_h))
window = pygame.display.set_mode((win_w, win_h))
pygame.display.set_caption('Raycaster')
clock = pygame.time.Clock()
font = pygame.font.SysFont("monospace", 12)

def clear_screens():
  window.fill((255,255,255))
  game_screen.fill((200,200,200))
  map_screen.fill((0, 0, 0))

def draw_text(screen, text, pos):
  text_image = font.render(str(text), 1, (0,255,0))
  screen.blit(text_image, pos)

def draw_screens():
  window.blit(game_screen, (0, 0))
  window.blit(map_screen, (0, 0))

tile_group = Grid_Map(map_width,map_height,big_tile_size,map_tile_size,map_show_size)
raycaster = Raycaster(map_width*big_tile_size,map_height*big_tile_size,tile_group.image_size)
player = Player(2.5,2.5)

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        pygame.quit()
        sys.exit()
  clear_screens()

  player.update(map_width*big_tile_size,map_height*big_tile_size)

  tile_group.draw_map(player.pos.x,player.pos.y,map_screen)
  raycaster.raycast(game_screen,player.dir,player.pos,tile_group)
  player.draw(map_screen,map_tile_size)

  draw_screens()
  draw_text(window,round(clock.get_fps(),2),(0,0))
  
  pygame.display.flip()
  clock.tick(30)
