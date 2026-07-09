from math import inf, sqrt
from timeit import default_timer as timer
import numpy as np
import csv
import random
import solver


def formulate(fileName, numBoats, weights, surveySpeed, transitSpeed, numGenLines, toPDF, whatIfs, lineGenerationType, writeToFileName, numSteps, corner):
    #x min and max for graphing purposes
    x_max = float(-inf)
    x_min = float(inf)

    y_max = float(-inf)
    y_min = float(inf)

    #list of all points/segments to be traversed
    points = []
    segments = []
    

    if fileName != None:
        numLines = 0 #Number of lines to be counted
        #reading points from csv file
        try:
            with open(fileName, mode='r', newline='', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    if(len(row) > 0):
                        adjRow = [[float(row[0]), float(row[1])], [float(row[2]), float(row[3])]]

                        x_max = max(x_max, max(adjRow[0][0], adjRow[1][0]))
                        x_min = min(x_min, min(adjRow[0][0], adjRow[1][0]))

                        y_max = max(y_max, max(adjRow[0][1], adjRow[1][1]))
                        y_min = min(y_min, min(adjRow[0][1], adjRow[1][1]))
                            
                        points.append(adjRow[0])
                        points.append(adjRow[1])
                        segments.append(adjRow)
                        numLines += 1
        except FileNotFoundError as e:
            print(e)
            # returning 2 as error code
            return [[2, e]]
            
    else:
        #number of columns
        columns = 1
        #width of columns
        width = 30
        #spacing between columns
        column_spacing = 5
        
        #formulate problem in broken segmented column formation
        if lineGenerationType == 4:
            #number of segments per column
            numSegments = 5

            numLines = 0

            for i in range(columns):
                for j in range(1,(numGenLines + 1)):
                    for k in range(numSegments):
                        if random.random() < 0.1:
                            numLines += 1
                            adjRow = [[width * i + (k * width / numSegments) + column_spacing * i, j], [width * i + ((k + 1) * width / numSegments) + column_spacing * i, j]]

                            x_max = max(x_max, max(adjRow[0][0], adjRow[1][0]))
                            x_min = min(x_min, min(adjRow[0][0], adjRow[1][0]))

                            y_max = max(y_max, max(adjRow[0][1], adjRow[1][1]))
                            y_min = min(y_min, min(adjRow[0][1], adjRow[1][1]))
                                    
                            points.append(adjRow[0])
                            points.append(adjRow[1])

                            segments.append(adjRow)
        #formulate problem in segmented column formation
        elif lineGenerationType == 3:
            #number of segments per column
            numSegments = 5

            numLines = numGenLines * columns * numSegments

            for i in range(columns):
                for j in range(1,(numGenLines + 1)):
                    for k in range(numSegments):
                        adjRow = [[width * i + (k * width / numSegments) + column_spacing * i, j], [width * i + ((k + 1) * width / numSegments) + column_spacing * i, j]]

                        x_max = max(x_max, max(adjRow[0][0], adjRow[1][0]))
                        x_min = min(x_min, min(adjRow[0][0], adjRow[1][0]))

                        y_max = max(y_max, max(adjRow[0][1], adjRow[1][1]))
                        y_min = min(y_min, min(adjRow[0][1], adjRow[1][1]))
                                
                        points.append(adjRow[0])
                        points.append(adjRow[1])

                        segments.append(adjRow)
        #formulate problem in broken column formation
        elif lineGenerationType == 2:
    
            numLines = numGenLines * columns

            for i in range(columns):
                for j in range(1,(numGenLines + 1)):
                    randLeft = random.random() * width / 2 
                    randRight = (random.random() + 1) * width / 2
                    adjRow = [[width * i + randLeft + column_spacing * i, j], [width * (i + .5) + randRight + column_spacing * i, j]]
                    
                    x_max = max(x_max, max(adjRow[0][0], adjRow[1][0]))
                    x_min = min(x_min, min(adjRow[0][0], adjRow[1][0]))

                    y_max = max(y_max, max(adjRow[0][1], adjRow[1][1]))
                    y_min = min(y_min, min(adjRow[0][1], adjRow[1][1]))
                            
                    points.append(adjRow[0])
                    points.append(adjRow[1])

                    segments.append(adjRow)
        #formulate problem in random instance formation
        elif lineGenerationType == 1:

            numLines = numGenLines

            maxCoordinate = 50
            for j in range(0,numGenLines):
                    adjRow = [[random.random()*maxCoordinate, random.random()*maxCoordinate], [random.random()*maxCoordinate, random.random()*maxCoordinate]]

                    x_max = max(x_max, max(adjRow[0][0], adjRow[1][0]))
                    x_min = min(x_min, min(adjRow[0][0], adjRow[1][0]))

                    y_max = max(y_max, max(adjRow[0][1], adjRow[1][1]))
                    y_min = min(y_min, min(adjRow[0][1], adjRow[1][1]))
                            
                    points.append(adjRow[0])
                    points.append(adjRow[1])
                    segments.append(adjRow)
        #formulate problem in complete column formation
        elif lineGenerationType == 0:

            numLines = numGenLines * columns

            for i in range(columns):
                for j in range(1,(numGenLines + 1)):
                    adjRow = [[width * i + column_spacing * i, j], [width * (i + 1) + column_spacing * i, j]]

                    x_max = max(x_max, max(adjRow[0][0], adjRow[1][0]))
                    x_min = min(x_min, min(adjRow[0][0], adjRow[1][0]))

                    y_max = max(y_max, max(adjRow[0][1], adjRow[1][1]))
                    y_min = min(y_min, min(adjRow[0][1], adjRow[1][1]))
                            
                    points.append(adjRow[0])
                    points.append(adjRow[1])

                    segments.append(adjRow)

    

    if writeToFileName != None:
        #writing coordinates to csv file
        try:
            with open(writeToFileName, mode='w', newline='', encoding='utf-8') as file:
                csv_writer = csv.writer(file)
                for row in segments:
                    writeRow = [row[0][0], row[0][1], row[1][0], row[1][1]]
                    csv_writer.writerow(writeRow)
                print(f"writing to: {writeToFileName}")
        except FileNotFoundError as e:
            print(e)
            # returning 2 as error code
            return [[2, e]]
     
    numEndPoints = numLines*2 # Number of endpoints

    print()
    print("\n-----------------------------------------------------------------------\n")
    print("Lines: %g, Boats: %g" % (numLines, numBoats),end=" ")
    print("\n-----------------------------------------------------------------------\n")
    print()

    x_spacing = 1
    y_spacing = 1
    x_offset = 1
    y_offset = 5

    # origin points = bottom left
    if corner == 0:
        for b in range(numBoats):
            #origin
            points.append([x_min - x_offset - b*x_spacing, y_min - y_offset - b*y_spacing])
    # origin points = bottom right
    elif corner == 1:
        for b in range(numBoats):
            #origin
            points.append([x_max + x_offset + b*x_spacing, y_min - y_offset - b*y_spacing])
    # origin points = top right
    elif corner == 2:
        for b in range(numBoats):
            #origin
            points.append([x_max + x_offset + b*x_spacing, y_max + y_offset + b*y_spacing])
    # origin points = top left
    elif corner == 3:
        for b in range(numBoats):
            #origin
            points.append([x_min - x_offset - b*x_spacing, y_max + y_offset + b*y_spacing])
    
    # rendezous points = top right
    for b in range(numBoats):
            #rendezvous
            points.append([x_max + x_offset + b*x_spacing, y_max + y_offset + b*y_spacing])

    # for step through, maxes are invisibly graphed to center subsequent stepped solutions on the original
    maxes = [[x_min - x_offset - numBoats*x_spacing, 0], [x_max + x_offset + numBoats*x_spacing, 0], [0, y_min - y_offset - numBoats*y_spacing], [0, y_max + y_offset + numBoats*y_spacing]]


    costMatrix = createCostMatrix(numEndPoints, numBoats, numLines, points, transitSpeed, surveySpeed)

    outputs = []
    

    #solve formulated problem for each weight passed in
    for weight in weights:
        #sending problem to solver
        outputs.append(solver.solve(numBoats, numEndPoints, points, numLines, costMatrix, weight, transitSpeed, surveySpeed, toPDF, 0, whatIfs, None, corner))
        if numSteps > 0:
            stepNumber = 1
            stepThrough(outputs[i-1], numSteps, points, numBoats, numEndPoints, transitSpeed, surveySpeed, weight, toPDF, outputs, stepNumber, maxes)
        
    return outputs


# stepThrough divides the initial solution's makespan by the number of steps provided and progesses each boat along its path in the solution by that step time/distance
def stepThrough(solution, numSteps, points, numBoats, numEndPoints, transitSpeed, surveySpeed, weight, toPDF, outputs, stepNumber, maxes):
    #pathsList format: index = boat number, list element = [starting point, ending point, isSurveyLine]
    pathsList = [[] for _ in range(numBoats)]
    boatStarts = [[] for _ in range(numBoats)] 
    boatEnds = [[] for _ in range(numBoats)] 
    boatTimes = [0] * numBoats 
    makespan = 0.0
    makespanBoat = -1
    
    #parsing solution to individual boat paths
    for j, line in enumerate(solution):
        #line in format "[boat #, index of starting point, index of ending point]"
        if j != 0:
            start = line[1]
            end = line[2]
            #rendezvous point
            if end >= numEndPoints+numBoats:
                pathsList[line[0]].append([points[start], points[end], False])
                # boatTimes[line[0]] += findEuclideanDistance(points[start], points[end]) / transitSpeed
                boatEnds[line[0]] = points[end]
        
            else: 
                mid = getMid(end)
                pathsList[line[0]].append([points[start], points[mid], False])
                boatTimes[line[0]] += findEuclideanDistance(points[start], points[mid]) / transitSpeed

                pathsList[line[0]].append([points[mid], points[end], True])
                boatTimes[line[0]] += findEuclideanDistance(points[mid], points[end]) / surveySpeed
                
                #origin point
                if start >= numEndPoints and start < numEndPoints+numBoats:
                    boatStarts[line[0]] = points[start]

    sortedPaths = sortPaths(boatStarts, pathsList)

    #find makespan to determine step time
    for i in range(numBoats):
        if boatTimes[i] > makespan or makespanBoat == -1:
            makespanBoat = i
            makespan = boatTimes[i]


    finishedBoats = [False] * numBoats
    stepTime = makespan/numSteps
    remainingBoats = numBoats
    retainedPath = True

    #for each step, find new positions of boats, remove completed segments and boats, reformulate problem endpoints, and solve
    for i in range(numSteps):
        newPoints = []
        #find new position of each boat
        for boat in range(numBoats):
            addPoints = []
            boatStep = stepTime
            if not finishedBoats[boat]:
                #while step has not been completed by the boat
                while boatStep > 0.0:
                    #if boat has only 1 segment left, it is the segment to the rendezvous point and boat is considered finished, else, it is not
                    if len(sortedPaths[boat]) > 1:
                        lineDistance = findEuclideanDistance(sortedPaths[boat][0][0], sortedPaths[boat][0][1])
                        #if line will be completed this step
                        if boatStep >= lineDistance:
                            boatStarts[boat] = sortedPaths[boat][0][1]
                            del sortedPaths[boat][0]
                            
                        #if boat's new start point will fall on the current line segment
                        else:
                            boatStarts[boat] = findNewStart(sortedPaths[boat][0][0], sortedPaths[boat][0][1], boatStep)
                            sortedPaths[boat][0][0] = boatStarts[boat]
                            #adding remaining endpoints of boat path if they are endpoints of a survey line
                            for line in sortedPaths[boat]:
                                if line[2]:
                                    addPoints.append(line[0])
                                    addPoints.append(line[1])

                        boatStep -= lineDistance
                    
                    #removing points if boat is finished
                    else:
                        addPoints = []
                        finishedBoats[boat] = True
                        remainingBoats -= 1
                        boatStep = 0.0

                newPoints.append(addPoints)


        newPoints = combineLists(newPoints)
        newNumEndpoints = len(newPoints)
        newNumLines = int(newNumEndpoints / 2)

        #add new origin and rendezvous points for boats that are not finished
        for boat in range(numBoats):
            if not finishedBoats[boat]:
                newPoints.append(boatStarts[boat])
        for boat in range(numBoats):
            if not finishedBoats[boat]:
                newPoints.append(boatEnds[boat])
        
        #re-solve problem with remaining boats and survey lines
        if remainingBoats > 0:
            costMatrix = createCostMatrix(newNumEndpoints, remainingBoats, newNumLines, newPoints, transitSpeed, surveySpeed)
            output = solver.solve(remainingBoats, newNumEndpoints, newPoints, newNumLines, costMatrix, weight, transitSpeed, surveySpeed, toPDF, stepNumber, [], maxes)
            print(f"step #: {i}")
            if not stepThroughChecker(sortedPaths, newPoints, output, remainingBoats, finishedBoats):
                retainedPath = False
            outputs.append(output)
            stepNumber += 1
    print("All boats finished, no more steps")
    print(f"Path retained for all steps: {retainedPath}")

#validating method to check if every subsequent solution is consistent withthe original solution, ture if original solution is returned each step, false if not
def stepThroughChecker(sortedPaths, points, output, remainingBoats, finishedBoats):
    boatIDs = [0] * remainingBoats
    priorFinished = 0
    for i, finished in enumerate(finishedBoats):
        if finished:
            priorFinished += 1
        else:
            boatIDs[i-priorFinished] = i
    
    for line in output:
        if line != [0, 0] and line != [0, 1]:
            #start and end are true if the line is present in the solution and in the original solution
            start = False
            end = False
            for sortedLine in sortedPaths[boatIDs[line[0]]]:
                if round(sortedLine[0][0], 10) == round(points[line[1]][0], 10) and round(sortedLine[0][1], 10) == round(points[line[1]][1], 10):
                    start = True
                if round(sortedLine[1][0], 10) == round(points[line[2]][0], 10) and round(sortedLine[1][1], 10) == round(points[line[2]][1], 10):
                    end = True
                    
            if not start or not end:
                return False
    return True


def combineLists(listsList):
    #combineLists returns a list of all the elements in listsList
    combinedList = []
    for list in listsList:
        for e in list:
            combinedList.append(e)
    return combinedList

def sortPaths(boatStarts, pathsList):
    #sortPaths returns a list of paths for each boat in which each line segment is ordered as they are traversed by the given b oat
    sortedPaths = [[] for _ in range(len(pathsList))] 
    for i, path in enumerate(pathsList):
        start = boatStarts[i]
        while (True):
            savedStart = start
            for line in path:
                print("line start = " + str(line[0]) + "start = " + str(start))
                if line[0] == start:
                    sortedPaths[i].append(line)
                    start = line[1]
                    break

            if (start == savedStart):
                break

    return sortedPaths


def findNewStart(point1, point2, d):
    #findNewStart returns the point that is distance d along the line from point1 to point2
    #point1 is the starting point, point2 is the ending point, d is the distance travelled along the line between the two points
    D = findEuclideanDistance(point1, point2)
    if d >= D:
        return point2
    X = abs(point1[0] - point2[0])
    Y = abs(point1[1] - point2[1])
    x = X * d / D
    y = Y * d / D
    if point2[0] < point1[0]:
        x = -x
    if point2[1] < point1[1]:
        y = -y
    return [point1[0] + x, point1[1] + y]


def createCostMatrix(numEndPoints, numBoats, numLines, points, transitSpeed, surveySpeed):
    # Create Cost Matrix
    CostMatrixSize = numEndPoints + numBoats + numBoats
    costMatrix = np.array([[0.0]*(CostMatrixSize)]*(CostMatrixSize))
    costMatrix2 = np.array([[0.0]*(CostMatrixSize)]*(CostMatrixSize))
    

    # Calculate the Euclidean distances and create the cost matrix
    for i in range(CostMatrixSize):
        for j in range(CostMatrixSize):
            costMatrix2[i][j] = findEuclideanDistance(points[i], points[j])
            # costMatrix2[i][j] = np.linalg.norm(np.array(points[i]) - np.array(points[j]))

    # Calculates the path length from one endpoint to the end of a survey line
    # path length as distance to any given point plus the distance of traversing the survey line
    for l in range(numLines):
        # endpoints j and k of line l
        j, k = [2*l, 2*l+1]
        for i in range(numEndPoints):
            if(i != j and i != k):
                # endpoints i and e of line that includes i
                e = i-1
                if (i % 2) == 0:
                    e = i+1
                #applies transit/survey speeds to cost aka distance travelled per possible line
                costMatrix[j][i] = costMatrix2[j][e]/transitSpeed + costMatrix2[e][i]/surveySpeed
                costMatrix[k][i] = costMatrix2[k][e]/transitSpeed + costMatrix2[e][i]/surveySpeed
                costMatrix[i][j] = costMatrix2[i][k]/transitSpeed + costMatrix2[k][j]/surveySpeed
                costMatrix[i][k] = costMatrix2[i][j]/transitSpeed + costMatrix2[j][k]/surveySpeed
                
                

    # Calculates the path length from one endpoint to a rendezvous point and start to any endpoint
    for boat in range(numBoats):
        for i in range(numEndPoints):
            k = i-1
            if (i % 2) == 0:
                k = i+1
            costMatrix[numEndPoints+boat][i] = costMatrix2[numEndPoints+boat][k]/transitSpeed + costMatrix2[k][i]/surveySpeed
            costMatrix[i][numEndPoints+numBoats+boat] = costMatrix2[i][numEndPoints+numBoats+boat]/transitSpeed

    return costMatrix


   
def findEuclideanDistance(point1, point2):
    return sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def getMid(end):
    return end+1 if end % 2 == 0 else end-1

