# DhilltOS, Graphical edition
# 2023, Mizu, kevadesu and contributors
import pygame, json, sys, os, datetime, time, box

def writeText(window, font_name, string, x, y, colour, fs, bg = None):
	font = pygame.font.Font(f'storage/fonts/{font_name}.ttf', fs)
	text = font.render(string, True, colour)
	if not bg is None:
		rect = text.get_rect()
		rect.x += x
		rect.y += y
		pygame.draw.rect(screen, bg, rect)
	window.blit(text, (x,y))

def putImage(window, image, x, y, mode="center"):
	rect = image.get_rect()
	screenRect = screen.get_rect()
	if mode == "center":
		rect.center = (screenRect.centerx + x, screenRect.centery + y)
	window.blit(image, (x,y), rect)

with open('machine.json', 'r') as f:
	MACHINE_SETTINGS = json.loads(f.read())
VERSION = [1, 0, 0, 'dev']

# initialize it
pygame.init()

# configurations
frames_per_second = MACHINE_SETTINGS['capped_fps']
window_width = MACHINE_SETTINGS['default_resolution'][0]
window_height = MACHINE_SETTINGS['default_resolution'][1]

# creating window
screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
vstring = '.'.join([str(e) for e in VERSION])
pygame.display.set_caption(f'DhilltOS v{vstring} (starting up) @ expects {frames_per_second}FPS')

SYS_IMAGES = {}
for img in os.listdir('storage/sys/img'):
	if os.path.isfile('storage/sys/img/' + img) and not img.startswith('_'):
		SYS_IMAGES['.'.join(img.split('.')[:-1])] = pygame.image.load('storage/sys/img/' + img)
SYS_IMAGES['lock'] = pygame.transform.scale(SYS_IMAGES['lock'], (window_width, window_height))
screen.blit(SYS_IMAGES['bootlogo'], (0,0), screen.get_rect()); pygame.display.flip()
writeText(screen, 'VictorMono/VictorMono-Bold', 'Resources imported', 0, 0, (255, 255, 255), 12, (0, 64, 0)); pygame.display.flip()
writeText(screen, 'VictorMono/VictorMono-Bold', 'Drivers ready', 0, 12, (255, 255, 255), 12, (0, 64, 0)); pygame.display.flip()

# creating our frame regulator
clock = pygame.time.Clock()

dt = 0
# forever loop
pygame.display.set_caption(f'DhilltOS v{vstring} (login) @ {frames_per_second}FPS')
while True:
	# fill the screen with a color to wipe away anything from last frame
	screen.fill("black")

  	# event loop
	screen.blit(SYS_IMAGES['lock'], (0,0), screen.get_rect())
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == pygame.VIDEORESIZE:
			screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
			SYS_IMAGES['lock'] = pygame.transform.scale(SYS_IMAGES['lock'], (event.w, event.h))
		elif event.type == pygame.MOUSEBUTTONUP:
			box.mouse_up(event)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			box.mouse_down(event)
		elif event.type == pygame.MOUSEMOTION:
			box.mouse_move(event)
		

	if dt > 0 and MACHINE_SETTINGS['display_fps']:
		writeText(screen, 'VictorMono/VictorMono-Regular', f'{round(1/dt)} FPS', 0, 0, (255, 255, 255), 12, (64, 64, 64))

	pygame.display.flip()

	# frame clock ticking
	dt = clock.tick(frames_per_second) / 1000