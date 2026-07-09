import tkinter as tk
from tkinter import *
import formulator
from tkinter.filedialog import askopenfilename
from pypdf import PdfWriter
import os

def readFromFileLabel():
    if selectReadFromFileVar.get():
        solveButton.config(text="Solve Problem From File")
    else:
        solveButton.config(text="Solve a Generated Problem")

def readTextFile():
    #reading settings from text file
    try:
        with open(textPathText.get(1.0, "end-1c")) as file:
            errorLabel.config(text="")
            for line in file:
                toLower = line.lower()
                split = toLower.split()
                if "boats" in toLower:
                    if len(split) != 2:
                        errorLabel.config(text="Invalid number of \"boats\" parameters in file")   
                        return
                    try:
                        boats = int(split[1])
                        errorLabel.config(text="")
                        boatsText.insert(tk.END, boats)
                    except ValueError:
                        errorLabel.config(text=f"{split[1]} is not a valid number of boats")
                        return
                elif "lines" in toLower:
                    if len(split) != 2:
                        errorLabel.config(text="Invalid number of \"lines\" parameters in file")   
                        return
                    try:
                        lines = int(split[1])
                        errorLabel.config(text="")
                        linesText.insert(tk.END, lines)
                    except ValueError:
                        errorLabel.config(text=f"{split[1]} is not a valid number of lines")
                        return
                elif "weights" in toLower:
                    if len(split) < 2:
                        errorLabel.config(text="Invalid number of \"weights\" parameters in file")   
                        return
                    for i in range(1, len(split)):
                        try:
                            weight = int(split[i])
                            errorLabel.config(text="")
                            weightText.insert(tk.END, weight)
                        except ValueError:
                            errorLabel.config(text=f"{split[i]} is not a valid weight")
                            return
                elif "survey" in toLower:
                    if len(split) != 2:
                        errorLabel.config(text="Invalid number of \"survey\" parameters in file")   
                        return
                    try:
                        survey = int(split[1])
                        errorLabel.config(text="")
                        surveyText.insert(tk.END, survey)
                    except ValueError:
                        errorLabel.config(text=f"{split[1]} is not a valid survey speed")
                        return
                elif "transit" in toLower:
                    if len(split) != 2:
                        errorLabel.config(text="Invalid number of \"transit\" parameters in file")   
                        return
                    try:
                        transit = int(split[1])
                        errorLabel.config(text="")
                        transitText.insert(tk.END, transit)
                    except ValueError:
                        errorLabel.config(text=f"{split[1]} is not a valid transit speed")
                        return
                elif "generation" in toLower:
                    if len(split) != 2:
                        errorLabel.config(text="Invalid number of \"generation\" parameters in file")   
                        return
                    try:
                        generation = int(split[1])
                        errorLabel.config(text="")
                        generationText.insert(tk.END, generation)
                    except ValueError:
                        errorLabel.config(text=f"{split[1]} is not a valid generation type")
                        return
                elif "steps" in toLower:
                    if len(split) != 2:
                        errorLabel.config(text="Invalid number of \"steps\" parameters in file")   
                        return
                    try:
                        steps = int(split[1])
                        errorLabel.config(text="")
                        stepsText.insert(tk.END, steps)
                    except ValueError:
                        errorLabel.config(text=f"{split[1]} is not a valid number of steps")
                        return
    except FileNotFoundError as e:
        errorLabel.config(text=f"File {textPathText.get(1.0, "end-1c")} not found")   
        return


def selectFileName(text):
    text.delete("1.0", tk.END)
    text.insert(tk.END, askopenfilename())
    
