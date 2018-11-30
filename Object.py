

class object:
    def __init__(self, Id, radius, center, color):

        self.Id = Id
        self.Pos = (center[0], center[1])
        self.Radio = radius
        self.Actualizaciones = 0
        self.Color = color
        self.Goalstate = 0
        self.In = center[1] < 80
        #print(self.In)

    def getId(self):
        return self.Id

    def getPosition(self):
        return self.Pos

    def getColor(self):
        return self.Color

    def setRadio(self,radius):
        self.Radio = radius;

    def setPosition(self,center):
        self.Pos = center

    def setActualizaciones(self,value):
        self.Actualizaciones = value

    def actualizar(self):
        self.Actualizaciones = self.Actualizaciones+2

    def itsObject(self, center,range):
        (x,y) = center
        (s_x,s_y) = self.Pos
        return ((x>s_x-(range))and(x<s_x+(range))and(y>s_y-(range+50))and(y<s_y+(range-50)))

    def itsGoalstate(self,range_y):

        if not(self.Goalstate) and (self.Pos[1] > range_y) and self.In:
            self.Goalstate = 1
            return self.Goalstate

        return 0
