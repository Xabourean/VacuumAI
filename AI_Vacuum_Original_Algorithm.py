import re
import random
from itertools import islice

"""
NAME: Logan Daniel Sicking
This program creates a 2d environment in the shape of a rectangle or square based on user input
Within this environment every spot is dirty or clean
A vacuum is placed in the environment with the ability to move in cardinal directions by 1 space
The vacuum can see and remember the status of all of the spaces it can move

Functionality:
User or automatic starting location for vacuum
User or automatic generation of dirt in the area
User or automatic movement within the area
Visualization after every movement

Notes:
Included is a robust searching algorithm I made. It will find the most efficient path and follow it in a strip mining fashion
I have limited the system to not allow areas smaller than 2x2
"""


# This function creates lists that are used to track every position and the status of dirty or clean for each position.
def CreateList(ColumnAmount, RowAmount):
    PositionList = []
    # Create a variable that is = to the total amount of spaces
    T = ColumnAmount * RowAmount
    # Make the entire status list clean, we will amend it to include the dirty spots later
    StatusList = ["c" for i in range(T)]
    # Create the position list by iterating through the total amount of spaces
    while T != 0:
        PositionList.append(T)
        T = T - 1

    return PositionList, StatusList


# This function handles the changing of the AI's position
def Movement(MovementCommand, CurrentLocation, ColumnAmount, BottomRow):

    # Set the parameters in which the AI cannot move due to the artificial boundaries we have made
    if MovementCommand == "up" and CurrentLocation <= ColumnAmount:
        CurrentLocation = "Cannot move upwards"
        return CurrentLocation
    elif MovementCommand == "right" and CurrentLocation % ColumnAmount == 0:
        CurrentLocation = "Cannot move right"
        return CurrentLocation
    elif MovementCommand == "left" and CurrentLocation % ColumnAmount == 1:
        CurrentLocation = "Cannot move left"
        return CurrentLocation
    elif MovementCommand == "down" and CurrentLocation in BottomRow:
        CurrentLocation = "Cannot move downwards"
        return CurrentLocation
    # Interpret the movement command to move the AI's position
    if MovementCommand == "up":
        CurrentLocation = CurrentLocation - ColumnAmount
        return CurrentLocation
    if MovementCommand == "right":
        CurrentLocation = CurrentLocation + 1
        return CurrentLocation
    if MovementCommand == "left":
        CurrentLocation = CurrentLocation - 1
        return CurrentLocation
    if MovementCommand == "down":
        CurrentLocation = CurrentLocation + ColumnAmount
        return CurrentLocation


# This function allows the AI to cross reference the position and status lists so that it may react appropriately later
def CheckForDirt(CurrentLocation, ColumnAmount, RowAmount, PositionList, StatusList, DirtyList, CleanList, KnownList, BottomRow, LeftColumn):
    # Create variables that can act as booleans for whether directional movement is possible
    UpCheck = 0
    RightCheck = 0
    LeftCheck = 0
    DownCheck = 0

    # Check the sight boundaries in a similar fashion to the movement boundaries
    if CurrentLocation <= ColumnAmount:
        UpCheck = 1
    if CurrentLocation % ColumnAmount == 0:
        RightCheck = 1
    if CurrentLocation in LeftColumn:
        LeftCheck = 1
    if CurrentLocation in BottomRow:
        DownCheck = 1
    # Cross reference the status and position lists at the current position of the AI
    if KnownList[CurrentLocation - 1] == "?":
        G = PositionList.index(CurrentLocation)
        if StatusList[G] == "d":
            DirtyList.append(PositionList[G])
        elif StatusList[G] == "c":
            CleanList.append(PositionList[G])
    # Cross reference the status and position lists at the position above the AI
    if UpCheck == 0 and KnownList[(CurrentLocation - ColumnAmount) - 1] == "?":
        G = PositionList.index(CurrentLocation - ColumnAmount)
        if StatusList[G] == "d":
            DirtyList.append(PositionList[G])
        elif StatusList[G] == "c":
            CleanList.append(PositionList[G])
    # Cross reference the status and position lists at the position to the right of the AI
    if RightCheck == 0 and KnownList[(CurrentLocation + 1) - 1] == "?":
        G = PositionList.index(CurrentLocation + 1)
        if StatusList[G] == "d":
            DirtyList.append(PositionList[G])
        elif StatusList[G] == "c":
            CleanList.append(PositionList[G])
    # Cross reference the status and position lists at the position to the left of the AI
    if LeftCheck == 0 and KnownList[(CurrentLocation - 1) - 1] == "?":
        G = PositionList.index(CurrentLocation - 1)
        if StatusList[G] == "d":
            DirtyList.append(PositionList[G])
        elif StatusList[G] == "c":
            CleanList.append(PositionList[G])
    # Cross reference the status and position lists at the position below the AI
    if DownCheck == 0 and KnownList[(CurrentLocation + ColumnAmount) - 1] == "?":
        G = PositionList.index(CurrentLocation + ColumnAmount)
        if StatusList[G] == "d":
            DirtyList.append(PositionList[G])
        elif StatusList[G] == "c":
            CleanList.append(PositionList[G])

    return DirtyList, CleanList


