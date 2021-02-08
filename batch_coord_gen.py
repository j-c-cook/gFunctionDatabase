'''
*batch_coord_gen.py*
Used to create an instance of a borefield

Functions:

    genCases([float,float],[float,float],[float,float],[float,float],float,float,
              float,float,float,float,float,float,float,float
              ,float,float,float,float,float,float,string,string,[float,float]
              ,[float,float],float,float,float,float,float,float,
              float,float,float,float,float,string,boolean,
              boolean,int,boolean,float,float,float) -> none
    main() -> none

'''
from math import pi
import math
import time
import coord_gen as InnerProgram
import csv
import random
from nogo import Shapes
from matplotlib.backends.backend_pdf import PdfPages

def genCases (BaseSLocStart,BaseSLocStop,TopSLocStart,TopSLocStop,BaseWidthStart,BaseWidthStop,
              TopWidthStart,TopWidthStop,YSpacStart,YSpacStop,XSpacStart,XSpacStop,xwStart,xwStop
              ,ywStart,ywStop,cxStart,cxStop,cyStart,cyStop,BaseFileName="",Directory="",BaseSLocStep=[1,1]
              ,TopSLocStep=[1,1],BaseWidthStep=1,TopWidthStep=1,YSpacStep=1,XSpacStep=1,xwStep=1,ywStep=1,
              cxStep=1,cyStep=1,thetaStart=pi/8,thetaStop=pi/2.0,thetaStep=pi/11,unit="m",graph = False,
              outputCases = True,SampleRate = 1000,Show = False,minArea = .45,maxArea=.55,mV = .75):
    '''
    Function generates a series of x,y points repersenting a field of bore holes
    in a trapezoidal shape. Returs empty if boreHole field does not meet given requirements

    Parameters
    -------------
    :param BaseSLocStart: [float,float]
        the initial value of the location of the base of the field
    :param BaseSLocStop: [float,float]
        the final value of the location of the base of the field
    :param TopSLocStart: [float,float]
        the initial value of the location of the top of the field
    :param TopSLocStop: [float,float]
        the final value of the location of the top of the field
    :param BaseWidthStart: float
        the initial value of the width of the base of the field
    :param BaseWidthStop: float
        the final value of the width of the base of the field
    :param TopWidthStart: float
        the initial value of the width of the top of the field
    :param TopWidthStop: float
        the final value fo the width of the top of the field
    :param YSpacStart: float
        the initial value for the minimum spacing in the y-dir
    :param YSpacStop: float
        the final value for the minimum spacing in the y-dir
    :param XSpacStart: float
        the intial value for the minimum spacing in the x-dir
    :param XSpacStop: float
        the final value for the minimum spacing int the x-dir
    :param xwStart: float
        the intial value for the xwidth of the nogo zone
    :param xwStop: float
        the final value for the xwidth of the nogo zone
    :param ywStart: float
        the initial value for the ywidth of the nogo zone
    :param ywStop: float
        the final value for the ywidth of the nogo zone
    :param cxStart: float
        the initial x value for the centroid of the nogo zone
    :param cxStop: float
        the final x value for the centroid of the nogo zone
    :param cyStart: float
        the initial y value for the centroid of the nogo zone
    :param cyStop: float
        the final y value for the centroid of the nogo zone
    :param BaseFileName: string
        the base filename to store bore fields (case number is appended to this)
    :param Directory: string
        the directory to place bore field csv files
    :param BaseSLocStep: [float,float]
        the stepsize to increment the x,y location of the base of the field
    :param TopSLocStep: [float,float]
        the stepsize to increment the x,y location of the top of the field
    :param BaseWidthStep: float
        the stepsize to increment the width of the base of the field
    :param TopWidthStep: float
        the stepsize to increment the width of the top of the field
    :param YSpacStep: float
        the stepsize to increment the y spacing of the field
    :param XSpacStep: float
        the stepsize to increment the x spacing of the field
    :param xwStep: float
        the stepsize to increment the xwidth of the nogo zone
    :param ywStep: float
        the stepsize to increment the ywidth of the nogo zone
    :param cxStep: float
        the stepsize to increment the x value of the centroid of the nogo zone
    :param cyStep: float
        the stepsize to increment the y vlaue of the centroid of the nogo zone
    :param thetaStart: float
        the initial value of the rotation of the nogo zone
    :param thetaStop: float
        the final value of the rotation of the nogo zone
    :param thetaStep: float
        the stepsize to increment the rotation of the nogo zone
    :param unit: string
        string containting the deisred unit only m is currently supported
    :param graph: boolean
        decides whether random cases should be selected and graphed for user inspection
    :param outputCases: boolean
        decides whether csv files should be written
    :param SampleRate: int
        integer controlling how often the generated cases are sampled
    :param Show: boolean
        decides whether graphed fields should be displayed (true) or thrown to file (false)
    :param minArea: float
        the minimum area of the field that the nogo zone should take up
    :param maxArea: float
        the maximum are of the field that the nogo zone should take up
    :param mV: float
        the fraction of vertices of the nogozone that should be inside the field
    :return: nothing
    '''

    start = time.time()
    BaseSLocStartx,BaseSLocStarty=BaseSLocStart
    BaseSLocStopx,BaseSLocStopy = BaseSLocStop
    TopSLocStartx,TopSLocStarty = TopSLocStart
    TopSLocStopx,TopSLocStopy = TopSLocStop
    BaseSLocStepx,BaseSLocStepy=BaseSLocStep
    TopSLocStepx,TopSLocStepy = TopSLocStep
    numberOfPos = ((math.floor((TopWidthStop-TopWidthStart)/TopWidthStep)+1)* (math.floor((BaseWidthStop-BaseWidthStart)/BaseWidthStep)+1)
                  * (math.floor((BaseSLocStopx-BaseSLocStartx)/BaseSLocStepx)+1) * (math.floor((BaseSLocStopy-BaseSLocStarty)/BaseSLocStepy)+1)*
                   (math.floor((TopSLocStopx-TopSLocStartx)/TopSLocStepx)+1)* (math.floor((TopSLocStopy-TopSLocStarty)/TopSLocStepy)+1)*
                   (math.floor((thetaStop - thetaStart) / thetaStep) + 1)*(math.floor((cxStop-cxStart)/cxStep)+1)*(math.floor((cyStop-cyStart)/cyStep)+1)*
                   (math.floor((ywStop - ywStart) / ywStep) + 1)*(math.floor((xwStop-xwStart)/xwStep)+1)*(math.floor((YSpacStop-YSpacStart)/YSpacStep)+1)*
                   (math.floor((XSpacStop - XSpacStart) / XSpacStep) + 1)*6
                   )
    print("Number of Possible Fields",numberOfPos)


    if unit == "m":
        unit = "(m)"
    else:
        unit = "(ft)"
    n = 0
    shapeStrings = ["S","U","T","L","Baseball","B"]
    thrownOut = 0
    BoreHoleFields = {}
    selected = [0]
    selectCurrent = 0
    shapes = {}
    thrownOut = 0
    smallArea=0

    cy = cyStart
    while cy <= cyStop:
        cx = cxStart
        while cx <= cxStop:
            yw = ywStart
            while yw <= ywStop:
                xw = xwStart
                while xw<=xwStop:
                    ang = thetaStart
                    while ang <= thetaStop:
                        for shapeString in shapeStrings:
                            shape = Shapes(cx, cy, xw, yw, theta=ang,sh=shapeString)
                            XSpac = XSpacStart
                            while XSpac <= XSpacStop:
                                YSpac = YSpacStart
                                while YSpac <= YSpacStop:
                                    TopWidth = TopWidthStart
                                    while TopWidth <= TopWidthStop:
                                        BaseWidth = BaseWidthStart
                                        while BaseWidth <= BaseWidthStop:
                                            BaseSLocx = BaseSLocStartx
                                            while BaseSLocx <= BaseSLocStopx:
                                                BaseSLocy = BaseSLocStarty
                                                while BaseSLocy <= BaseSLocStopy:
                                                    TopSLocx = TopSLocStartx
                                                    while TopSLocx <= TopSLocStopx:
                                                        TopSLocy = TopSLocStarty
                                                        while TopSLocy <= TopSLocStopy:
                                                            ar = shape.getArea()/( .5 * (BaseWidth + TopWidth) * (
                                                                TopSLocy - BaseSLocy))
                                                            if ar < minArea or ar > maxArea:
                                                                TopSLocy += TopSLocStepy
                                                                smallArea += 1
                                                                continue
                                                            holes = InnerProgram.genBoreHoleConfig([BaseSLocx,BaseSLocy],BaseWidth,[TopSLocx,TopSLocy],TopWidth,YSpac,XSpac,shape,minVert=mV) #creates borefield
                                                            if len(holes)==0:
                                                                TopSLocy += TopSLocStepy
                                                                thrownOut+=1
                                                                continue
                                                            if graph:
                                                                if n == selected[selectCurrent]:
                                                                    shapes[selectCurrent] = shape
                                                                    selected.append(
                                                                    random.randrange(selected[selectCurrent]+1, selected[selectCurrent]+SampleRate, 1))
                                                                    selectCurrent+=1
                                                            BoreHoleFields[n]=holes
                                                            n+=1
                                                            TopSLocy+=TopSLocStepy
                                                        TopSLocx+=TopSLocStepx
                                                    BaseSLocy+=BaseSLocStepy
                                                BaseSLocx+=BaseSLocStepx
                                            BaseWidth+=BaseWidthStep
                                        TopWidth+=TopWidthStep
                                    YSpac += YSpacStep
                                XSpac+=XSpacStep
                        ang += thetaStep
                    xw+=xwStep
                yw+=ywStep
            cx += cxStep
        cy += cyStep
    print("Number of Cases thrown out: ",thrownOut)
    print("Number with too small of area: ",smallArea)
    print("Total Fields Generated: ", n)
    print("Beginning Outputting")
    if outputCases:
        for i in range(n):
            with open("".join([Directory, BaseFileName, "_", str(i), ".csv"]), "w") as outputFile:
                csvWriter = csv.writer(outputFile)
                csvWriter.writerow(["x" + unit, "y" + unit])
                csvWriter.writerows(BoreHoleFields[i])
    if graph:
        selected.__delitem__(len(selected)-1)
        if Show:
            i=0
            for sel in selected:
                print(sel)
                InnerProgram.plotField(BoreHoleFields[sel], shapes[i], title="Case_" + str(sel))
                i+=1
        else:
            with PdfPages(Directory + "Graphs" + ".pdf") as PdP:
                i=0
                for sel in selected:
                    InnerProgram.plotField(BoreHoleFields[sel], shapes[i], SaveOrShow=Show, Pdf=PdP, title="Case_" + str(sel))
                    i+=1
    end = time.time()
    print("Time elapsed: ",end-start)
    return
