''' Стандартные модули '''
import random
''' Локальные модули игры '''
from food import Food

class Plant(Food):
	''' Класс, добавляющий в игру зеленые растения '''

	def __init__(self, field, center=False, radius=3, width=1,\
				color=(37, 124, 0), class_='Plant', type_='Plant', health=30,\
				maxHealth=40, energy=20, maxEnergy=20, energyCons=0):
		''' Создание нового растения '''

		if not center:
			''' Если точка спавна растения не была задана - она выбирается рандомно '''
			center = (random.randint(10, field.x-10), random.randint(10, field.y-10));

		super().__init__(field, center, radius, width, color, class_, type_,\
						health, maxHealth, energy, maxEnergy, energyCons);