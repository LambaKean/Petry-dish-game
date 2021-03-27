''' Стандартные модули '''
import sys
''' Пользовательские модули '''
import pygame
''' Локальные модули игры '''
from field import Field
from civilian import Civilian
from agressor import Agressor
from window import Window
from timestamp import Timestamp
from plant import Plant


pygame.init();
''' Создание объекта, хранящего информацию и ходе игры '''
f = Field(pygame.display.set_mode((1100, 640)), (128, 212, 95));
''' Создание объекта-обертки для управления окном, открывающемся при запуске игры '''
w = Window(f);
''' Создание объекта для управления временными метками '''
t = Timestamp();

# Первоначальный спавн 5 первых мирных юнитов
Civilian(f);
Civilian(f);
Civilian(f);
Civilian(f);
Civilian(f);

# Первоначальный спавн 1 агрессивного юнита
Agressor(f);

while True:

	''' Время, прошедшее с момента запуска игры в миллисекундах '''
	currTime = pygame.time.get_ticks();

	'''
		Вычисляется, сколько раз успело пройти 40мс с момента, когда
		объекты на поле последний раз делали ход. Столько раз вызывается
		метод f.makeSteps
	'''
	for i in range(t.howManyTimesPassed('make-steps', currTime, 40)):
		''' Все объекты делают ход.'''
		f.makeSteps();
		''' Фиксируется время, в которое были сделаны ходы '''
		t.stamp('make-steps', currTime);

	'''
		Если с момента прошлой обработки собыий прошло более 100мс, то
		события обрабатываются снова
	'''
	if(t.getElapsedTime('handle-events', currTime) >= 100):
		'''
			Обработка событий, связанных с открывающимся при запуске игры окном.
			Максимум - 10 раз в секунду.
		'''
		w.handleEvents();
		''' Фиксируется время, в которое были обработаны события '''
		t.stamp('handle-events', currTime);

	'''
		Если с момента прошлой перерисовки кадра прошло более 20мс, то
		кадр перерисовывается снова
	'''
	if(t.howManyTimesPassed('redraw-frame', currTime, 20)):
		''' Перерисовка кадра. Максимум - 50 FPS'''
		w.redrawFrame();
		''' Фиксируется время, в которое была сделана перерисовка кадра '''
		t.stamp('redraw-frame', currTime);

	'''
		Вычисляется, сколько раз успело пройти 450мс с момента спавна
		прошлого растения. Столько раз спавнится новое растение.
	'''
	for i in range(t.howManyTimesPassed('spawn-plant', currTime, 450)):
		''' Спавн еды. Раз в 450мс '''
		Plant(f);
		''' Фиксируется время, в которое было заспавнено растение '''
		t.stamp('spawn-plant', currTime);