def main ():
    '''
     An example use of the genCases function
    :return: nothing
    '''
    BSLSta = [0,0]
    BSLSto = [0,0]
    TSLSta= [0,60]
    TSLSto= [40,100]
    BWSta = 60
    BWSto = 100
    TWSta = 0
    TWSto = 100
    YSSta = 5
    YSSto = 6
    XSSta = YSSta
    XSSto = YSSto
    xwSta = 14
    xwSto = 30
    ywSta = 34
    ywSto = 50
    cxSta = 20
    cxSto = 80
    cySta = 20
    cySto = 80
    xwS = 10
    ywS = xwS
    cxS = 30
    cyS = cxS
    TWS = 50
    BWS = 40
    TopSLS = [40,40]
    XSS = .5
    YSS = .5
    BFN = "\Files\Case_TTNGR"
    BD = "D:\Work\GSHP\Optimizing\Cases"
    genCases(BSLSta,BSLSto,TSLSta,TSLSto,BWSta,BWSto,TWSta,TWSto,YSSta,YSSto,XSSta,XSSto
             ,xwSta,xwSto,ywSta,ywSto,cxSta,cxSto,cySta,cySto,graph = True,
             BaseFileName = BFN,Directory = BD,xwStep = xwS,ywStep = ywS
             ,cxStep = cxS, cyStep = cyS,outputCases=False,TopSLocStep = TopSLS
             ,BaseWidthStep = BWS,TopWidthStep = TWS,SampleRate = 500,Show=True
             ,XSpacStep=XSS,YSpacStep=YSS,minArea=.45,maxArea=.55,mV = .75)

    return
if __name__ == "__main__":
    main()