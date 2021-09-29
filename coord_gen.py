'''
*coord_gen.py*
Used to create an instance of a borefield

Functions:

    genBoreHoleConfig(float,float,float,float,float,float,object,int,float) -> [[float]]
    plotField([[float]],object,string,boolean,object) -> none
    processRows(float,float,object,float,float,float,float,int)
    def Between(float,float,float) -> double
    distribute(float,float,float,float,[[float]]) -> appends to given array

'''
import math
import numpy as np
from math import pi
import matplotlib.pyplot as plt
import operator
from nogo import Shapes
from matplotlib.backends.backend_pdf import PdfPages

def genBoreHoleConfig(BaseSLoc,BaseWidth,TopSLoc,TopWidth,YSpac,XSpac,shape,maxLength = 250,minVert=.75):
    '''
    Function generates a series of x,y points repersenting a field of bore holes
    in a trapezoidal shape. Returs empty if boreHole field does not meet given requirements

    Parameters
    -------------
        :param BaseSLoc: [float,float]
            x,y coordinates of the leftmost point of the base of the trapezoid
        :param BaseWidth: float
            the width of the base of the trapezoid
        :param TopSLoc: [float,float]
            x,y coordinates of the leftmost point of the top of the trapezoid
        :param TopWidth: float
            the width of the top of the trapezoid
        :param YSpac: float
            the minimum spacing between points in the y-dir
        :param XSpac: float
            the minimum spacing between points in the x-dir
        :param shape: shape object
            the obstruction or "nogo zone" to the borefield
        :param maxLength: int
            the maximum number of boreholes allowed in the field
        :param minVert: float
            the fraction of vertices of the no-go zone required to be in the bore hole field
        :return: [[float]] -> 2 col + n rows
    '''
    minVert =minVert*len(shape.c)

    nrows = int((TopSLoc[1]-BaseSLoc[1])//YSpac)
    rowspace = float((TopSLoc[1]-BaseSLoc[1]))/nrows

    s1 = ((TopSLoc[0]-BaseSLoc[0])/(TopSLoc[1]-BaseSLoc[1]))
    s2 = ((TopSLoc[0]-BaseSLoc[0]+TopWidth-BaseWidth)/(TopSLoc[1]-BaseSLoc[1]))
    nin = 0
    for cen in shape.c:
        if cen[1] > TopSLoc[1] or cen[1] < BaseSLoc[1]:
            continue
        elif cen[0] > BaseSLoc[0] + s1*cen[1] and cen[0] < BaseSLoc[0]+BaseWidth + s2*cen[1]:
            nin+=1
    if nin < minVert:
        return []
    boreHoles =np.array( [row for i in range(nrows+1) if not (rows := ProcessRows(BaseSLoc,rowspace,shape,XSpac,s1,BaseWidth,s2,i))==None for row in rows])
    if len(boreHoles) > maxLength:
        return []
    return boreHoles


def plotField (points,shape,title = "BoreField",SaveOrShow = True,Pdf = None):
    '''
     Function graphs given bore hole field
    Parameters
    -------------
        :param points: [[float]]
            array containing series of x,y points
        :param shape: object shape
            shape object representing obstruction used to generate series of x,y points
        :param title: string
            tile of figure
        :param SaveOrShow: boolean
            True if diplay is desired, False if figure should be saved
        :param Pdf: Pdf Object
            Object where figure should be saved
        :return: Nothing

    '''
    plt.clf()
    fig = plt.figure(figsize=(10,7))
    plt.rcParams.update({"font.size": 18})
    plt.title(title)
    for i in range(len(shape.c)):
        if i == len(shape.c)-1:
            plt.plot([shape.c[i][0],shape.c[0][0]],[shape.c[i][1],shape.c[0][1]], "r")
        else:
            plt.plot([shape.c[i][0], shape.c[i+1][0]], [shape.c[i][1],shape.c[i+1][1]], "r")
    X = points[:,0]
    Y = points[:,1]
    plt.plot(X,Y,"bo")
    plt.axis("equal")
    if SaveOrShow:
        plt.show()
    else:
        Pdf.savefig(fig)
    plt.close()
    return

def main():
    return

def ProcessRows (BaseSLoc,rowspace,shape,XSpac,s1,BaseWidth,s2,i):
    '''
    Function generates a row of the borefield
    *Note: the formatting from the rows can be a little unexpected. Some adjustment
    may be required to correct the formatting. The genBoreHoleConfig function already accounts for this.
    Parameters
    -------------
    :param BaseSLoc: [float,float]
        x,y location of the leftmost point of the trapezoid
    :param rowspace: float
        the spacing between rows
    :param shape: shape object
        object representing "no-go" zone
    :param XSpac: float
        minimum spacing between columns
    :param s1: float
        slope of the left side of the trapezoid
    :param BaseWidth: float
        with of the base of the trapezoid
    :param s2: float
        slope of the rights side of the trapezoid
    :param i: int
        the index of the currunt row
    :return: [[float]]
        two dimensional array containing the x,y values of the bore holes for this row
    '''
    rA = []
    currentY = BaseSLoc[1] + rowspace * i
    rowsx = BaseSLoc[0] + s1 * currentY
    rowex = BaseSLoc[0] + BaseWidth + s2 * currentY
    currentX = rowsx
    ncol = int((rowex - rowsx) // XSpac)
    inters = shape.lineintersect([currentX, currentY, rowex, currentY])
    noin = len(inters)
    if noin > 0:
        inters.sort(key=operator.itemgetter(0))
    if noin > 1:
        if inters[0][0] < rowsx and inters[noin - 1][0] > rowex:
            inside = False
            for inter in inters:
                if inter[0] >= rowsx and inter[0] <= rowex:
                    inside = True
            if not inside:
                if shape.pointintersect([(rowex+rowsx)/2,currentY]):
                    return
    inters = np.array(inters)
    indices = [j for j in range(noin) if not (inters[j][0] > rowex or inters[j][0] < rowsx)]
    inters = inters[indices]
    noin = len(inters)
    for i in range(noin-1):
        spac = float(inters[i+1][0]-inters[i][0])
        if spac < XSpac and shape.pointintersect([(inters[i+1][0]+inters[i][0])/2,currentY]):
            inters[i+1][0] += (XSpac-spac)/2
            inters[i][0] -= (XSpac-spac)/2
    if ncol < 1:
        if not shape.pointintersect([(rowsx + rowex) / 2, currentY]):
            return[[(rowsx + rowex) / 2, currentY]]
    else:
        if noin == 0:
            distribute(rowsx, rowex, currentY, XSpac,rA)
        elif noin == 2:
            if shape.pointintersect([(inters[0][0] + inters[1][0]) / 2, currentY]):
                distribute(rowsx, inters[0][0] , currentY, XSpac,rA)
                distribute(inters[1][0], rowex, currentY, XSpac,rA)
            else:
                distribute(inters[0][0], inters[1][0], currentY, XSpac,rA)
        elif noin == 1:
            if shape.pointintersect([rowex, currentY]):
                distribute(rowsx, inters[0][0], currentY, XSpac,rA)
            else:
                distribute(inters[0][0], rowex, currentY, XSpac,rA)
        elif noin % 2 == 0:
            i = 0
            while i < noin:
                if i == 0:
                    distribute(rowsx, inters[0][0], currentY, XSpac,rA)
                    i = 1
                    continue
                elif i == noin - 1:
                    distribute(inters[noin - 1][0], rowex, currentY, XSpac,rA)
                else:
                    distribute(inters[i][0], inters[i + 1][0], currentY, XSpac,rA)
                i += 2
        else:
            if shape.pointintersect([rowex, currentY]):
                i = 0
                while i < noin:
                    if i == 0:
                        distribute(rowsx, inters[0][0], currentY, XSpac,rA)
                        i = 1
                        continue
                    elif i == noin - 1:
                        i += 2
                        continue
                    else:
                        distribute(inters[i][0], inters[i + 1][0], currentY, XSpac,rA)
                    i += 2
            else:
                i = 0
                while i < noin:
                    if i == noin - 1:
                        distribute(inters[noin - 1][0], rowex, currentY, XSpac,rA)
                    else:
                        distribute(inters[i][0], inters[i + 1][0], currentY, XSpac,rA)
                    i += 2
    return rA
def Between(x1,x2,x3):
    '''
    Function determines whenther x1 lies between x2 and x3
    Parameters
    -------------
    :param x1: [float,float]
        point 1
    :param x2: [float,float]
        point 2
    :param x3: [float,float]
        point 3
    :return:
    '''
    if x1 >= x2 and x1 <= x3:
        return True
    return False
def distribute(x1,x2,y,spacing,r):
    '''
      Function generates a series of boreholes between x1 and x2
    Parameters
    -------------
    :param x1: float
        left x value
    :param x2: float
        right x value
    :param y: float
        y value of row
    :param spacing: float
        spacing between columns
    :param r: [[float]]
        existing array of points
    :return:
    '''
    if x2-x1 < spacing:
        r.append([(x2+x1)/2, y])
        return
    currentX = x1
    actncol = int((x2 - x1) // spacing)
    actSpac = float(x2 - x1) / actncol
    while (currentX - x2) <= (1e-12):
        r.append([currentX, y])
        currentX += actSpac
    return


if __name__ == "__main__":
    main()