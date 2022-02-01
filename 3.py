import os
import sys
import pygame
import requests


API_KEY = '40d1649f-0493-4b70-98ba-98533de7710b'
geocode = ['Барнаул', 'Советская', '6']
decoder_request = f'http://geocode-maps.yandex.ru/1.x/?apikey={API_KEY}&geocode={",".join(geocode)}&format=json'
response = requests.get(decoder_request)

json_response = response.json()
toponym = json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']



pos = toponym['Point']['pos']
delta = '0.01'
map_file = "map.png"



def mapp(pos, delta):
    global map_file
    map_params = {
        "ll": ",".join(pos.split()),
        "spn": ",".join([delta, delta]),
        "l": "map"
    }
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)


    if not response:
        print("Ошибка выполнения запроса:")
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
    
    with open(map_file, "wb") as file:
        file.write(response.content)


pygame.init()
running = True
clock = pygame.time.Clock()
fps = 60
while running:
    mapp(pos, delta)
    pos1 = list(map(float, pos.split()))
    screen = pygame.display.set_mode((600, 450))
    screen.blit(pygame.image.load(map_file), (0, 0))
    clock.tick(fps)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                delta = str(float(delta) - float(delta) * 0.5)
                if float(delta) <= 0:
                    delta = '0.00000000000000000000000001'
            if event.key == pygame.K_PAGEDOWN:
                delta = str(float(delta) + float(delta) * 1.1)
                if float(delta) >= 40.0:
                    delta = str(39.9)
            if event.key == pygame.K_UP:
                dol = float(pos1[0])
                shr = float(pos1[1])
                shr += ((0.05 * float(delta)) + 0.001)
                if shr >= 80:
                    shr = 79.99
                pos = f'{dol} {shr}'
            if event.key == pygame.K_DOWN:
                dol = float(pos1[0])
                shr = float(pos1[1])
                shr -= ((0.05 * float(delta)) + 0.001)
                if shr <= -70:
                    shr = -69.99
                pos = f'{dol} {shr}'
            if event.key == pygame.K_LEFT:
                dol = float(pos1[0])
                shr = float(pos1[1])
                dol -= ((0.05 * float(delta)) + 0.001)
                if dol <= -179.99:
                    dol = 179.99
                print(dol)
                pos = f'{dol} {shr}'
            if event.key == pygame.K_RIGHT:
                dol = float(pos1[0])
                shr = float(pos1[1])
                dol += ((0.05 * float(delta)) + 0.001)
                if dol >= 179.99:
                    dol = -179.99
                pos = f'{dol} {shr}'

pygame.quit()
os.remove(map_file)