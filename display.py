ROOTDIR = '/bigdrive/Photos/wedding sort/uniq'
wanted_tags = [
'EXIF ExifVersion',
'Image Make',
'Image Model'
]

import os
import pygame
import pprint
import pickle
import exifread
from datetime import datetime
from datetime import timedelta
import time

pygame.init()
w = 800
h = 800
size=(w,h)
screen = pygame.display.set_mode(size)
c = pygame.time.Clock() # create a clock object for timing

with open('tags.pkl', 'rb') as pkl_file:
    tags = pickle.load(pkl_file)
def get_tags(file):
    return tags[file]

def id(tag):
    try:
        id = ', '.join(sorted([tag['EXIF ExifImageWidth'].printable, tag['EXIF ExifImageLength'].printable]))+', '
    except KeyError:
        id = ''
    for key in wanted_tags:
        try:
            id += tag[key].printable+', '
        except KeyError:
            id += '!, '
    return id

paths = []
for subdir, dirs, files in os.walk(ROOTDIR):
    for filename in files:
        path = os.path.join(subdir, filename)
        tag = get_tags(path)
        try:
            paths.append([path, id(tag), datetime.strptime(tag['Image DateTime'].printable, '%Y:%m:%d %H:%M:%S')])
        except KeyError:
            paths.append([path, id(tag), datetime.strptime('9999:01:01 12:12:12', '%Y:%m:%d %H:%M:%S')])



font = pygame.font.Font(None, 36)

def update_image(path):
    screen.fill((250, 250, 250))
    img = pygame.image.load(path[0])
    width, height = img.get_size()
    img = pygame.transform.scale(img, (800, 600) if width > height else (600, 800))
    screen.blit(img,(0,0))
    text = font.render(path[1], 1, (200, 10, 10))
    textpos = text.get_rect()
    textpos.centerx = screen.get_rect().centerx
    screen.blit(text, textpos)
    text = font.render(str(path[2]), 1, (200, 10, 10))
    textpos = text.get_rect()
    textpos.centerx = screen.get_rect().centerx
    textpos.centery = 40
    screen.blit(text, textpos)
    pygame.display.flip() # update the display

def timeshift(paths, tag, seconds):
    for path in paths:
        if path[1] == tag:
            path[2] = path[2] + timedelta(seconds = seconds)
    return sorted(paths, key=lambda f: f[2])

exit = False
current_image = 0
update_image(paths[current_image])
while not exit:
    paths = sorted(paths, key=lambda f: f[2])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                current_image = min(len(paths), max(0, current_image-1))
                update_image(paths[current_image])
            elif event.key == pygame.K_RIGHT:
                current_image = min(len(paths), max(0, current_image+1))
                update_image(paths[current_image])
            if event.key == pygame.K_UP:
                paths = timeshift(paths, paths[current_image][1], 60 if pygame.key.get_mods() & pygame.KMOD_SHIFT else 1)
                update_image(paths[current_image])
            elif event.key == pygame.K_DOWN:
                paths = timeshift(paths, paths[current_image][1], -(60 if pygame.key.get_mods() & pygame.KMOD_SHIFT else 1))
                update_image(paths[current_image])
    c.tick(60) # only three images per second

