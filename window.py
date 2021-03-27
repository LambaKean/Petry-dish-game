''' Стандартные модули '''
import sys
''' Пользовательские модули '''
import pygame

class Window ():
	''' Класс-обертка для управления открывающимся при запуске игры окном '''

	def __init__(self, field):
		''' Инициализация окна '''
		self.field = field; # Отображаемое в окне игрвое поле


	def handleEvents(self):
		''' Обработка событий, находящихся в очереди на обработку '''
		for event in pygame.event.get():
			
			if event.type == pygame.QUIT:
				pygame.quit();
				sys.exit();


	def redrawFrame(self):
		''' Перерисовка кадра '''
		self.field.surface.fill(self.field.background);  # Перерисовка заднего фона

		for unit in self.field.units:
			unit.draw();  # Перерисовка юнитов

		for item in self.field.items:
			item.draw();  # Перерисовка предметов

		for food in self.field.food:
			food.draw();  # Перерисовка еды

		pygame.display.flip();  # Обновление экрана