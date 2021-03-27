''' Стандартные модули '''
import random
''' Локальные модули игры '''
from unit import Unit
from vector import Vector

class Agressor (Unit):
	'''Юнит: Агрессор, поедает других юнитов'''

	def __init__(self, field, center=False, radius=5,\
				width=1, color=(224, 67, 67), class_='Agressor', type_='Agressor',\
				health=420, maxHealth=450, damage=32, energy=230, maxEnergy=290,\
				energyCons=0.07, speed=2.8, vision=155, actDist=3, scare=1,\
				toAvoid=[],\
				toAttack=['Civilian'],\
				toEat=[]):
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
		nearestTarget = False;  # Ближайшая цель, на которую должен нападать юнит

		for obj in found.keys():
			''' Реагирование на найденные в поле зрения объекты '''

			if(obj.class_ in self.toAvoid):
				''' Если юнит пытается избегать найденный в поле зрения объект '''

				''' Строится дополнительный вектор, уводящий юнита от объекта '''
				v += Vector(start=(self.x, self.y), end=(obj.x, obj.y)).normalized().inverted() * self.scare;


			elif(obj.class_ in self.toAttack):
				''' Если юнит хочет атаковать найденный в поле зрения объект '''

				if(found[obj] < self.actDist):
					''' Если объект находится достаточно близко, то юнит атакует его '''
					self.attack(obj);
				
				elif not nearestTarget:
					'''
						Если obj - это первая замеченная юнитом цель для атаки, то
						она помечается как ближайшая
					'''
					nearestTarget = obj;

				elif(found[obj] < found[nearestTarget]):
					'''
						Если замеченная юнитом цель ближе к нему, чем та, которая
						считалась ближайшей раньше, то новая цель помечается как ближайшая
					'''
					nearestTarget = obj;



			elif(obj.class_ in self.toEat):
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
					Если ближайшая еда находится недочтаточно близко, 
					то строится вектор, приближающий юнита к еде
				'''
				v += Vector(start=(self.x, self.y), end=(nearestFood.x, nearestFood.y)).normalized();

		if nearestTarget:
			'''
				Если в поле зрения юнита была обнаружена цель для атаки,
				то строится вектор, приближающий юнита к цели
			'''
			v += Vector(start=(self.x, self.y), end=(nearestTarget.x, nearestTarget.y)).normalized();


		if(self.energy >= 250):
			''' Если у юнита достаточно энергии, то он откладывает яйцо '''
			self.spawnEgg(80, Agressor);

		if(v.x or v.y):
			''' Если юнит нашел, что ему делать - он перемещается по построенному вектору '''
			self.move(v.normalized() * self.speed);
		else:
			''' Если юнит не нашел, что ему делать - он перемещается рандомно '''
			self.moveRandomly();