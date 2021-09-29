'''
*nogo.py*
creates and handles rectangular nogo zones

Classes:
    rec
Functions:

    angleBetween(float,float,float) - > float
    vectorintersect()->[[float]]

'''
from math import cos
from math import sin
from math import acos
from math  import sqrt
from math import pi
import numpy as np
from rectangular_nogo import rec
import matplotlib.pyplot as plt
class Shapes:
    '''
       a class to represent nogo zones

       Attributes
       ----------
       cx : float
           the x value of the centroid
       cy : float
           the y value of the centroid
       xw: float
           the xwidth
       yw : float
           the ywidth
       theta: float
           the rotation of the shape
       c00: [float,float]
           x,y location of 1 vertex
       c01: [float,float]
           x,y location of 2nd vertex
       c10: [float,float]
           x,y location of 3rd vertex
       c11: [float,float]
           x,y location of 4th vertex
       c: [[float]]
           array containing x,y locations of vertices
       maxy : float
           maximum y value of shape
       miny: float
           minimum y value of shape
       maxx: float
           maximum x value of shape
       minx: float
           minimum x value of shape
       Methods
       -------
       lineintersect(xy)
           determines the intersection of this shape and the given line segment
       pointintersect(xy)
           determines whether the given point is inside of the rectangle
       '''
    def __init__(self, cx, cy, xw, yw, theta=0,sh = "B"):
        '''
         contructs a shape object

        Parameters
        ----------
        :param cx: float
            the x location of the centroid
        :param cy: float
            the y location of the centroid
        :param xw: float
            the width in the x dir
        :param yw: float
            the width in the y dir
        :param theta: float
            the amount of rotation in radians
        :param sh: string
            string specifying the desired shape supports:
            B,S,L,U,T,BL
        '''
        self.xw = xw
        self.yw = yw
        self.c = []
        self.rects = None
        dy1 = .5*(yw+xw)*sin(pi/2 - theta)
        dy2 = .5*(yw-xw)*sin(theta)
        dx1 = .5*(yw+xw)*cos(pi/2-theta)
        dx2 = .5*(yw-xw)*cos(theta)
        if sh == "B":
            self.rects = [rec(cx,cy,xw,yw,theta)]
            self.c=self.rects[0].c
        elif sh == "S":
            self.rects = [rec(cx,cy,xw,yw,theta),
                          rec(cx-dx1+dx2,cy+dy1+dy2,yw,xw,theta),
                          rec(cx+dx1-dx2,cy-dy1-dy2,yw,xw,theta)]
            self.c = [self.rects[2].c[0],self.rects[2].c[1],self.rects[0].c[2],self.rects[1].c[1],self.rects[1].c[2],self.rects[1].c[3],self.rects[0].c[0],self.rects[2].c[3]]
        elif sh == "L":
            self.rects = [rec(cx, cy, xw, yw, theta),
                          rec(cx + dx1+dx2, cy - dy1+dy2, yw, xw,
                              theta)]
            self.c = [self.rects[1].c[0], self.rects[1].c[1], self.rects[1].c[2], self.rects[0].c[1],
                      self.rects[0].c[2], self.rects[0].c[3]]
        elif sh == "U":
           self.rects =  [rec(cx, cy, xw, yw, theta),
             rec(cx - dx1+dx2,
                 cy+dy1+dy2, yw, xw, theta),
             rec(cx + dx1 + dx2,
                 cy - dy1 + dy2, yw, xw, theta)]
           self.c = [self.rects[2].c[0], self.rects[2].c[1], self.rects[2].c[2], self.rects[0].c[1], self.rects[0].c[2],
                     self.rects[1].c[1], self.rects[1].c[2], self.rects[1].c[3]]
        elif sh == "T":
            self.rects = [rec(cx,cy,xw,yw,theta),rec(cx-dx1, cy+dy1, yw, xw, theta)]
            self.c = [self.rects[0].c[0], self.rects[0].c[1], self.rects[0].c[2], self.rects[1].c[1],
                      self.rects[1].c[2], self.rects[1].c[3],self.rects[1].c[0],self.rects[0].c[3]]

        else:
            self.rects = [rec(cx, cy, xw, yw, theta),
                          rec(cx + dx1 - dx2,
                              cy - dy1 - dy2, yw, xw,
                              theta)]
            self.c = [self.rects[1].c[0], self.rects[1].c[1], self.rects[0].c[2], self.rects[0].c[3],
                      self.rects[0].c[0], self.rects[1].c[3]]
        self.maxx = max(self.c[:][0])
        self.minx = min(self.c[:][0])
        self.maxy = max(self.c[:][1])
        self.miny = min(self.c[:][1])

    def lineintersect(self, xy):
        '''
            returns the intersections between a line segment and the rectanlge

            Parameters
            -----------
            :param xy: [float,float,float,float]
                the x,y values of both endpoints of the line segment
            :return: [[float]]
                the x,y values of the intersections
        '''
        x1, y1, x2, y2 = xy
        rA = []
        for i in range(len(self.c)):
            if i == len(self.c)-1:
                c1 = self.c[len(self.c)-1]
                c2 = self.c[0]
                r = vectorintersect([c1[0], c1[1], c2[0], c2[1]], [x1-100, y1, x2+100, y2])
                if r != None:
                    rA.append(r)
            else:
                c1 = self.c[i]
                c2 = self.c[i + 1]
                r = vectorintersect([c1[0], c1[1], c2[0], c2[1]], [x1-100, y1, x2+100, y2])
                if r != None:
                    rA.append(r)
        return rA

    def pointintersect(self, xy):
        '''
        returns whether the given point is inside of the rectangle

        Parameters
        -----------
        :param xy: [float,float]
            x,y value of point
        :return: boolean
            true if inside, false if not
        '''
        for rect in self.rects:
           if rect.pointintersect(xy):
               return True
        return False
    def getArea (self):
        '''
        returns area of shape
        :return: float
            area of shape
        '''
        return len(self.rects)*self.xw*self.yw



