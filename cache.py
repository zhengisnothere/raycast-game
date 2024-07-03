import os

import pygame


def cache_all_images(path,scale):
  for file in os.listdir(path):
    if file.endswith('.png'):
      image=pygame.image.load(os.path.join(path,file))
      image=pygame.transform.scale_by(image,scale)
      image_dict[file]=image
    else:
      cache_all_images(os.path.join(path,file),scale)

pygame.init()
image_dict={}
cache_all_images('images',2)