# This function generates a random starting position for the AI
def AutoGenStartLocation(ColumnAmount, RowAmount):
    # The starting position can be anywhere within the space
    CurrentLocation = random.randrange(1, (ColumnAmount * RowAmount))
    CurrentLocation = int(CurrentLocation)
    return CurrentLocation


# This function generates a random amount of dirt and their positions
def AutoGenDirt(ColumnAmount, RowAmount, StatusList):
    # The amount of dirt is a random number between 0 and all the spaces
    DirtyAmount = random.randrange(0, (ColumnAmount * RowAmount))
    # Create an empty variable for filling in all the locations that are dirty
    DirtySpots = []
    # Create a variable that will randomly generate positions
    ToolVariable = 0
    # Create a loop that keeps attempting to create dirty spots until the desired amount is reached
    while len(DirtySpots) != DirtyAmount:
        ToolVariable = random.randrange(1, (ColumnAmount * RowAmount))
        # Repeat the loop if the randomly generated spot is already dirty
        if ToolVariable not in DirtySpots:
            DirtySpots.append(ToolVariable)

    # Amend the status list to include the dirty spots
    for i in DirtySpots:
        StatusList[(i - 1)] = "d"

    return StatusList


# This function creates a visual for users to track the AI/their progress
def MakeVisual(ColumnAmount, RowAmount, KnownList):
    w = 0
    z = ColumnAmount

    # Create a filler row to break up each row of the space
    FillerRow = "+"
    for i in range(ColumnAmount):
        FillerRow += "---+"
    # Create the initial filler row
    print(FillerRow)
    # Iterate through the list and print the rows in slices
    for i in range(RowAmount):
        FillableRows = "|"
        # Use slice tool to iterate through the list correctly
        for i in islice(KnownList, w, z):
            FillableRows += (" " + i + " |")
        print(FillableRows)
        print(FillerRow)
        w = w + ColumnAmount
        z = z + ColumnAmount
    print(FillerRow)

    return None


# This function will update the list of known locations for display purposes
def UpdateKnownList(KnownList, CurrentLocation, DirtyList, CleanList):
    # Set the dirty spots
    for i in DirtyList:
        KnownList[(i - 1)] = "d"

    # Set the clean spots
    for i in CleanList:
        KnownList[(i - 1)] = "c"

    # Set the location of the vacuum
    KnownList[CurrentLocation - 1] = "V"

    return KnownList


# This function will change any dirty spot to a clean spot
def CleanDirt(StatusList, CurrentLocation, CleanList, DirtyList):
    # Update each list to correspond to the new conditions
    StatusList[(CurrentLocation - 1)] = "c"
    CleanList.append(CurrentLocation)
    CleanList.sort()
    DirtyList.remove(CurrentLocation)

    return StatusList, CleanList, DirtyList