def angleBetween(a, b, c):
    '''
         gives the angle opposite of side a

        Parameters
        -----------
        :param a: float
            length of side a
        :param b: float
            length of side b
        :param c: float
            length of side c
        :return: double
            angle across from a in triangle
    '''
    if a == 0 or b == 0 or c == 0:
        return 0
    r = (a * a + b * b - c * c) / (2 * a * b)
    if r > 1 or r < -1:
        return 0
    else:
        return acos(r)


def vectorintersect(l1, l2):
    '''
         gives the intersection between two line segments

        Parameters
        -----------
        :param l1: [[float]]
            endpoints of first line segment
        :param l2: [[float]]
            endpoints of the second line segment
        :return: [float,float]
            x,y values of intersection (returns None if there is none)
    '''
    x11, y11, x12, y12 = l1
    x21, y21, x22, y22 = l2

    p = np.array([x11, y11])
    q = np.array([x21, y21])
    r = np.array([x12 - x11, y12 - y11])
    s = np.array([x22 - x21, y22 - y21])
    rcs = np.cross(r, s)
    if rcs != 0:
        qpr = np.cross(np.subtract(q, p), r)
        qps = np.cross(np.subtract(q, p), s)
        u = qpr / rcs
        t = qps / rcs
        if 0 <= t <= 1 and 0 <= u <= 1:
            return [p[0] + t * r[0], p[1] + t * r[1]]
    return None
#Testing method
def main():
    '''
       tests shape class

        Parameters
        -----------
        :return: none
        '''
    rect = Shapes(3.0,4.0,4.0,9.0,pi/5.0,"S")
    xy = [-3,11,10,11]
    points = rect.lineintersect(xy)
    for i in range(len(rect.c)):
        if i == len(rect.c)-1:
            plt.plot([rect.c[i][0],rect.c[0][0]],[rect.c[i][1],rect.c[0][1]], "r")
        else:
            plt.plot([rect.c[i][0], rect.c[i+1][0]], [rect.c[i][1], rect.c[i+1][1]], "r")
    plt.plot([xy[0],xy[2]],[xy[1],xy[3]],"b")
    plt.plot([-10,10],[rect.maxy,rect.maxy],"y")
    X = np.zeros(len(points))
    Y = np.zeros(len(points))
    for i in range(len(points)):
        X[i] = points[i][0]
        Y[i] = points[i][1]
    plt.plot(X,Y,"go")
    plt.axis("equal")
    plt.show()
    for i in range(len(rect.rects)):
        plt.plot([rect.rects[i].c00[0], rect.rects[i].c01[0]], [rect.rects[i].c00[1], rect.rects[i].c01[1]], "r")
        plt.plot([rect.rects[i].c01[0], rect.rects[i].c11[0]], [rect.rects[i].c01[1], rect.rects[i].c11[1]], "r")
        plt.plot([rect.rects[i].c11[0], rect.rects[i].c10[0]], [rect.rects[i].c11[1], rect.rects[i].c10[1]], "r")
        plt.plot([rect.rects[i].c10[0], rect.rects[i].c00[0]], [rect.rects[i].c10[1], rect.rects[i].c00[1]], "r")

    plt.axis("equal")
    plt.show()
if __name__ == "__main__":
    main()