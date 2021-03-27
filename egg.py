''' Стандартные модули '''
import random
import traceback
''' Локальные модули игры '''
from item import Item

class Egg(Item):
	''' Класс, добавляющий в игру яица, откладываемые юнитами '''

	def __init__(self, field, center=False, radius=4, width=0, color=(0, 0, 0),\
				class_='Egg', type_='', health=1, maxHealth=1, damage=0, energy=0,\
				maxEnergy=0, energyCons=0, speed=0, vision=0, actDist=0, toAvoid=[], toAttack=[],
				spawningUnitClass=None):
		''' Создание яйца '''

		if not (type_ and energy and maxEnergy and energyCons):
			''' Если обязательные параметры не переданы '''
			raise TypeError('field, type_, energy, maxEnergy and energyCons parameters are required.');
			
		if not center:
			''' Если точка спавна яйца не была задана - она выбирается рандомно '''
			center = (random.randint(10, field.x-10), random.randint(10, field.y-10));

		''' Класс юнита, который должен вылупиться из яйца '''
		self.spawningUnitClass = spawningUnitClass;

		super().__init__(field, center, radius, width, color, class_,\
						type_, health, maxHealth, damage, energy, maxEnergy,\
						energyCons, speed, vision, actDist, toAvoid, toAttack);


	def decreaseEnergy(self):
		''' Уменьшение количества здоровья яйца '''

		'''
			Если у предмета меньше энергии, чем ему необходимо потратить,
			то из яйца вылупляется юнит
		
		'''
		if(self.energy - self.energyCons < 0):
			self.spawnUnit();

		else:
			self.energy -= self.energyCons;

	def spawnUnit(self):
		''' Вылупление юнита из яйца '''
		try:
			''' Спавн юнита '''
			self.spawningUnitClass(field=self.field, center=(self.x, self.y), energy=self.maxEnergy);
		except TypeError as te:
			print("TypeError in '{}' in spawnUnit()\n\t{}".format(__file__, te));
		finally:
			''' Удаление яйца с поля '''
			self.delete();