# This function will allow the user to set their own dirty spots
def SetDirtSpots(ColumnAmount, RowAmount, StatusList):
    # Create an x variable for various uses such as displaying an int
    x = ColumnAmount * RowAmount
    x = str(x)
    # Display the amount of spaces to the user
    print("There are " + x + " spaces")
    # Allow the user to decide the amount of dirt they want
    DirtyAmount = input("Enter the amount of spots of dirt you want: ")
    DirtyAmount = int(DirtyAmount)
    DirtySpots = []
    # Reuse the x variable alongside a y variable to create a list referencing the amount of rows and columns
    x = []
    y = []
    for i in range(1, (ColumnAmount + 1)):
        x.append(i)
    for i in range(1, (RowAmount + 1)):
        y.append(i)
    # Create a loop that will run for the amount of times needed to add all pieces of dirt
    for i in range(DirtyAmount):
        # Allow the user to specify the column of each piece of dirt
        DirtyCol = input("Enter the column coordinate of the spot of dirt: ")
        DirtyCol = int(DirtyCol)
        # Create a loop that error checks in case the user does not work within their boundaries
        while not (DirtyCol in x and DirtyCol > 0):
            print("That is not a valid column coordinate")
            DirtyCol = input("Enter the column coordinate of the spot of dirt: ")
            DirtyCol = int(DirtyCol)

        # Allow the user to specify the row of each piece of dirt
        DirtyRow = input("Enter the row coordinate of the spot of dirt: ")
        DirtyRow = int(DirtyRow)
        # Create a loop that error checks in case the user does not work within their boundaries
        while not (DirtyRow in y and DirtyCol > 0):
            print("That is not a valid row coordinate")
            DirtyRow = input("Enter the row coordinate of the spot of dirt: ")
            DirtyRow = int(DirtyRow)
        # Find the final location of each piece of dirt based on their column and row
        DirtySpots.append(DirtyCol * DirtyRow)
        print("Dirt added")

    # Add the dirt to the status list
    for i in DirtySpots:
        StatusList[(i - 1)] = "d"

    return StatusList


# This function allows the user to set their starting position
def SetStartSpot(ColumnAmount, RowAmount):
    # Use an x variable alongside a y variable to create a list referencing the amount of rows and columns
    x = []
    y = []
    for i in range(1, (ColumnAmount + 1)):
        x.append(i)
    for i in range(1, (RowAmount + 1)):
        y.append(i)

    # The user will enter the column of their starting position
    StartCol = input("Enter the column coordinate of the starting spot: ")
    StartCol = int(StartCol)
    # Create a loop that error checks in case the user does not work within their boundaries
    while not (StartCol in x):
        print("That is not a valid column coordinate")
        StartCol = input("Enter the column coordinate of the starting spot: ")
        StartCol = int(StartCol)

    # The user will enter the row of their starting position
    StartRow = input("Enter the row coordinate of the starting spot: ")
    StartRow = int(StartRow)
    # Create a loop that error checks in case the user does not work within their boundaries
    while not (StartRow in y):
        print("That is not a valid row coordinate")
        StartRow = input("Enter the row coordinate of the starting spot: ")
        StartRow = int(StartRow)

    # Find the final location of the starting location based on their column and row
    CurrentLocation = StartCol * StartRow
    CurrentLocation = int(CurrentLocation)

    return CurrentLocation


# This function finds the starting location of the search algorithm based on the dimensions of the area and where the starting position of the vacuum is
def AutoSetTargetSearchStart(ColumnAmount, RowAmount, CurrentLocation):
    VertCheck = "Blank"
    HorzCheck = "Blank"
    SearchPattern = "Blank"
    TargetSearchStart = 0

    # Find the nearest vertical and horizontal wall
    if CurrentLocation > ((ColumnAmount * RowAmount) / 2):
        VertCheck = "Bot"
    if CurrentLocation <= ((ColumnAmount * RowAmount) / 2):
        VertCheck = "Top"
    if (CurrentLocation % ColumnAmount) > (ColumnAmount / 2):
        HorzCheck = "Right"
    if (CurrentLocation % ColumnAmount) <= (ColumnAmount / 2):
        HorzCheck = "Left"

    # Create a series of conditionals that overwrite eachother in order of searching efficiency
    # These are based on the divisibility of the columns and rows of the area
    if ColumnAmount % 2 == 0:
        SearchPattern = "CE"
    if RowAmount % 2 > 0:
        SearchPattern = "RO"
    if ColumnAmount % 2 > 0:
        SearchPattern = "CO"
    if RowAmount % 3 == 0:
        SearchPattern = "R3"
    if ColumnAmount % 3 == 0:
        SearchPattern = "C3"

    # Generate the starting position based on the nearest walls and the best searching pattern
    # All the vertical search patterns can be grouped together
    if SearchPattern == "C3" or SearchPattern == "CO" or SearchPattern == "CE":
        if VertCheck == "Top" and HorzCheck == "Right":
            TargetSearchStart = ColumnAmount - 1
        if VertCheck == "Top" and HorzCheck == "Left":
            TargetSearchStart = 2
        if VertCheck == "Bot" and HorzCheck == "Right":
            TargetSearchStart = ((ColumnAmount * RowAmount) - 1)
        if VertCheck == "Bot" and HorzCheck == "Left":
            TargetSearchStart = ((ColumnAmount * RowAmount) - (ColumnAmount - 2))

    # All the horizontal search patterns can be grouped together
    if SearchPattern == "R3" or SearchPattern == "RO":
        if VertCheck == "Top" and HorzCheck == "Right":
            TargetSearchStart = (ColumnAmount * 2)
        if VertCheck == "Top" and HorzCheck == "Left":
            TargetSearchStart = (ColumnAmount + 1)
        if VertCheck == "Bot" and HorzCheck == "Right":
            TargetSearchStart = ((ColumnAmount * RowAmount) - ColumnAmount)
        if VertCheck == "Bot" and HorzCheck == "Left":
            TargetSearchStart = ((ColumnAmount * RowAmount) - ((ColumnAmount * 2) - 1))

    # Create a condition that will throw an error if a target spot cannot be found
    if TargetSearchStart == 0:
        print("ERROR")
        print(CurrentLocation)
        print(VertCheck)
        print(HorzCheck)
        print(SearchPattern)

    return SearchPattern, TargetSearchStart, VertCheck, HorzCheck