def formulateProblem(): 
    #default settings
    weights = [1]
    boats = 1
    surveySpeed = 1
    transitSpeed = 1
    numLines = 0
    whatIfs = []
    generation = 0
    numSteps = 0
    fileName = None
    writeToFileName = None

    # Error Checking For Inputs
    if (selectReadFromFileVar.get()):   
        fileName = filePathText.get(1.0, "end-1c")
         
    if (selectWriteToFileVar.get()):   
        writeToFileName = writePathText.get(1.0, "end-1c")
    
    if (len(boatsText.get(1.0, "end-1c")) != 0):   
        try:
            boats = int(boatsText.get(1.0, "end-1c"))
            errorLabel.config(text="")
        except ValueError:
            errorLabel.config(text=f"{boatsText.get(1.0, "end-1c")} is not a valid number of boats")
            return
    
    
    if (len(boatsText.get(1.0, "end-1c")) != 0):   
        try:
            boats = int(boatsText.get(1.0, "end-1c"))
            errorLabel.config(text="")
        except ValueError:
            errorLabel.config(text=f"{boatsText.get(1.0, "end-1c")} is not a valid number of boats")
            return
    else:
        errorLabel.config(text="Please enter a number of boats")   
        return
    

    if (len(linesText.get(1.0, "end-1c")) != 0):
        try:
            numLines = int(linesText.get(1.0, "end-1c"))
            errorLabel.config(text="")
        except ValueError:
            errorLabel.config(text=f"{linesText.get(1.0, "end-1c")} is not a valid number of lines")
            return    
    elif selectReadFromFileVar.get() != True:
        errorLabel.config(text=f"Please a number of lines")
        return    


    if (len(weightText.get(1.0, "end-1c")) != 0):
        weights = []
        strings = weightText.get(1.0, "end-1c").split(" ")
        for i, string in enumerate(strings):
            try:
                weights.append(float(string))
                errorLabel.config(text="")
            except ValueError:
                errorLabel.config(text=f"{string} is not a valid weight")
                return
        

    if (len(transitText.get(1.0, "end-1c")) != 0):
        try:
            transitSpeed = float(transitText.get(1.0, "end-1c"))
            errorLabel.config(text="")
        except ValueError:
            errorLabel.config(text=f"{transitText.get(1.0, "end-1c")} is not a valid transit speed")
            return


    if (len(surveyText.get(1.0, "end-1c")) != 0):
        try:
            surveySpeed = float(surveyText.get(1.0, "end-1c"))
            errorLabel.config(text="")
        except ValueError:
            errorLabel.config(text=f"{surveyText.get(1.0, "end-1c")} is not a valid survey speed")
            return    
        

    if (len(whatIfText.get(1.0, "end-1c")) != 0):
        strings = whatIfText.get(1.0, "end-1c").split()
        if (len(strings)%3!=0):
            errorLabel.config(text="Please enter What Ifs in the correct format")
            return
        
        trio = []
        for i, string in enumerate(strings):
            try:
                val = int(string)
                errorLabel.config(text="")
                trio.append(val)
                if i % 3 == 2:
                    whatIfs.append(trio)
                    trio = []
            except ValueError:
                errorLabel.config(text=f"{string} is not a valid number")
                return    
        for tri in whatIfs:
            print(f"{tri[0]}, {tri[1]}, {tri[2]}")

    if (len(generationText.get(1.0, "end-1c")) != 0):   
        try:
            generation = int(generationText.get(1.0, "end-1c"))
            errorLabel.config(text="")
            if generation > 4 or generation < 0:
                errorLabel.config(text=f"{generationText.get(1.0, "end-1c")} is not a valid generation type")
                return
        except ValueError:
            errorLabel.config(text=f"{generationText.get(1.0, "end-1c")} is not a valid generation type")
            return
    
    if (len(stepsText.get(1.0, "end-1c")) != 0):   
        try:
            numSteps = int(stepsText.get(1.0, "end-1c"))
            errorLabel.config(text="")
            if numSteps < 0:
                errorLabel.config(text=f"{stepsText.get(1.0, "end-1c")} is not a valid number of steps")
                return
        except ValueError:
            errorLabel.config(text=f"{stepsText.get(1.0, "end-1c")} is not a valid number of steps")
            return
            
    #array to be filled with file names of pdfs
    pdfs = []

    #sending problem to formulator
    outputs = formulator.formulate(fileName, boats, weights, surveySpeed, transitSpeed, numLines, toPDFVar.get(), whatIfs, generation, writeToFileName, numSteps, 0)

    #output format: [[status], [pdfFileName], [solutionLines]]
    for i, output in enumerate(outputs):
        if (output[0][0] == 0):
            if (toPDFVar.get()):
                pdfs.append(output[1])
        elif (output[0][0] == 1):
            errorLabel.config(text=f"No solution found")  
        elif (output[0][0] == 2):
            errorLabel.config(text=f"{output[0][1]}") 
        
    if (toPDFVar.get()):
        merger = PdfWriter()
        for pdf in pdfs:
            merger.append(pdf)
            os.remove(pdf)

        if len(whatIfs) > 0:
            merger.write("finalPlotWithWhatIfs.pdf")
        else:   
            merger.write("finalPlot.pdf")
        merger.close()
        
    # for purposes of producing multiple solutions
    # num = 0
    # while num < 4:
    #     outputs = formulator.formulate(fileName, boats, weights, surveySpeed, transitSpeed, numLines, toPDFVar.get(), whatIfs, generation, writeToFileName, numSteps, num)

    #     #output format: [[status], [pdfFileName], [solutionLines]]
    #     for i, output in enumerate(outputs):
    #         if (output[0][0] == 0):
    #             if (toPDFVar.get()):
    #                 pdfs.append(output[1])
    #         elif (output[0][0] == 1):
    #             errorLabel.config(text=f"No solution found")  
    #         elif (output[0][0] == 2):
    #             errorLabel.config(text=f"{output[0][1]}") 
            
    #     num += 1
        
    # if (toPDFVar.get()):
    #         merger = PdfWriter()
    #         for pdf in pdfs:
    #             merger.append(pdf)
    #             os.remove(pdf)

    #         if len(whatIfs) > 0:
    #             merger.write("finalPlotWithWhatIfs.pdf")
    #         else:   
    #             merger.write("finalPlot.pdf")
    #         merger.close()

    return
        

# UI Setup
root = Tk()
root.title("Ducklings")
root.geometry('1000x400')

row = 0

filePathLabel = tk.Label(root, text="Enter path of CSV File with Coordinates")
filePathLabel.grid(row=row, column=0, sticky=E, padx=10)

