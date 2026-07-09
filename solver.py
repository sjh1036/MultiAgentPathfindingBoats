from pyexpat import model

import gurobipy as gp
from gurobipy import GRB
from timeit import default_timer as timer
import visualizer 

    
# new method of finding cycles in an incumbent solution
def newFindCycles(solution, numBoats, numLines): 
    solutionList = list(solution.items())

    # Finding paths taken by each boat in incumbent solution
    boatPaths = [{} for _ in range(numBoats)]
    for lineTaken in solutionList:
        if lineTaken[1] > .5:
            line = lineTaken[0]
            boatPaths[line[0]][line[1]] = [line[1], line[2]]

    cycles = []
    # Parsing each boat's path
    for i, path in enumerate(boatPaths):
        start = numLines*2 + i
        nonCyclePath = []

        # Tracking path of boat from start to finish, removing points covered from dict as they are parsed  
        while True:
            newStart = path.pop(start, None)
            if newStart == None:
                break
            nonCyclePath.append(newStart)
            start = newStart[1]

        # If path from origin to rendezvous does not remove all points from boat's path, there must be a, or multiple, cycle(s)
        if len(path) != 0:
            while len(path) > 0:
                pathValues = list(path.values())
                cycle = []
                nextEdgeStart = pathValues[0][0]
                while True:
                    currentEdge = path.pop(nextEdgeStart, None)
                    if currentEdge == None:
                        break

                    #Finding complementary endpoint of current surveyed edge
                    if (currentEdge[1] % 2 == 0):
                        cycleLine = [currentEdge[1], currentEdge[1] + 1]
                    else:
                        cycleLine = [currentEdge[1] - 1, currentEdge[1]]
                    cycle.append(cycleLine)
                    nextEdgeStart = currentEdge[1]
                cycles.append(cycle)
        
    return cycles