# This function will generate a movement command based on the current location and the target location
def AutoGenerateMoveCommand(ColumnAmount, CurrentLocation, TargetLocation, MovementCommand):
    # By using modulus we can create a system wherein the vacuums horizontal location can be determined in relation to the target location
    if CurrentLocation % ColumnAmount > TargetLocation % ColumnAmount and TargetLocation % ColumnAmount != 0 or (CurrentLocation % ColumnAmount == 0 and CurrentLocation % ColumnAmount < TargetLocation % ColumnAmount):
        MovementCommand = "left"
        return MovementCommand
    if CurrentLocation % ColumnAmount < TargetLocation % ColumnAmount or (CurrentLocation % ColumnAmount > TargetLocation % ColumnAmount and TargetLocation % ColumnAmount == 0):
        MovementCommand = "right"
        return MovementCommand
    if CurrentLocation > TargetLocation:
        MovementCommand = "up"
        return MovementCommand
    if CurrentLocation < TargetLocation:
        MovementCommand = "down"
        return MovementCommand


# This function will find the next location that the vacuum must reach
def AutoFindNextTargetLocation(CurrentLocation, DirtyList, TargetLocation, VertCheck, HorzCheck, ColumnAmount, RowAmount, SearchPattern, CleanList, KnownList, PositionList, MovementCommand, TopRow, BottomRow):

    # Create conditions that will set the vacuum back on its path after cleaning by checking if the nearby values have been seen
    # These variables will be filled with the known data of every direction of possible movement from the current location
    L = 0
    R = 0
    U = 0
    D = 0
    try:
        if not (CurrentLocation % ColumnAmount) == 1:
            L = KnownList[(CurrentLocation - 1) - 1]
    except:
        L = 0
    try:
        if not (CurrentLocation % ColumnAmount) == 0:
            R = KnownList[(CurrentLocation + 1) - 1]
    except:
        R = 0
    try:
        if not CurrentLocation in TopRow:
            U = KnownList[(CurrentLocation - ColumnAmount) - 1]
    except:
        U = 0
    try:
        if not CurrentLocation in BottomRow:
            D = KnownList[(CurrentLocation + ColumnAmount) - 1]
    except:
        D = 0

    # Check the last movement command and move in the opposite direction
    if L == "?" or R == "?" or U == "?" or D == "?":
        if MovementCommand == "left":
            TargetLocation = CurrentLocation + 1
            return TargetLocation, VertCheck, HorzCheck
        if MovementCommand == "right":
            TargetLocation = CurrentLocation - 1
            return TargetLocation, VertCheck, HorzCheck
        if MovementCommand == "down":
            TargetLocation = CurrentLocation - ColumnAmount
            return TargetLocation, VertCheck, HorzCheck
        if MovementCommand == "up":
            TargetLocation = CurrentLocation + ColumnAmount
            return TargetLocation, VertCheck, HorzCheck

    # Create a condition that will put the vacuum back on the path when it has reached a corner
    # These reference the two non corner directions and the previous movement command
    if CurrentLocation == 1 or CurrentLocation == ColumnAmount or CurrentLocation == (ColumnAmount * RowAmount) or CurrentLocation == ((ColumnAmount * RowAmount) - (ColumnAmount - 1)):
        if not (U == "?" and R == "?"):
            if MovementCommand == "left":
                TargetLocation = CurrentLocation + 1
                return TargetLocation, VertCheck, HorzCheck
            if MovementCommand == "down":
                TargetLocation = CurrentLocation - ColumnAmount
                return TargetLocation, VertCheck, HorzCheck
        if not (D == "?" and R == "?"):
            if MovementCommand == "left":
                 TargetLocation = CurrentLocation + 1
                 return TargetLocation, VertCheck, HorzCheck
            if MovementCommand == "up":
                 TargetLocation = CurrentLocation + ColumnAmount
                 return TargetLocation, VertCheck, HorzCheck
        if not (D == "?" and L == "?"):
            if MovementCommand == "right":
                TargetLocation = CurrentLocation - 1
                return TargetLocation, VertCheck, HorzCheck
            if MovementCommand == "up":
                TargetLocation = CurrentLocation + ColumnAmount
                return TargetLocation, VertCheck, HorzCheck
        if not (U == "?" and L == "?"):
            if MovementCommand == "right":
                TargetLocation = CurrentLocation - 1
                return TargetLocation, VertCheck, HorzCheck
            if MovementCommand == "down":
                TargetLocation = CurrentLocation - ColumnAmount
                return TargetLocation, VertCheck, HorzCheck

    # Check the dirty list
    if CurrentLocation == TargetLocation:
        try:
            TargetLocation = DirtyList[0]
            return TargetLocation, VertCheck, HorzCheck
        except:
            TargetLocation = "Empty"

    if TargetLocation == "Empty":
        # Vertical Based Search case
        if SearchPattern == "C3" or SearchPattern == "CO" or SearchPattern == "CE":
            # Reach top case
            if CurrentLocation in TopRow:
                # Track direction you are coming from
                VertCheck = "Top"
                # Switch column case
                if (CurrentLocation + ColumnAmount) in CleanList and (
                        (CurrentLocation + (ColumnAmount * 2)) in CleanList):
                    # Move in the opposite direction of the starting side
                    if HorzCheck == "Right" and (CurrentLocation - 2) >= 1 and KnownList[(CurrentLocation - 2) - 1] == "?":
                        if CurrentLocation - 3 in PositionList:
                            TargetLocation = CurrentLocation - 3
                            return TargetLocation, VertCheck, HorzCheck
                        else:
                            TargetLocation = CurrentLocation - 2
                            return TargetLocation, VertCheck, HorzCheck
                    # Move in the opposite direction of the starting side
                    if HorzCheck == "Left" and (CurrentLocation + 2) <= len(KnownList) and KnownList[
                        (CurrentLocation + 2) - 1] == "?":
                        if CurrentLocation + 3 in PositionList:
                            TargetLocation = CurrentLocation + 3
                            return TargetLocation, VertCheck, HorzCheck
                        else:
                            TargetLocation = CurrentLocation + 2
                            return TargetLocation, VertCheck, HorzCheck
            # Reach bottom case
            if CurrentLocation in BottomRow:
                # Track direction you are coming from
                VertCheck = "Bot"
                # Switch column case
                if (CurrentLocation - ColumnAmount) in CleanList and (
                        (CurrentLocation - (ColumnAmount * 2)) in CleanList):
                    # Move in the opposite direction of the starting side
                    if HorzCheck == "Right" and (CurrentLocation - 2) >= 1 and KnownList[(CurrentLocation - 2) - 1] == "?":
                        if CurrentLocation - 3 in PositionList:
                            TargetLocation = CurrentLocation - 3
                            return TargetLocation, VertCheck, HorzCheck
                        else:
                            TargetLocation = CurrentLocation - 2
                            return TargetLocation, VertCheck, HorzCheck
                    # Move in the opposite direction of the starting side
                    if HorzCheck == "Left" and (CurrentLocation + 2) <= len(KnownList) and KnownList[
                        (CurrentLocation + 2) - 1] == "?":
                        if CurrentLocation + 3 in PositionList:
                            TargetLocation = CurrentLocation + 3
                            return TargetLocation, VertCheck, HorzCheck
                        else:
                            TargetLocation = CurrentLocation + 2
                            return TargetLocation, VertCheck, HorzCheck
            # Move along vertical path if not at boundary
            if VertCheck == "Top":
                TargetLocation = CurrentLocation + ColumnAmount
                return TargetLocation, VertCheck, HorzCheck
            # Move along vertical path if not at boundary
            if VertCheck == "Bot":
                TargetLocation = CurrentLocation - ColumnAmount
                return TargetLocation, VertCheck, HorzCheck
        # Horizontal Based Search case
        if SearchPattern == "R3" or SearchPattern == "RO":
            # Reach right boundary case
            if CurrentLocation % ColumnAmount == 0:
                # Track direction you are coming from
                HorzCheck = "Right"
                # Switch row case
                if (CurrentLocation - 1) in CleanList and (CurrentLocation - 2) in CleanList:
                    # Move in the opposite direction of the starting side
                    if VertCheck == "Top" and (CurrentLocation + (ColumnAmount * 2)) <= len(KnownList) and KnownList[(CurrentLocation + (ColumnAmount * 2)) - 1] == "?":
                        if (CurrentLocation + (ColumnAmount * 3)) in PositionList:
                            TargetLocation = CurrentLocation + (ColumnAmount * 3)
                            return TargetLocation, VertCheck, HorzCheck
                        else:
                            TargetLocation = CurrentLocation + (ColumnAmount * 2)
                            return TargetLocation, VertCheck, HorzCheck
                    # Move in the opposite direction of the starting side
                    if VertCheck == "Bot" and (CurrentLocation - (ColumnAmount * 2)) >= 1 and KnownList[
                        (CurrentLocation - (ColumnAmount * 2)) - 1] == "?":
                        if (CurrentLocation - (ColumnAmount * 3)) in PositionList:
                            TargetLocation = CurrentLocation - (ColumnAmount * 3)
                            return TargetLocation, VertCheck, HorzCheck
                        else:
                            TargetLocation = CurrentLocation - (ColumnAmount * 2)
                            return TargetLocation, VertCheck, HorzCheck
            # Reach left boundary case
            if CurrentLocation % ColumnAmount == 1:
                # Track direction you are coming from
                HorzCheck = "Left"
                # Switch row case
                if (CurrentLocation + 1) in CleanList and (CurrentLocation + 2) in CleanList:
                    # Move in the opposite direction of the starting side
                    if VertCheck == "Top":
                        if (CurrentLocation + (ColumnAmount * 3)) in PositionList:
                            TargetLocation = CurrentLocation + (ColumnAmount * 3)
                            return TargetLocation, VertCheck, HorzCheck
                        else:
                            TargetLocation = CurrentLocation + (ColumnAmount * 2)
                            return TargetLocation, VertCheck, HorzCheck
                    # Move in the opposite direction of the starting side
                    if VertCheck == "Bot":
                        if (CurrentLocation - (ColumnAmount * 3)) in PositionList:
                            TargetLocation = CurrentLocation - (ColumnAmount * 3)
                            return TargetLocation, VertCheck, HorzCheck
                        else:
                            TargetLocation = CurrentLocation - (ColumnAmount * 2)
                            return TargetLocation, VertCheck, HorzCheck
            # Move along horizontal path if not at boundary
            if HorzCheck == "Left":
                TargetLocation = CurrentLocation + 1
                return TargetLocation, VertCheck, HorzCheck
            # Move along horizontal path if not at boundary
            if HorzCheck == "Right":
                TargetLocation = CurrentLocation - 1
                return TargetLocation, VertCheck, HorzCheck


