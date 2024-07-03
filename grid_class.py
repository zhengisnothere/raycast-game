import random
import pygame

from cache import image_dict


image_names=['stone_brick','carved_pumpkin','bamboo','oak_plank','bricks','mossy_stone_brick','grass_block']

tile_styles=[(1,1,1,1),(1,1,1,0),(1,1,0,0),(1,0,0,0)]

def shift_list(list,shift):
  return list[shift:] + list[:shift]

class Grid_Map:
  def __init__(self,map_width,map_height,big_tile_size,map_tile_size,map_show_size):
    self.map_width=map_width
    self.map_height=map_height
    self.big_tile_size=big_tile_size
    self.map_show_size=map_show_size
    self.create_map(map_width,map_height,big_tile_size)
    self.map_tile_size=map_tile_size
    self.map_tile=pygame.Surface((map_tile_size,map_tile_size))
    self.map_tile.fill((255,255,255))
    self.image_size=self.matrix[0][0].image_size

  def create_map(self,map_width,map_height,big_tile_size):
    self.matrix=[[Grid(x,y,'blank') for x in range(map_width*big_tile_size)] for y in range(map_height*big_tile_size)]
    for iy in range(map_height):
      for ix in range(map_width):
        if ix==0 or iy==0 or ix==map_width-1 or iy==map_height-1:
          self.change_one_tile(ix,iy,'wall',tile_styles[0],'bricks.png')
        elif random.randint(0,5)==1:
          style=shift_list(random.choice(tile_styles),random.randint(0,3))
          image_name=random.choice(image_names)+'.png'
          self.change_one_tile(ix,iy,'wall',style,image_name)

  def change_one_tile(self,x,y,wall_type,style,image_name=None):
    sx,sy=x*self.big_tile_size,y*self.big_tile_size
    for iy in range(self.big_tile_size):
      for ix in range(self.big_tile_size):
        if wall_type=='wall':
          tile=Grid(sx+ix,sy+iy,'wall',image_name) if style[iy*2+ix]==1 else Grid(x,y,'blank')
        else:
          tile=Grid(sx+ix,sy+iy,'blank')
        self.matrix[sy+iy][sx+ix]=tile

  def draw_map(self,px,py,screen):
    for iy in range(self.map_show_size):
      for ix in range(self.map_show_size):
        x,y=int(px+ix)-self.map_show_size//2,int(py+iy)-self.map_show_size//2
        if x>=0 and y>=0 and x<self.map_width*self.big_tile_size and y<self.map_height*self.big_tile_size:
          grid=self.matrix[y][x]
          if grid.type=='wall':
            screen.blit(self.map_tile,(self.map_tile_size*ix,self.map_tile_size*iy))

class Grid():
  def __init__(self,index_x,index_y,type,image_name=None):
    self.index_x = index_x
    self.index_y = index_y
    self.type = type
    if type == 'wall':
      self.image=image_dict[image_name]
    else:
      self.image = pygame.Surface((0,0))
    self.pos=pygame.math.Vector2(index_x,index_y)
    self.image_size=self.image.get_width()