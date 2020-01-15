import numpy, math

def delta(speeds):
    delta = numpy.diff(speeds)
    return sum([el ** 2 for el in delta])/len(delta)

def rpm(speed, gr, tp):
    return (speed * 16.666) / (gr * tp)

def speed(rpm, gr, tp):
    return (rpm * gr * tp) / 16.666

def torque(pw, rpm):
    return (pw * 60) / (2 * math.pi * rpm)
    
class EcoDrive():

    @staticmethod
    def gear(driving, driven):
        return driving / driven
        
    @staticmethod
    def gears(*args):
        return args 
    
    def __init__(self, gears, rpm=(2500, 3500), tp=1.92):
        
        self.GEARS = gears
        self.MIN_RPM, self.MAX_RPM = rpm
        self.TP = tp
        
        self.BAD_RPM = 0.1
        
        self.speeds = []
        self.current_gear = 0
        
        self.score = 1
        
    def upadte(self, speed):
        
        self.speeds.append(speed)
        
        _rpm = rpm(speed, self.GEARS[self.current_gear], self.TP)
        
        if not _rpm > self.MIN_RPM and _rpm < self.MAX_RPM:
            self.score += self.BAD_RPM
        
        return _rpm
        
    def shift(self, inc):
        self.current_gear += int(inc/abs(inc))
        if self.current_gear < 0:
            self.current_gear = 0
        elif self.current_gear > len(self.GEARS) - 1:
            self.current_gear = len(self.GEARS) - 1
        
        
if __name__ == '__main__':
    
    ed = EcoDrive(EcoDrive.gears(
        EcoDrive.gear(1, 10),
        EcoDrive.gear(1, 7),
        EcoDrive.gear(1, 5),
        EcoDrive.gear(1, 3)
    ))

    print(ed.upadte(20))
    print(ed.upadte(40))

    print(ed.score)