def main():
    # Create a bunch of variables to be filled later
    MovementCommand = ""
    CurrentLocation = 0
    ColumnAmount = 0
    RowAmount = 0
    DirtyList = []
    CleanList = []
    AutoMove = "x"
    AutoStart = "x"
    AutoDirt = "x"

    # Print a welcome message because we have manners
    print("Welcome")
    # Ask for the dimensions of the area and loop if an acceptable answer is not given
    print("Please enter the amount of columns there are in the area; ")
    ColumnAmount = input()
    try:
        ColumnAmount = int(ColumnAmount)
    except:
        pass
    while isinstance(ColumnAmount, int) == False or ColumnAmount <= 1:
        print("That is not a valid input")
        print("Please enter the amount of columns there are in the area; ")
        ColumnAmount = input()
        try:
            ColumnAmount = int(ColumnAmount)
        except:
            pass

    print("Please enter the amount of rows there are in the area; ")
    RowAmount = input()
    try:
        RowAmount = int(RowAmount)
    except:
        pass
    while isinstance(RowAmount, int) == False or RowAmount <= 1:
        print("That is not a valid input")
        print("Please enter the amount of rows there are in the area; ")
        RowAmount = input()
        try:
            RowAmount = int(RowAmount)
        except:
            pass

    # Generate three lists for tracking pertinent data
    # PositionList contains all the spots in the area and is numbered starting from 1
    # StatusList directly correlates with PositionList but contains d or c in every spot for clean or dirty
    # KnownList tracks what has been detected by the vacuum
    PositionList, StatusList = CreateList(ColumnAmount, RowAmount)
    KnownList = ["?" for i in range(ColumnAmount * RowAmount)]
    TopRow = []
    BottomRow = []
    LeftColumn = [1]
    RightColumn = [ColumnAmount]
    for i in range(1, (ColumnAmount + 1)):
        TopRow.append(i)
    for i in range(((ColumnAmount * (RowAmount - 1)) + 1), ((ColumnAmount * RowAmount) + 1)):
        BottomRow.append(i)
    for i in range(1, RowAmount):
        LeftColumn.append(((ColumnAmount * i) + 1))
    for i in range(1, RowAmount):
        RightColumn.append(((ColumnAmount * i) + ColumnAmount))

    # Ask if the user wants to automatically or manually have the dirty spots set into the area
    AutoDirt = input("Would you like to enter the dirty spots manually or automatically? Enter A or M; ")
    while not (AutoDirt.upper() == "A" or AutoDirt.upper() == "M"):
        print("That is not a valid input")
        AutoDirt = input("Would you like to enter the dirty spots manually or automatically? Enter A or M; ")
        AutoDirt.upper()

    # Based on the choice of automatic or manual, generate the dirty spots
    if AutoDirt == "A":
        StatusList = AutoGenDirt(ColumnAmount, RowAmount, StatusList)
    if AutoDirt == "M":
        StatusList = SetDirtSpots(ColumnAmount, RowAmount, StatusList)

    # Ask if the user wants to automatically or manually choose the starting spot of the vacuum
    AutoStart = input("Would you like to enter the starting position manually or automatically? Enter A or M; ")
    while not (AutoStart.upper() == "A" or AutoStart.upper() == "M"):
        print("That is not a valid input")
        AutoStart = input("Would you like to enter the starting position manually or automatically? Enter A or M; ")

    # Based on the choice of automatic or manual, generate the starting spot of the vacuum
    if AutoStart == "A":
        CurrentLocation = AutoGenStartLocation(ColumnAmount, RowAmount)
    if AutoStart == "M":
        CurrentLocation = SetStartSpot(ColumnAmount, RowAmount)

    # Ask if the user wants to automatically or manually clean the area
    AutoMove = input("Would you like to clean manually or automatically? Enter A or M; ")
    while not (AutoMove.upper() == "A" or AutoMove.upper() == "M"):
        print("That is not a valid input")
        AutoMove = input("Would you like to clean manually or automatically? Enter A or M; ")

    # Initialize all the data for manual users and display the starting board
    if AutoMove == "M":
        StatusList, CleanList, DirtyList = CleanDirt(StatusList, CurrentLocation, CleanList, DirtyList)
        DirtyList, CleanList = CheckForDirt(CurrentLocation, ColumnAmount, RowAmount, PositionList, StatusList, DirtyList, CleanList, BottomRow, LeftColumn)
        KnownList = UpdateKnownList(KnownList, CurrentLocation, DirtyList, CleanList)
    MakeVisual(ColumnAmount, RowAmount, KnownList)

    # Create a loop for the user to keep using the program till its end
    while AutoMove == "M" and len(CleanList) != len(PositionList):
        # Create variables for tracking if the user wants to clean or check for dirt
        CleanTracker = "blank"
        CleanAsk = "blank"

        # Ask the user for a movement command
        MovementCommand = input("Please make a movement choice (up, left, right, down); ")
        while MovementCommand != "up" or MovementCommand != "left" or MovementCommand != "right" or MovementCommand != "down":
            print("That is not a valid input")
            MovementCommand = input("Please make a movement choice (up, left, right, down); ")

        # Move the user based on the previous command
        CurrentLocation = Movement(MovementCommand, CurrentLocation, ColumnAmount, BottomRow)
        # If the movement is not valid error check the user
        while CurrentLocation != type(int):
            print("That is not a valid movement input")
            MovementCommand = input("Please make a movement choice (up, left, right, down); ")
            CurrentLocation = Movement(MovementCommand, CurrentLocation, ColumnAmount, BottomRow)

        # Ask the user if they wish to check the current area
        CleankAsk = input("Would you like to search the area? (Y/N): ")
        while not (CleankAsk == "Y" or CleankAsk == "N"):
            print("That is not a valid input")
            CleankAsk = input("Would you like to search the area? (Y/N); ")

        # Check the area if the user wishes
        if CleanAsk == "Y":
            DirtyList, CleanList = CheckForDirt(CurrentLocation, ColumnAmount, RowAmount, PositionList, StatusList, DirtyList, CleanList, BottomRow, LeftColumn)
            KnownList = UpdateKnownList(KnownList, CurrentLocation, DirtyList, CleanList)
            MakeVisual(ColumnAmount, RowAmount, KnownList)
            print("Here is the updated map")

        # Ask if the user wants to clean the current spot
        CleanTracker = input("Would you like to clean the current spot? (Y/N); ")
        while CleanTracker != "Y" or CleanTracker != "N":
            print("That is not a valid input")
            CleanTracker = input("Would you like to clean the current spot? (y/n); ")

        # Clean the spot if the user wishes
        if CleanTracker == "Y":
            StatusList, CleanList, DirtyList = CleanDirt(StatusList, CurrentLocation, CleanList, DirtyList)

        # Visualize the area
        MakeVisual(ColumnAmount, RowAmount, KnownList)
        print("Here is the updated map")

    # Create trackers to see the amount of steps taken to reach the end goal
    StepsToTargetStart = 0
    StepsAfterSearchStart = 0
    AmountOfCleans = 0
    AmountOfSearches = 0

    # If the user wishes for the AI to take over you must find the starting location of the search
    if AutoMove == "A":
        SearchPattern, TargetSearchStart, VertCheck, HorzCheck = AutoSetTargetSearchStart(ColumnAmount, RowAmount, CurrentLocation)
        TargetLocation = TargetSearchStart

        # Loop movement until the vacuum has reached its target starting location
        while CurrentLocation != TargetLocation:
            StepsToTargetStart = StepsToTargetStart + 1
            MovementCommand = AutoGenerateMoveCommand(ColumnAmount, CurrentLocation, TargetLocation, MovementCommand)
            CurrentLocation = Movement(MovementCommand, CurrentLocation, ColumnAmount, BottomRow)
            MakeVisual(ColumnAmount, RowAmount, KnownList)
        print("We are now at the start of the search")

    # Loop the searching algorithm until every spot has been viewed
    while AutoMove == "A" and len(CleanList) != len(PositionList):
        # Loop movement to target locations
        while not (CurrentLocation == TargetLocation):
            StepsAfterSearchStart = StepsAfterSearchStart + 1
            MovementCommand = AutoGenerateMoveCommand(ColumnAmount, CurrentLocation, TargetLocation, MovementCommand)
            CurrentLocation = Movement(MovementCommand, CurrentLocation, ColumnAmount, BottomRow)
            MakeVisual(ColumnAmount, RowAmount, KnownList)
        # Scan areas when moving along desired path
        if CurrentLocation not in DirtyList:
            print("Starting scan")
            DirtyList, CleanList = CheckForDirt(CurrentLocation, ColumnAmount, RowAmount, PositionList, StatusList, DirtyList, CleanList, KnownList, BottomRow, LeftColumn)
            KnownList = UpdateKnownList(KnownList, CurrentLocation, DirtyList, CleanList)
            MakeVisual(ColumnAmount, RowAmount, KnownList)
            print("Scan done")
        # Clean any dirty spots
        if CurrentLocation in DirtyList:
            AmountOfCleans = AmountOfCleans + 1
            StatusList, CleanList, DirtyList = CleanDirt(StatusList, CurrentLocation, CleanList, DirtyList)
        # Find the next target location
        TargetLocation, VertCheck, HorzCheck = AutoFindNextTargetLocation(CurrentLocation, DirtyList, TargetLocation, VertCheck, HorzCheck, ColumnAmount, RowAmount, SearchPattern, CleanList, KnownList, PositionList, MovementCommand,  TopRow, BottomRow)
        AmountOfSearches = AmountOfSearches + 1

    # Create a final visualization
    MakeVisual(ColumnAmount, RowAmount, KnownList)
    if AutoMove == "A":
        print("The amount of steps taken to get to the starting position; " + str(StepsToTargetStart))
        print("The amount of steps taken while searching; " + str(StepsAfterSearchStart))
        print("The amount of cleanings; " + str(AmountOfCleans))
        print("The amount of searches; " + str(AmountOfSearches))
    print("You are done")


main()
