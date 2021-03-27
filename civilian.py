''' Стандартные модули '''
import random
''' Локальные модули игры '''
from unit import Unit
from vector import Vector

class Civilian(Unit):
	''' Класс, добавляющий в игру мирных юнитов '''

	def __init__(self, field, center=False, radius=4, width=1,\
				color=(13, 150, 255), class_='Civilian', type_='Civilian',\
				health=100, maxHealth=150, damage=3, energy=70, maxEnergy=100,\
				energyCons=0.1, speed=2.2, vision=140, actDist=4, scare=2,\
				toAvoid=['Agressor'],\
				toAttack=[],\
				toEat=['Plant']):
		''' Создание юнита '''

		if not center:
			''' Если точка спавна юнита не была задана - она выбирается рандомно '''
			center = (random.randint(10, field.x-10), random.randint(10, field.y-10));

		super().__init__(field, center, radius, width, color, class_,\
				type_, health, maxHealth, damage, energy, maxEnergy,\
				energyCons, speed, vision, actDist, scare, toAvoid, toAttack, toEat);


	def makeStep(self):
		''' Метод определяет оптимальное решение, которое принимает юнит '''
		
		''' Объекты, находящиеся в поле зрения юнита '''
		found = self.lookAround();  # {object : distance}

		v = Vector((0, 0));  # Вектор, по которому будет двигаться юнит

		nearestFood = False;  # Ближайшая еда, находящаяся в поле зрения

		for obj in found.keys():

			if(obj.class_ in self.toAvoid):
				''' Если юнит пытается избегать найденный в поле зрения объект '''

				''' Строится дополнительный вектор, уводящий юнита от объекта '''
				v += Vector(start=(self.x, self.y), end=(obj.x, obj.y)).normalized().inverted() * self.scare;


			if(obj.class_ in self.toAttack):
				''' Если юнит хочет атаковать найденный в поле зрения объект '''
				if(found[obj] > self.actDist):
					'''
					Если объект находится недостаточно близко для нападения, то
					строится вектор, приближающий юнита к объекту
					'''
					v += Vector(start=(self.x, self.y), end=(obj.x, obj.y)).normalized();
				
				else:
					''' Если объект находится достаточно близко, то юнит атакует его '''
					self.attack(obj)


			if(obj.class_ in self.toEat):
				''' Если юнит питается найденной в поле зрения едой '''
				if not nearestFood:
					''' Если это первая еда, которую заметил юнит, то она отмечается как ближайшая '''
					nearestFood = obj;

				else:
					'''
						Если до этого юнит уже обнаруживал другую еду, то вычисляется,
						какой из двух кусочков еды ближе к юниту
					'''
					if(found[obj] < found[nearestFood]):
						'''
							Если новая обнаруженная еда ближе к юниту, чем предыдущая,
							то новая еда помечается как ближайшая
						'''
						nearestFood = obj;


		if nearestFood:
			''' Если в поле зрения юнита была обнаружена еда '''
			if(found[nearestFood] < self.actDist):
				''' Если найденная еда в зоне досягаемости - юнит ест её '''
				self.eat(nearestFood);

			else:
				'''
					Если ближайшая еда вне зоны досягаемости, то строится вектор,
					приближающий юнита к еде
				'''
				v += Vector(start=(self.x, self.y), end=(nearestFood.x, nearestFood.y)).normalized();

		if(self.energy >= 90):
			''' Если у юнита достаточно энергии, то он откладывает яйцо '''
			self.spawnEgg(40, Civilian);

		if(v.x or v.y):
			''' Если юнит нашел, что ему делать - он перемещается по построенному вектору '''
			self.move(v.normalized() * self.speed);
		else:
			''' Если юнит не нашел, что ему делать - он перемещается рандомно '''
			self.moveRandomly();