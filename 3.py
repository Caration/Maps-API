import os
import sys
import pygame
import requests
import sys
from random import randint
from form import Ui_Menu
from PyQt5.QtWidgets import QApplication, QMainWindow


API_KEY = '40d1649f-0493-4b70-98ba-98533de7710b'
geocode = ['Барнаул', 'Советская', '6']
decoder_request = f'http://geocode-maps.yandex.ru/1.x/?apikey={API_KEY}&geocode={",".join(geocode)}&format=json'
response = requests.get(decoder_request)

json_response = response.json()
toponym = json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']


pos = toponym['Point']['pos']
delta = '0.01'
map_file = "map.png"


class Maps:
    def __init__(self):
        self.map_file = map_file
        self.map_params = {
            "ll": ",".join(pos.split()),
            "spn": ",".join([delta, delta]),
            "l": "map",
            'pt': ""
        }

    def get_map(self):
        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, params=self.map_params)

        if not response:
            print("Ошибка выполнения запроса:")
            print("Http статус:", response.status_code,
                  "(", response.reason, ")")
            sys.exit(1)

        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def set_type(self, type):
        self.map_params['l'] = type
    
    def set_pos(self, pos):
        self.map_params['ll'] = ",".join(pos.split())

    def set_delta(self, delta):
        self.map_params['spn'] = ",".join([delta, delta])
    
    def get_pos(self, geocode):
        decoder_request = f'http://geocode-maps.yandex.ru/1.x/?apikey={API_KEY}&geocode={",".join(geocode)}&format=json'
        response = requests.get(decoder_request)
        json_response = response.json()
        toponym = json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
        pos = toponym['Point']['pos']
        return pos

    def pos_now(self):
        return self.map_params['ll'].replace(',', ' ')
    
    def set_marker(self):
        #37.617698,55.755864,pmwtm1
        self.map_params['pt'] = f'{self.map_params["ll"]},pmwtm1'


mapp = Maps()


class MyWidget(QMainWindow, Ui_Menu):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.sp = [None, None, None]

        self.pushButton.clicked.connect(self.run)
        self.radioButton.clicked.connect(self.run2)
        self.radioButton.setChecked(True)
        self.radioButton_2.clicked.connect(self.run2)
        self.radioButton_3.clicked.connect(self.run2)
        self.sl = {self.radioButton: 'map',
                   self.radioButton_2: 'sat', self.radioButton_3: 'skl'}

    def run2(self, button):
        a = self.sl[self.sender()]
        mapp.set_type(a)
    
    def run(self):
        text = self.lineEdit.text().replace(',', '')
        geocode = text.split()
        pos = mapp.get_pos(geocode)
        mapp.set_pos(pos)
        mapp.set_marker()


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
pygame.init()
running = True
clock = pygame.time.Clock()
fps = 60
pos = f'{randint(20, 80)} {randint(20, 80)}'
while running:
    mapp.get_map()
    pos1 = list(map(float, mapp.pos_now().split()))
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
                mapp.set_pos(pos)
            if event.key == pygame.K_DOWN:
                dol = float(pos1[0])
                shr = float(pos1[1])
                shr -= ((0.05 * float(delta)) + 0.001)
                if shr <= -70:
                    shr = -69.99
                pos = f'{dol} {shr}'
                mapp.set_pos(pos)
            if event.key == pygame.K_LEFT:
                dol = float(pos1[0])
                shr = float(pos1[1])
                dol -= ((0.05 * float(delta)) + 0.001)
                if dol <= -179.99:
                    dol = 179.99
                pos = f'{dol} {shr}'
                mapp.set_pos(pos)
            if event.key == pygame.K_RIGHT:
                dol = float(pos1[0])
                shr = float(pos1[1])
                dol = dol + ((0.05 * float(delta)) + 0.001)
                if dol >= 179.99:
                    dol = -179.99
                pos = f'{dol} {shr}'
                mapp.set_pos(pos)
        mapp.set_delta(delta)


pygame.quit()
os.remove(map_file)
