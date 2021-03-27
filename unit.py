''' Стандартные модули '''
import random
''' Пользовательские модули '''
import pygame.draw
''' Локальные модули игры '''
from vector import Vector
from egg import Egg

class Unit:
	''' Класс, хранящий информацию о каждом отдельном юните '''

	''' Не знаю, что это, но это повышает производительность '''
	__slots__ = ('field', 'center', 'radius', 'width', 'color', 'class_',\
				'type_', 'health', 'maxHealth', 'damage', 'energy', 'maxEnergy',\
				'energyCons', 'speed', 'vision', 'actDist', 'scare', 'toAvoid', 'toAttack', 'toEat');

	def __init__(self, field, center, radius, width, color, class_,\
				type_, health, maxHealth, damage, energy, maxEnergy,\
				energyCons, speed, vision, actDist, scare, toAvoid, toAttack, toEat):

		''' Создание юнита '''
		self.field = field;  # Поле, на котором находится юнит
		self.x = center[0];  # Координата X юнита
		self.y = center[1];  # Координата Y юнита
		self.radius = radius;  # Радиус нарисованного на поле юнита
		self.width = width;  # Толщина окружности нарисованного юнита. 0 - сплошной круг
		self.color = color;  # Цвет юнита

		self.class_ = class_;  # Класс юнита
		self.type_ = type_;  # Тип юнита

		self.health = health;  # Здоровье юнита
		self.maxHealth = maxHealth;  # Максимальное здоровье юнита
		self.damage = damage;  # Урон юнита
		self.energy = energy;  # Текущая энергия юнита
		self.maxEnergy = maxEnergy;  # Максимально возможная энергия юнита
		self.energyCons = energyCons;  # Потребление юнитом энергии за 1 ход
		self.speed = speed;  # Скорость юнита
		self.vision = vision;  # Радиус видимости юнита
		self.actDist = actDist;  # С объектами на каком максимальном расстоянии может взаимодействовать юнит
		self.scare = scare;  # Боязливость юнита
		self.toAvoid = toAvoid;  # От кого юнит убегает
		self.toAttack = toAttack;  # На кого юнит нападает
		self.toEat = toEat;  # Список еды, которую ест юнит

		self.field.addUnit(self);  # Добавление юнита в общий список юнитов
		self.draw();  # Отображение юнита на игровом поле


	def draw(self):
		''' Отображение юнита на игровом поле '''
		pygame.draw.circle(self.field.surface, self.color, (int(self.x), int(self.y)), self.radius, self.width);


	def delete(self):
		''' Удаление юнита с поля '''
		self.field.delUnit(self);


	def move(self, vec):
		''' Перемещение юнита по заданному вектору '''
		self.x += vec.x;
		self.y += vec.y;


	def moveRandomly(self):
		''' Перемещение юнита по рандомно сгенерированному вектору '''

		''' На поле выбирается случайная точка '''
		randomDot = (random.randint(0, self.field.x), random.randint(0, self.field.y));

		'''
			По направлению к выбранной точке строится нормализованный вектор, по которому
			будет двигаться юнит
		'''
		self.move(Vector(start=(self.x, self.y), end=randomDot).normalized() * self.speed);


	def increaseEnergy(self, energy):
		''' Увеличение количества энергии юнита '''
		self.energy += energy;

		'''
			Если энергия юнита превышает максимально возможную, то лишняя
			энергия переходит в здоровье
		'''
		if(self.energy > self.maxEnergy):
			self.increaseHealth(self.energy - self.maxEnergy);
			self.energy = self.maxEnergy;


	def increaseHealth(self, health):
		''' Увеличение количества здоровья юнита '''
		self.health += health;

		'''
			Если количество здоровья юнита превышает максимально возможное,
			то лишнее здоровье удаляется
		'''
		if(self.health > self.maxHealth):
			self.health = self.maxHealth;


	def decreaseEnergy(self, energy=0):
		''' Уменьшение количества здоровья юнита '''
		
		''' Если параметр energy не передан, то списывается стандартное кол-во энергии '''
		energy = (energy or self.energyCons);

		'''
			Если у юнита меньше энергии, чем ему необходимо потратить,
			то уменьшается его здоровье
		
		'''
		if(self.energy - energy < 0):
			self.decreaseHealth(energy);

		else:
			self.energy -= energy;


	def decreaseHealth(self, health, attacker=False):
		''' Уменьшение количества здоровья юнита '''
		self.health -= health;

		''' Если здоровья не осталось - юнит умирает '''
		if(self.health < 0):

			''' Если юнит умер в бою - его энергия переходит к победителю '''
			if(attacker):
				attackerEnBefore = attacker.energy;
				attacker.increaseEnergy(self.energy);

			self.delete();


	def eat(self, food):
		''' Поедание юнитом еды '''
		
		self.increaseEnergy(food.energy);  # Переход энергии съедаемой еды к юниту

		self.field.delFood(food);  # Удаление съеденной еды с поля


	def attack(self, opponent):
		''' Проведение атаки противника '''
		opponent.decreaseHealth(self.damage, self);  # Снятие ХП у атакуемого
		self.decreaseHealth(opponent.damage, opponent);  # Снятие ХП атакуемым


	def lookAround(self):
		''' Поиск объектов (юнитов/предметов/еды), которые находятся в поле зрения юнита '''
		found = dict();  # {object : distance}

		''' Поиск юнитов в поле зрения '''
		for unit in self.field.units:

			''' Расстояние между двумя юнитами '''
			dist = Vector(start=(self.x, self.y), end=(unit.x, unit.y)).getLength();

			if(dist <= self.vision):
				found[unit] = dist;

		''' Поиск предметов в поле зрения '''
		for item in self.field.items:

			''' Расстояние между юнитом и предметом '''
			dist = Vector(start=(self.x, self.y), end=(item.x, item.y)).getLength();

			if(dist <= self.vision):
				found[item] = dist;

		''' Поиск еды в поле зрения '''
		for food in self.field.food:

			''' Расстояние между юнитом и предметом '''
			dist = Vector(start=(self.x, self.y), end=(food.x, food.y)).getLength();

			if(dist <= self.vision):
				found[food] = dist;

		return found;


	def makeStep(self):
		pass


	def spawnEgg(self, energy, spawningUnitClass):
		''' Если у юнита достаточно энергии, то он откладывает яйцо '''
		Egg(field=self.field, center=(self.x, self.y), color=self.color, type_='Civilian',\
			energy=energy, maxEnergy=energy, energyCons=self.energyCons/2, spawningUnitClass=spawningUnitClass);
		self.decreaseEnergy(energy);