filePathText = tk.Text(master=root, height=1, width=30, )
filePathText.grid(row=row, column=1, sticky=W)

row+=1

filePathButton = tk.Button(root, text="Or upload file", command=lambda: selectFileName(filePathText))
filePathButton.grid(row=row, column=0, sticky=E, padx=10)

selectReadFromFileVar = tk.BooleanVar()
selectReadFromFileVar.set(False)

selectReadFromFile = tk.Checkbutton(
    root,
    text="Read from File",
    variable=selectReadFromFileVar,
    command=readFromFileLabel
)
selectReadFromFile.grid(row=row, column=1, sticky=W)

row+=1

writePathLabel = tk.Label(root, text="Enter path of CSV File to write coordinates")
writePathLabel.grid(row=row, column=0, sticky=E, padx=10)

writePathText = tk.Text(master=root, height=1, width=30, )
writePathText.grid(row=row, column=1, sticky=W)

row+=1

writePathButton = tk.Button(root, text="Or upload file", command=lambda: selectFileName(writePathText))
writePathButton.grid(row=row, column=0, sticky=E, padx=10)

selectWriteToFileVar = tk.BooleanVar()
selectWriteToFileVar.set(False)

selectWriteToFile = tk.Checkbutton(
    root,
    text="Write to File",
    variable=selectWriteToFileVar,
    command=writePathLabel
)
selectWriteToFile.grid(row=row, column=1, sticky=W)

row+=1

textPathLabel = tk.Label(root, text="Enter path of Text File with settings to formulate")
textPathLabel.grid(row=row, column=0, sticky=E, padx=10)

textPathText = tk.Text(master=root, height=1, width=30, )
textPathText.grid(row=row, column=1, sticky=W)

row+=1

textPathButton = tk.Button(root, text="Or upload file", command=lambda: selectFileName(textPathText))
textPathButton.grid(row=row, column=0, sticky=E, padx=10)

textReadButton = tk.Button(root, text="Load Settings", command=lambda: readTextFile())
textReadButton.grid(row=row, column=1, sticky=W)

row+=1

boatsLabel = tk.Label(master=root, text="Enter number of boats:")
boatsLabel.grid(row=row, column=0, sticky=E, padx=10)

boatsText = tk.Text(master=root, height=1, width=30, )
boatsText.grid(row=row, column=1, sticky=W)

row+=1

linesLabel = tk.Label(root, text="Enter Number of Lines to Formulate")
linesLabel.grid(row=row, column=0, sticky=E, padx=10)

linesText = tk.Text(master=root, height=1, width=30, )
linesText.grid(row=row, column=1, sticky=W)

row+=1

weightLabel = tk.Label(root, text="Enter Objective Weight(s) to solve with (default is 1)")
weightLabel.grid(row=row, column=0, sticky=E, padx=10)

weightText = tk.Text(master=root, height=1, width=30, )
weightText.grid(row=row, column=1, sticky=W)

row+=1

surveyLabel = tk.Label(root, text="Enter Survey Speed (default is 1)")
surveyLabel.grid(row=row, column=0, sticky=E, padx=10)

surveyText = tk.Text(master=root, height=1, width=30, )
surveyText.grid(row=row, column=1, sticky=W)

row+=1

transitLabel = tk.Label(root, text="Enter Transit Speed (default is 1)")
transitLabel.grid(row=row, column=0, sticky=E, padx=10)

transitText = tk.Text(master=root, height=1, width=30, )
transitText.grid(row=row, column=1, sticky=W)

row+=1

whatIfLabel = tk.Label(root, text="Enter \"What-If\" line (\"boatnumber startpoint endpoint\")")
whatIfLabel.grid(row=row, column=0, sticky=E, padx=10)

whatIfText = tk.Text(master=root, height=1, width=30, )
whatIfText.grid(row=row, column=1, sticky=W)

row+=1

generationLabel = tk.Label(root, text="Enter line generation type (0 = column, 1 = random, 2 = broken column, 3 = segmented column)")
generationLabel.grid(row=row, column=0, sticky=E, padx=10)

generationText = tk.Text(master=root, height=1, width=30, )
generationText.grid(row=row, column=1, sticky=W)

row+=1

stepsLabel = tk.Label(root, text="Enter number of steps to step through solution (default is 0)")
stepsLabel.grid(row=row, column=0, sticky=E, padx=10)

stepsText = tk.Text(master=root, height=1, width=30, )
stepsText.grid(row=row, column=1, sticky=W)

row+=1

errorLabel = tk.Label(root, text="")
errorLabel.grid(row=row, column=1, sticky=W)

row+=1

toPDFVar = tk.BooleanVar()
toPDFVar.set(False)

toPDFButton = tk.Checkbutton(
    root,
    text="Print to PDF",
    variable=toPDFVar,
)
toPDFButton.grid(row=row, column=0, sticky=E, padx=10)

solveButton = tk.Button(root, text="Solve a Generated Problem", command=lambda: formulateProblem())
solveButton.grid(row=row, column=1, sticky=W)

root.mainloop()