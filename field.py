class Field():
	''' Класс, являющийся абстрактным представлением игрового поля и
		содержащий всю информацию об этом поле (ширина, высота, 
		цвет фона, список сущностей на поле) и методы изменения
		параметров игрового поля
	'''

	''' Не знаю, что это, но это повышает производительность '''
	__slots__ = ('units', 'items', 'food', 'surface', 'x', 'y', 'background');

	def __init__(self, surface, background=(0, 0, 0)):
		''' Создание игрового окна (поля) '''
		self.units = list();  # Список всех находящихся на поле юнитов
		self.items = list();  # Список всех находящихся на поле предметов
		self.food = list();  # Список всей находящейся на поле еды

		self.surface = surface;  # Объект pygame.Surface создаваемого поля: pygame.display.set_mode((x, y));

		self.x = self.surface.get_width();  # Ширина поля
		self.y = self.surface.get_height();  # Высота поля
		self.background = background;  # Цвет игрового поля

		self.setBackground(self.background); # Заливка игрового поля цветом


	def setBackground(self, background=(0, 0, 0)):
		''' Изменение цвета игрового поля '''
		self.surface.fill(background);
		self.background = background;


	def addUnit(self, unit):
		''' Добавление нового юнита в список '''
		self.units.append(unit);


	def addItem(self, item):
		''' Добавление нового предмета в список '''
		self.items.append(item)


	def addFood(self, food):
		''' Добавление новой еды в список '''
		self.food.append(food);


	def delUnit(self, unit):
		''' Удаление юнита с поля '''
		self.units.remove(unit);


	def delItem(self, item):
		''' Удаление предмета с поля '''
		self.items.remove(item);


	def delFood(self, food):
		''' Удаление еды с поля '''
		self.food.remove(food);


	def makeSteps(self):
		''' Все сущности (юниты, предметы, еда) на поле делают ход '''

		for unit in self.units:
			unit.makeStep();  # Каждый юнит в списке делает ход
			unit.decreaseEnergy();  # Каждый юнит на поле тратит энергию

		for item in self.items:
			item.makeStep();  # Каждый предмет на поле делает ход
			item.decreaseEnergy();  # Каждый предмет на поле тратит энергию

		for food in self.food:
			food.makeStep();  # Каждая еда на поле делает ход
			food.decreaseEnergy(); # Каждая еда на поле тратит энергию