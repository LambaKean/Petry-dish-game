''' Пользовательские модули '''
import pygame.draw

class Food:
	''' Класс, харнящий ифнормацию о каждом отдельном кусочке еды '''

	''' Не знаю, что это, но это повышает производительность '''
	__slots__ = ('field', 'center', 'radius', 'width', 'color', 'class_',\
				'type_', 'health', 'maxHealth', 'energy', 'maxEnergy',\
				'energyCons');

	def __init__(self, field, center, radius, width, color, class_,\
				type_, health, maxHealth, energy, maxEnergy,\
				energyCons):

		''' Создание кусочка еды '''
		self.field = field;  # Поле, на котором находится кусочек еды
		self.x = center[0];  # Координата X кусочка еды
		self.y = center[1];  # Координата Y кусочка еды
		self.radius = radius;  # Радиус нарисованного на поле кусочка еды
		self.width = width;  # Толщина окружности нарисованного кусочка еды
		self.color = color;  # Цвет кусочка еды

		self.class_ = class_;  # Класс кусочка еды
		self.type_ = type_;  # Тип кусочка еды (подкласс)

		self.health = health;  # HP кусочка еды
		self.maxHealth = maxHealth;  # Максимальное HP кусочка еды
		self.energy = energy;  # Энергия кусочка еды
		self.maxEnergy = maxEnergy;  # Максимальная энергия кусочка еды
		self.energyCons = energyCons;  # Потребление энергии кусочком еды

		self.field.addFood(self);  # Добавление кусочка еды в общий список еды на поле
		self.draw();  # Прорисовка кусочка еды


	def draw(self):
		''' Отображение кусочка еды на игровом поле '''
		pygame.draw.circle(self.field.surface, self.color, (int(self.x), int(self.y)), self.radius, self.width);


	def delete(self):
		''' Удаление кусочка еды с поля '''
		self.field.delFood(self);


	def increaseEnergy(self, energy):
		''' Увеличение количества энергии кусочка еды '''
		self.energy += energy;

		'''
			Если энергия превышает максимально возможную, то лишняя
			энергия переходит в здоровье
		'''
		if(self.energy > self.maxEnergy):
			self.increaseHealth(self.energy - self.maxEnergy);
			self.energy = self.maxEnergy;


	def increaseHealth(self, health):
		''' Увеличение количества здоровья кусочка еды '''
		self.health += health;

		'''
			Если количество здоровья превышает максимально возможное,
			то лишнее здоровье удаляется
		'''
		if(self.health > self.maxHealth):
			self.health = self.maxHealth;


	def decreaseEnergy(self, energy=0):
		''' Уменьшение количества здоровья кусочка еды '''
		
		''' Если параметр energy не передан, то списывается стандартное кол-во энергии '''
		energy = (energy or self.energyCons);

		'''
			Если у кусочка еды меньше энергии, чем ему необходимо
			потратить, то уменьшается его здоровье
		
		'''
		if(self.energy - energy < 0):
			self.decreaseHealth(energy);

		else:
			self.energy -= energy;


	def decreaseHealth(self, health, attacker=False):
		''' Уменьшение количества здоровья кусочка еды '''
		self.health -= health;

		''' Если здоровья не осталось - кусочек еды удаляется '''
		if(self.health < 0):

			self.delete();


	def makeStep(self):
		''' Заглушка: еда никак не изменяет своё состояние самостоятельно '''
		pass