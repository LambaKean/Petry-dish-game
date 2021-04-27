class Vector:
    '''Класс для работы с векторами в двумерной плоскости'''

    def __init__ (self, start=(0, 0), end=(0, 0)):
        ''' Инициализация вектора '''

        self.startX = start[0];
        self.startY = start[1];
        self.endX = end[0];
        self.endY = end[1];

        self.x = self.endX - self.startX;
        self.y = self.endY - self.startY;


    def __add__(self, another):
        '''Суммирование векторов'''

        if(type(self) == type(another)):

            endX = self.endX + (another.endX - another.startX);
            endY = self.endY + (another.endY - another.startY);

            return Vector( (self.startX, self.startY), (endX, endY) );

        else:
            raise TypeError("Unsupported operand type for +: %s and 'Vector'" % str(type(another)));


    def __mul__(self, another):
        '''Умножение векторов'''

        if(type(self) == type(another)):  # Скалярное умножение векторов

            return (self.endX-self.startX) * (another.endX-another.startX) + (self.endY-self.startY) * (another.endY-another.startY);

        elif (type(another) == type(int()) or type(another) == type(float())):  # Умножение вектора на скаляр

            endX = self.endX + (self.endX - self.startX) * (another - 1);
            endY = self.endY + (self.endY - self.startY) * (another - 1);

            return Vector( (self.startX, self.startY), (endX, endY) );

        else:

            raise TypeError("Unsupported operand type for *: %s and 'Vector'" % str(type(another)));


    def __str__(self):
        '''Задает строковое прдеставление вектора (для отладки)'''

        return '({0};{1}) -> ({2};{3})'.format(self.startX, self.startY, self.endX, self.endY);


    def getLength(self):
        '''Вычисляет и возвращает длину вектора'''

        return ((self.endX - self.startX)**2 + (self.endY - self.startY)**2)**0.5;


    def getAngleWith(self, another):
        '''Возвращает угол между двумя векторами.'''
        
        return math.fabs(self.getAtan2() - another.getAtan2());


    def normalized(self):
        '''Нормализация вектора - приведение его длины к единице'''

        length = self.getLength();
        return Vector( (self.startX, self.startY), ( self.startX + (self.endX - self.startX)/length,\
                        self.startY + (self.endY - self.startY)/length) );


    def getAtan2(self):
        '''Возвращает угол между вектором и осью X (в градусах, от 0 до 359 градусов)'''

        angle = math.degrees(math.atan2(self.endY - self.startY, self.endX - self.startX));
        if angle < 0:
            return angle + 360;

        return angle;


    def rotated(self, angle):
        '''Поворот вектора (против часовой стрелки)'''

        pass;


    def draw(self, field, width=1, color=(0, 0, 0)):
        '''Отрисовка вектора на экране (для отладки)'''

        pygame.draw.line(field.surface, color, self.start, self.end, width);


    def inverted(self):
        '''Возвращает инвертированный вектор'''

        dx = self.endX - self.startX; # Дельта X
        dy = self.endY - self.startY; # Дельта Y

        return Vector((self.startX, self.startY), (self.startX - dx, self.startY - dy));
