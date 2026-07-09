import gurobipy as gp
import numpy as np
import pylab as plt
from matplotlib import collections  as mc
from matplotlib.collections import LineCollection
from datetime import datetime


def getMid(end):
    return end+1 if end % 2 == 0 else end-1

def printTranscriptAndPlot(boat, start, end, Boats, EndPoints, points):
    
    if end >= EndPoints+Boats:
        print(f"Boat {boat} moves from endpoint {start} and ends at rendezvous {end}")
        plotLine(boat, start, end, False, points)

    elif start >= EndPoints and start < EndPoints+Boats:
        mid = getMid(end)
        print(f"Boat {boat} moves from start point {start} and then traverses line ({mid},{end})")
        plotLine(boat, start, mid, False, points)
        plotLine(boat, mid, end, True, points)

    elif start < EndPoints:
        mid = getMid(end)
        print(f"Boat {boat} moves from endpoint {start} and then traverses line ({mid},{end})")
        plotLine(boat, start, mid, False, points)
        plotLine(boat, mid, end, True, points)

def plotLine(boat, start, end, isPair, points):
    boatColors = {
        0 : "red",
        1 : "blue",
        2 : "green",
        3 : "yellow",
        4 : "orange",
    }
    if boat < 0:
        plt.plot([points[start][0], points[end][0]], [points[start][1], points[end][1]], color="black", alpha=0.01)
    else: 
        if isPair:
            plt.plot([points[start][0], points[end][0]], [points[start][1], points[end][1]], color=boatColors.get(boat % 5, "black"), linestyle='dashed', alpha=0.5)
        else:
            plt.plot([points[start][0], points[end][0]], [points[start][1], points[end][1]], color=boatColors.get(boat % 5, "black"), alpha=0.5)

# prints problem solution to output and uses matplotlib to plot the solution
def printProblem(model, x, numBoats, numLines, numEndPoints, points, Weight, transitSpeed, surveySpeed, toPDF, limitHit, maxes, pdfTitle):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # plotting lines going between survey lines
    for boat in range(numBoats):
        for l in range(numLines):
            j, k = [2*l, 2*l+1]
            for i in range(numEndPoints):
                if i != j and i != k:
                    if(x[boat, j, i] > .5):
                        printTranscriptAndPlot(boat, j, i, numBoats, numEndPoints, points)
                    if(x[boat, k, i] > .5):
                        printTranscriptAndPlot(boat, k, i, numBoats, numEndPoints, points)
    
    # plotting lines going from start point/to rendezvous
    for boat in range(numBoats):
        for i in range(numEndPoints):
            if x[boat, numEndPoints+boat, i] > .5:
                printTranscriptAndPlot(boat, numEndPoints+boat, i, numBoats, numEndPoints, points)
            if x[boat, i, numEndPoints+numBoats+boat] > .5:
                printTranscriptAndPlot(boat, i, numEndPoints+numBoats+boat, numBoats, numEndPoints, points)
    
    objectiveValue = model.ObjVal
    makespan = model.getVarByName('t').X
    weightedSumOfCosts = objectiveValue - makespan
    if Weight == 0:
        sumOfCosts = weightedSumOfCosts
    else:
        sumOfCosts = weightedSumOfCosts / Weight


    # Create a scatter plot for the points and label them
    x1, y = zip(*points)
    scatter = plt.scatter(x1, y, label="Points")

    # Annotate each point with its index
    for i, point in enumerate(points):
        ax.annotate(f'{i}', (point[0], point[1]), textcoords="offset points", xytext=(0, 5), ha='center')

    #for step-through, center graph with max and min points
    if maxes != None:
        plotLine(-1, 0, 1, True, maxes)
        plotLine(-1, 2, 3, True, maxes)

    ax.autoscale()

    ax.set_aspect('auto')

    if limitHit:
        outcome = "Suboptimal"
    else:
        outcome = "Optimal"
        
    SLCP_tradeoff_solution_title = (outcome + " SLCP Solution - " + "Lines: " + str(numLines) + ", Boats: " + str(numBoats) + ", T. Speed: " + str(transitSpeed) + ", S. Speed: " + str(surveySpeed) + 
                                    "\nTrue Obj.: " + str(round(sumOfCosts + makespan, 2)) + ", SoC: " + str(round(sumOfCosts, 2)) + ", MS: "+ str(round(makespan, 2)) + " ("+ str(round(makespan*100/sumOfCosts, 2)) + "%)" +
                                    "\nWObj.: " + str(round(objectiveValue, 2)) + ", WSoC: " + str(round(weightedSumOfCosts, 2))) + ", W: " + str(Weight)
    
    plt.title(SLCP_tradeoff_solution_title)
    plt.grid()
    if (toPDF):
        plt.savefig(f"{pdfTitle}", format="pdf")    
    else:
        plt.show()  

    plt.close()