def solve(numBoats, numEndPoints, points, numLines, costMatrix, Weight, transitSpeed, surveySpeed, toPDF, stepNumber, whatIfs, maxes, corner):
    SHOWPATHS = True

    # Create a Gurobi model
    model = gp.Model("MCPP")

    # Binary Edge Variable
    x = {}
    
    # creating binary edge variables (1 if edge taken, 0 if not) ------------------------------------------------------------------------------------------------------------------------------------
    
    # number of binary variables should be ((2*Lines)^2 * Boats)
    for boat in range(numBoats):
        for i in range(numEndPoints):
            # Start Point to Line
            x[boat, numEndPoints+boat,i] = model.addVar(vtype=GRB.BINARY, name=f'x_{boat}_{numEndPoints+boat}_{i}')
            # Line to Redezvous Point
            x[boat, i,numEndPoints+numBoats+boat] = model.addVar(vtype=GRB.BINARY, name=f'x_{boat}_{i}_{numEndPoints+numBoats+boat}')

    for boat in range(numBoats):
        for l in range(numLines):
            j, k = [2*l, 2*l+1]
            for i in range(numEndPoints):
                if (i != j and i != k):
                    # Line Endpoints
                    x[boat, j, i] = model.addVar(vtype=GRB.BINARY, name=f'x_{boat}_{j}_{i}')
                    x[boat, k, i] = model.addVar(vtype=GRB.BINARY, name=f'x_{boat}_{k}_{i}')
                

    # creating objective function and assigning constraints ------------------------------------------------------------------------------------------------------------------------------------

    # Makespan Variable
    t = model.addVar(vtype=GRB.CONTINUOUS, name=f't')

    # Aggregate Weight Variable
    aggregateWeight = Weight

    # Objective Function
    model.setObjective((t + aggregateWeight *
        (gp.quicksum(costMatrix[2*j][i] * x[boat, 2*j, i] for boat in range(numBoats) for j in range(numLines) for i in range(numEndPoints) if i != 2*j and i != 2*j+1) +
        gp.quicksum(costMatrix[2*j+1][i] * x[boat, 2*j+1, i] for boat in range(numBoats) for j in range(numLines) for i in range(numEndPoints) if i != 2*j and i != 2*j+1) +
        gp.quicksum(costMatrix[numEndPoints+boat][i] * x[boat, numEndPoints+boat,i] for boat in range(numBoats) for i in range(numEndPoints)) + 
        gp.quicksum(costMatrix[i][numEndPoints+numBoats+boat] * x[boat, i,numEndPoints+numBoats+boat] for boat in range(numBoats) for i in range(numEndPoints)))),
        GRB.MINIMIZE)

    # Makespan Constraint
    for boat in range(numBoats):
        model.addConstr(
            gp.quicksum(costMatrix[2*j][i] * x[boat, 2*j, i] for j in range(numLines) for i in range(numEndPoints) if i != 2*j and i != 2*j+1) +
            gp.quicksum(costMatrix[2*j+1][i] * x[boat, 2*j+1, i] for j in range(numLines) for i in range(numEndPoints) if i != 2*j and i != 2*j+1) +
            gp.quicksum(costMatrix[numEndPoints+boat][i] * x[boat, numEndPoints+boat,i]  for i in range(numEndPoints)) +
            gp.quicksum(costMatrix[i][numEndPoints+numBoats+boat] * x[boat, i,numEndPoints+numBoats+boat] for i in range(numEndPoints))
            <= t)

    # Cover Constraint
    count = 0
    for l in range(numLines):
        CoverContraints = {}
        j, k = [2*l, 2*l+1]
        for boat in range(numBoats):
            for i in range(numEndPoints):
                if j != i and k != i:
                    CoverContraints[count] = [boat, i, j]
                    count = count + 1
                    CoverContraints[count] = [boat, i, k]
                    count = count + 1
            CoverContraints[count] = [boat, numEndPoints+boat, j]
            count = count + 1
            CoverContraints[count] = [boat, numEndPoints+boat, k]
            count = count + 1
        model.addConstr(gp.quicksum(x[b,i,j] for b,i,j in CoverContraints.values()) == 1)

    # Flow Contraints
    for boat in range(numBoats):
        for l in range(numLines):
            j, k = [2*l, 2*l+1]
            model.addConstr(gp.quicksum(x[boat, i, j] for i in range(numEndPoints) if i != j and i != k) + x[boat, numEndPoints+boat, j] == gp.quicksum(x[boat, j, i] for i in range(numEndPoints) if i != j and i != k) + x[boat, j, numEndPoints+numBoats+boat])
            model.addConstr(gp.quicksum(x[boat, i, k] for i in range(numEndPoints) if i != j and i != k) + x[boat, numEndPoints+boat, k] == gp.quicksum(x[boat, k, i] for i in range(numEndPoints) if i != j and i != k) + x[boat, k, numEndPoints+numBoats+boat])

    # Start and End Contraints
    for boat in range(numBoats):
        model.addConstr(gp.quicksum(x[boat, numEndPoints+boat, i] for i in range(numEndPoints)) == 1)
        model.addConstr(gp.quicksum(x[boat, i, numEndPoints+numBoats+boat] for i in range(numEndPoints)) == 1)

    # Two Line Loops Constraint
    for l in range(numLines):
        j, k = [2*l, 2*l+1]
        for i in range(numEndPoints):
            if i != j and i != k:
                model.addConstr(gp.quicksum(x[boat, i, j] + x[boat, j, i] for boat in range(numBoats)) <= 1)
                model.addConstr(gp.quicksum(x[boat, i, k] + x[boat, k, i] for boat in range(numBoats)) <= 1)

    #What if constraints
    #trio[0] = boat #, trio[1] = opposite of desired starting endpoint (opposite end of the same line), trio[2] = opposite of desired ending endpoint (opposite end of the same line)
    for trio in whatIfs:
        try:
            model.addConstr(x[trio[0], trio[1], trio[2]] == 1)
        except KeyError as e:
            print(f"KeyError: {e}")
            return [[2, f"{e} is not a valid What-If"]]


    # callback function ---------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # Lazy Callback for Cycle Constraints
    def DisjointLazyCycleContraint(model , where):
        
        if where == gp.GRB.Callback.MIPSOL:
            # make a list of edges selected in the solution
            solution = model.cbGetSolution(model._vars)
            
            Cycles = newFindCycles(solution, numBoats, numLines)
            # NewCycles = FindCycle(numBoats, numLines, numEndPoints, x)
            # General No-Callback Loop Constraint
            if len(Cycles) > 0:
                # New Constraints (Print Constraints)
                for cycle in Cycles:
                    incomingConstraints = []
                    outgoingConstraints = []
                    cycleAsList = []
                    for line in cycle:
                        cycleAsList.append(line[0])
                        cycleAsList.append(line[1])

                    # Incoming
                    for pairInCycle in cycle:
                        j, k = [pairInCycle[0], pairInCycle[1]]
                        for boat in range(numBoats):
                            for i in range(numEndPoints):
                                u = i + 1 if i % 2 == 0 else i - 1
                                # Basic index management
                                if (i != j and i != k and i not in cycleAsList):
                                    # Add incoming constraints to all other endpoints
                                    # print("x_%g_%g_%g + x_%g_%g_%g" % (boat, i, j, boat, i, k), end=" + ")
                                    incomingConstraints.append([boat, i, j])
                                    incomingConstraints.append([boat, i, k])
                            # Add incoming constraints to from boat specific origin points
                            # print("x_%g_%g_%g + x_%g_%g_%g" % (boat, EndPoints+boat, j, boat, EndPoints+boat, k), end=" + ")
                            incomingConstraints.append([boat, numEndPoints+boat, j])
                            incomingConstraints.append([boat, numEndPoints+boat, k])
                    # print(" >= 1")                       
                    model.cbLazy(gp.quicksum(x[c[0], c[1], c[2]] for c in incomingConstraints) >= 1)

                    # Outgoing
                    for pairInCycle in cycle:
                        j, k = [pairInCycle[0], pairInCycle[1]]
                        for boat in range(numBoats):
                            for i in range(numEndPoints):
                                u = i + 1 if i % 2 == 0 else i - 1
                                # Basic index management
                                if (i != j and i != k and i not in cycleAsList):
                                    # Add outgoing constraints to all other endpoints
                                    # print("x_%g_%g_%g + x_%g_%g_%g" % (boat, j, i, boat, k, i), end=" + ")
                                    outgoingConstraints.append([boat, j, i])
                                    outgoingConstraints.append([boat, k, i])
                            # Add outgoing constraints that end at boat specific rondeview points
                            # print("x_%g_%g_%g + x_%g_%g_%g" % (boat, j, EndPoints+Boats+boat, boat, k, EndPoints+Boats+boat), end=" + ")
                            outgoingConstraints.append([boat, j, numEndPoints+numBoats+boat])
                            outgoingConstraints.append([boat, k, numEndPoints+numBoats+boat])
                    # print(" >= 1")                       
                    model.cbLazy(gp.quicksum(x[c[0], c[1], c[2]] for c in outgoingConstraints) >= 1)
 
    # optimizing model and printing results (calling visualizer and printing solution/status codes) -----------------------------------------------------------------------------------------
    
    # Optimize the model
    model._vars = x
    model.Params.lazyConstraints = 1

    # Add 10 second time limit to optimization
    model.setParam("TimeLimit", 10.0)

    # model.setParam("TuneTimeLimit", 3600.0)
    # model.tune()

    # if model.TuneResultCount > 0:
    #     # Load the best result (index 0) into the model
    #     model.getTuneResult(0)
    #     # Export the modified parameters to a file
    #     model.write("best_params.prm")

    # Start Runtime Timer
    startTime = timer()
    # model.optimize()
    model.optimize(DisjointLazyCycleContraint)
    endTime = timer()

    RUNTIME = endTime - startTime
    
    if model.status == GRB.OPTIMAL or model.status == GRB.TIME_LIMIT:
        objectiveValue = model.ObjVal
        makespan = model.getVarByName('t').X
        weightedSumOfCosts = objectiveValue - makespan
        if Weight == 0:
            sumOfCosts = weightedSumOfCosts
        else:
            sumOfCosts = weightedSumOfCosts / Weight
        unweightedObj = makespan + sumOfCosts
        
        with open("scalingtimes.txt", "a") as f:
            f.write(f"{objectiveValue}\n")
        print("\n")
        obj = str(unweightedObj)
        if model.Status == GRB.TIME_LIMIT:
            returnList = [[0, 1]]
            print("Suboptimal Solution Found - Time Limit Hit:")
            obj = obj + " 1"
        elif model.Status == GRB.OPTIMAL:
            print("Optimal Solution Found:")
            returnList = [[0, 0]]
            obj = obj + " 0"
        
        # creating pdftitle for visualizer
        whatIfOut = ""
        if len(whatIfs) > 0:
            whatIfOut = "withWhatIfs"
        pdfTitle = f"{numBoats}boats{numLines}lines{Weight}weight{stepNumber}step{whatIfOut}{corner}.pdf"  
        #appending pdfTitle to returnList for pdf merging
        returnList.append(pdfTitle)
        
        print("Total coverage time:", model.objVal)
        X = {}
        #parsing binary variables (formatted as "x_{boatnumber}_{startpoint}_{endpoint}")
        #1 if boat took line from start to end, 0 if not
        returnList.append([])
        for x in model.getVars():
            ary = x.varName.split("_")
            if ary[0] == "x":
                # print(x.VarName)
                X[int(ary[1]),int(ary[2]), int(ary[3])] = x.x
                if x.x > .5: 
                   returnList[2].append([int(ary[1]),int(ary[2]), int(ary[3])])        

        if(SHOWPATHS):
            #sending solution to formulator
            visualizer.printProblem(model, X, numBoats, numLines, numEndPoints, points, Weight, transitSpeed, surveySpeed, toPDF, model.status == GRB.TIME_LIMIT, maxes, pdfTitle)
        
        print("Total run time:", RUNTIME)
        cycles = newFindCycles(X, numBoats, numLines)
        
        if(len(cycles) != 0):
            output = f"{len(cycles)} cycle(s) of size ("
            for j, cycle in enumerate(cycles):
                if j != 0:
                    output = output + ", "
                output = output + str(len(cycle))
            output = output + ") detected!"
            print(output)
            with open("cycles.txt", "a") as f:
                f.write(f"{numBoats} boats, {numLines} lines: {output}\n")
        else: 
            print(f"No cycles detected")

        return returnList 
    
    else:
        print(f"No solution found for {numLines} lines, {numBoats} boats,  status code: {model.status}")
        # Solution was infeaseable
        return [[1]]
