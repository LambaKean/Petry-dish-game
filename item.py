''' Стандартные модули '''
import random
''' Пользовательские модули '''
import pygame.draw
''' Локальные модули игры '''
from vector import Vector

class Item:
	''' Класс, хранящий информацию о каждом предмете на поле '''

	def __init__(self, field, center, radius, width, color, class_, type_,\
				health, maxHealth, damage, energy, maxEnergy, energyCons,\
				speed, vision, actDist, toAvoid, toAttack):
		''' Создание предмета '''
		self.field = field;  # Поле, на котором находится предмет
		self.x = center[0];  # Координата X предмета
		self.y = center[1];  # Координата Y предмета
		self.radius = radius;  # Радиус нарисованного на поле предмета
		self.width = width;  # Толщина окружности нарисованного предмета.
		self.color = color;  # Цвет предмета

		self.class_ = class_;  # Класс предмета
		self.type_ = type_;  # Тип предмета

		self.health = health;  # Здоровье предмета
		self.maxHealth = maxHealth;  # Максимальное здоровье предмета
		self.damage = damage;  # Урон предмета
		self.energy = energy;  # Текущая энергия предмета
		self.maxEnergy = maxEnergy;  # Максимально возможная энергия предмета
		self.energyCons = energyCons;  # Потребление предметом энергии за 1 ход
		self.speed = speed;  # Скорость предмета
		self.vision = vision;  # Радиус видимости предмета
		self.actDist = actDist;  # Зона досягаемости предмета
		self.toAvoid = toAvoid;  # Кого избегает предмет
		self.toAttack = toAttack;  # На кого нападает предмет

		self.field.addItem(self);  # Добавление юнита в общий список юнитов
		self.draw();  # Отображение юнита на игровом поле


	def draw(self):
		''' Прорисовка предмета на игровом поле '''
		pygame.draw.circle(self.field.surface, self.color, (int(self.x), int(self.y)), self.radius, self.width);


	def delete(self):
		''' Удаление предмета '''
		self.field.delItem(self);


	def move(self, vec):
		''' Перемещение предмета по заданному вектору '''
		self.x += vec.x;
		self.y += vec.y;


	def moveRandomly(self):
		''' Перемещение предмета по рандомно сгенерированному вектору '''

		''' На поле выбирается случайная точка '''
		randomDot = (random.randint(0, self.field.x), random.randint(0, self.field.y));

		'''
			По направлению к выбранной точке строится нормализованный вектор, по которому
			будет двигаться предмет
		'''
		self.move(Vector(start=(self.x, self.y), end=randomDot).normalized() * self.speed);


	def increaseEnergy(self, energy):
		''' Увеличение количества энергии предмета '''
		self.energy += energy;

		'''
			Если энергия юнита превышает максимально возможную, то лишняя
			энергия переходит в здоровье
		'''
		if(self.energy > self.maxEnergy):
			self.increaseHealth(self.energy - self.maxEnergy);
			self.energy = self.maxEnergy;


	def increaseHealth(self, health):
		''' Увеличение количества здоровья предмета '''
		self.health += health;

		'''
			Если количество здоровья предмета превышает максимально возможное,
			то лишнее здоровье удаляется
		'''
		if(self.health > self.maxHealth):
			self.health = self.maxHealth;


	def decreaseEnergy(self, energy=0):
		''' Уменьшение количества здоровья предмета '''
		
		''' Если параметр energy не передан, то списывается стандартное кол-во энергии '''
		energy = (energy or self.energyCons);

		'''
			Если у предмета меньше энергии, чем ему необходимо потратить,
			то уменьшается его здоровье
		
		'''
		if(self.energy - energy < 0):
			self.decreaseHealth(energy);

		else:
			self.energy -= energy;


	def decreaseHealth(self, health, attacker=False):
		''' Уменьшение количества здоровья предмета '''
		self.health -= health;

		''' Если здоровья не осталось - предмет удаляется '''
		if(self.health < 0):

			''' Если предмет сломался в бою - его энергия переходит к победителю '''
			if(attacker):
				attacker.increaseEnergy(self.energy);

			self.delete();


	def attack(self, opponent):
		''' Проведение атаки противника '''
		target.decreaseHealth(self.damage, self);  # Снятие ХП у атакуемого
		self.decreaseHealth(target.damage, opponent);  # Снятие ХП атакуемым


	def lookAround(self):
		''' Поиск объектов (юнитов/предметов/еды), которые находятся в поле зрения предмета '''
		found = dict();  # {object : distance}

		''' Поиск юнитов в поле зрения '''
		for unit in self.field.units:

			''' Расстояние между предметом и юнитом '''
			dist = Vector(start=(self.x, self.y), end=(unit.x, unit.y)).length();

			if(dist <= self.vision):
				found[unit] = dist;

		''' Поиск предметов в поле зрения '''
		for item in self.field.items:

			''' Расстояние между двумя предметами '''
			dist = Vector(start=(self.x, self.y), end=(item.x, item.y)).length();

			if(dist <= self.vision):
				found[item] = dist;

		''' Поиск еды в поле зрения '''
		for food in self.field.food:

			''' Расстояние между предметом и едой '''
			dist = Vector(start=(self.x, self.y), end=(food.x, food.y)).length();

			if(dist <= self.vision):
				found[food] = dist;

		return found;


	def makeStep(self):
		''' Заглушка: предмет никак не изменяет своё состояние самостоятельно '''
		pass