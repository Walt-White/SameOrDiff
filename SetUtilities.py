def generateCardDeck():
    # Create tuples for characteristics that don't change:
    traits = ('number', 'shape', 'fill', 'color')
    numbers = ('One', 'Two', 'Three')
    shapes = ('Diamond', 'Oval', 'Squiggle')
    fills = ('Empty', 'Lines', 'Solid')
    colors = ('Black', 'Blue', 'Orange')

    cardDeck = []
    card = []
    cardFilename = ''

    for number in numbers:
        numberCard = card.copy()
        numberCard.append(numbers.index(number) + 1)
        numberCardFilename = cardFilename
        numberCardFilename += number
        for shape in shapes:
            shapeCard = numberCard.copy()
            shapeCard.append(shapes.index(shape) + 1)
            shapeCardFilename = numberCardFilename
            shapeCardFilename += shape
            for fill in fills:
                fillCard = shapeCard.copy()
                fillCard.append(fills.index(fill) + 1)
                fillCardFilename = shapeCardFilename
                fillCardFilename += fill
                for color in colors:
                    colorCard = fillCard.copy()
                    colorCard.append(colors.index(color) + 1)
                    colorCardFilename = fillCardFilename + color + ".svg"
                    colorCard.append(colorCardFilename)
                    cardDeck.append(colorCard)
    return cardDeck

def generateTrainingDeck():
    # Create tuples for characteristics that don't change:
    traits = ('number', 'shape', 'fill', 'color')
    numbers = ('One', 'Two', 'Three', 'Four')
    shapes = ('Diamond', 'Oval', 'Squiggle', 'Star')
    fills = ('Empty', 'Lines', 'Solid', 'Splat')
    colors = ('Black', 'Blue', 'Orange', 'White')

    cardDeck = []
    card = []
    cardFilename = ''

    for number in numbers:
        numberCard = card.copy()
        numberCard.append(numbers.index(number) + 1)
        numberCardFilename = cardFilename
        numberCardFilename += number
        for shape in shapes:
            shapeCard = numberCard.copy()
            shapeCard.append(shapes.index(shape) + 1)
            shapeCardFilename = numberCardFilename
            shapeCardFilename += shape
            for fill in fills:
                fillCard = shapeCard.copy()
                fillCard.append(fills.index(fill) + 1)
                fillCardFilename = shapeCardFilename
                fillCardFilename += fill
                for color in colors:
                    colorCard = fillCard.copy()
                    colorCard.append(colors.index(color) + 1)
                    colorCardFilename = fillCardFilename + color + ".svg"
                    colorCard.append(colorCardFilename)
                    cardDeck.append(colorCard)
    return cardDeck

def testForSet (cardDeck, card1, card2, card3):
    # Success using 3, 68, 49 and using 37, 78, 5
    trioOfCards = [cardDeck[card1], cardDeck[card2], cardDeck[card3]]
    testNumber = 0
    testShape = 0
    testFill = 0
    testColor = 0
    response = ""
    for card in trioOfCards:
        testNumber += card[0]
        testShape += card[1]
        testFill += card[2]
        testColor += card[3]
    if testNumber % 3 != 0:
        response += "number"
    if testShape % 3 != 0:
        if len(response) != 0:
            response += ", shape"
        else:
            response += "shape"
    if testFill % 3 != 0:
        if len(response) != 0:
            response += ", fill"
        else:
            response += "fill"
    if testColor % 3 != 0:
        if len(response) != 0:
            response += ", color"
        else:
            response += "color"

    if response == "":
        response = "<p class=\"scrunch\">Great!  You found a group.</p>"
        return response
    else:
        response = "<p class=\"scrunch\">Oops!  Problem with " + response + ".</p>"
        return response

def printFoundSets (cardDeck, foundSets, cardFolder):      #  added cardFolder
    page = ""
    for set in foundSets:
        page += "\n<table border=\"1\">\n\t<tr>"
        for card in set:
            if cardFolder == "ColoredShapes":
                page += "\n\t\t<td><img width=\"65\" src=\"static\\CardImages\\ColoredShapes\\" + cardDeck[card][4] + "\"></td>"
            else:
                page += "\n\t\t<td><img width=\"65\" src=\"static\\CardImages\\BlackShapes\\" + cardDeck[card][4] + "\"></td>"
        page += "\n\t</tr>\n</table>\n"
    return page

def int32toInt (listOfLists):
    tempResult = []
    for list in listOfLists:
        temp = []
        for i in list:
            temp.append(int(i))
        tempResult.append(temp)
    return tempResult

# HTML to print basic user page will be used for training pages:
def printTrainingHeader() :
    page = ""
    page += "<!DOCTYPE html>\n<html lang=\"en-US\">\n<head>\n"
    page += "\t<title>Same Or Different Exercise</title>\n\t<meta charset=\"utf-8\" />\n"
    page += "\t<link type=\"text/css\" rel=\"stylesheet\" href=\"./static/SameOrDifferent.css\">\n"
    page += "\t<link rel=\"icon\" href=\"/static/FCB-1.ico\" type=\"image/x-icon\">\n</head>\n<body class=\"training\">"
    page += "<center><h2>Same Or Different Training Exercise</h2></center>\n"
    page += "<form action=\"ExerciseEval\" method=\"post\">\n\n<center>"
    return page

def printTrainingOneHeader() :
    page = ""
    page += "<!DOCTYPE html>\n<html lang=\"en-US\">\n<head>\n"
    page += "\t<title>Same Or Different Exercise</title>\n\t<meta charset=\"utf-8\" />\n"
    page += "\t<link type=\"text/css\" rel=\"stylesheet\" href=\"./static/SameOrDifferent.css\">\n"
    page += "\t<link rel=\"icon\" href=\"/static/FCB-1.ico\" type=\"image/x-icon\">\n</head>\n<body class=\"training\">"
    page += "<center><h2>Same Or Different Training Exercise</h2></center>\n"
    page += "<form action=\"ExerciseEvalOne\" method=\"post\">\n\n<center>"
    return page

def printTrainingFooter(submitValue) :
    page = ""
    page += "<input type=\"submit\" value=\" + submitValue + \">\n</form>\n</center>\n</body>\n</html>"
#    page += "<input type=\"submit\" value=submitValue>\n</form>\n</center>\n</body>\n</html>"
    return page

# HTML presenting user choices.  New training game will print all.  They are separate because when
# a user choice (number, shape, fill, color) is successful, then that choice will not be presented on subsequent pages.
def printNumberChoices() :
    page = ""
    page += '\n<table>\n\t<tr>\n\t\t<td>\n\t\t\t<center><img width=\"175\" src=\"static/UtilityImages/TrainingThree.png\"><br />\n'
    page += "\t\t\t<input type=\"radio\" name=\"Number\" value=\"3\">3</center>\n\t\t</td>\n"
    page += "\t\t<td>\n\t\t\t&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\n\t\t</td>\n"
    page += "\t\t<td>\n\t\t\t<center><img width=\"117\" src=\"static/UtilityImages/TrainingTwo.png\"><br />\n"
    page += "\t\t\t<input type=\"radio\" name=\"Number\" value=\"2\">2</center>\n\t\t</td>\n"
    page += "\t\t<td>\n\t\t\t&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>\n"
    page += "\t\t<td>\n\t\t\t<center><img width=\"58\" src=\"static/UtilityImages/TrainingOne.png\"><br />\n"
    page += "\t\t\t<input type=\"radio\" name=\"Number\" value=\"1\">1</center>\n\t\t</td>\n\t</tr>\n"
    page += "\t<caption><h3>Number</h3></caption>\n</table>\n<br /><br />\n"
    return page

def printColorChoices() :
    page = ""
    page += '\n<table>\n\t<tr>\n\t\t<td>\n\t\t\t<center><img width=\"55\" src=\"static/UtilityImages/TrainingBlue.png\"><br />\n'
    page += "\t\t\t<input type=\"radio\" name=\"Color\" value=\"2\">Blue</center>\n\t\t</td>\n"
    page += "\t\t<td>\n\t\t\t<center><img width=\"55\" src=\"static/UtilityImages/TrainingGray.png\"><br />\n"
    page += "\t\t\t<input type=\"radio\" name=\"Color\" value=\"1\">Gray</center>\n\t\t</td>\n"
    page += "\t\t<td>\n\t\t\t<center><img width=\"55\" src=\"static/UtilityImages/TrainingOrange.png\"><br />\n"
    page += "\t\t\t<input type=\"radio\" name=\"Color\" value=\"3\">Orange</center>\n\t\t</td>\n\t</tr>\n"
    page += "\t<caption><h3>Color</h3></caption>\n</table>\n<br /><br />\n"
    return page

def printFillChoices() :
    page = ""
    page += '\n<table>\n\t<tr>\n\t\t<td>\n\t\t\t<center><img width=\"55\" src=\"static/UtilityImages/TrainingEmpty.png\"><br />\n'
    page += "\t\t\t<input type=\"radio\" name=\"Fill\" value=\"1\">Empty</center>\n\t\t</td>\n"
    page += "\t\t<td>&nbsp;&nbsp;&nbsp;&nbsp;\n\t\t</td>\n"
    page += "\t\t<td>\n\t\t\t<center><img width=\"55\" src=\"static/UtilityImages/TrainingSolid.png\"><br />\n"
    page += "\t\t\t<input type=\"radio\" name=\"Fill\" value=\"3\">Solid</center>\n\t\t</td>\n"
    page += "\t\t<td>\n\t\t\t&nbsp;&nbsp;&nbsp;&nbsp;\n\t\t</td>\n"
    page += "\t\t<td>\n\t\t\t<center><img width=\"55\" src=\"static/UtilityImages/TrainingLines.png\"><br />\n"
    page += "\t\t\t<input type=\"radio\" name=\"Fill\" value=\"2\">Lines</center>\n\t\t</td>\n\t</tr>\n"
    page += "\t<caption><h3>Fill</h3></caption>\n</table>\n<br /><br />\n"
    return page

def printShapeChoices() :
    page = ""
    page += '\n<table>\n\t<tr>\n\t\t<td>\n\t\t\t<center><img width=\"55\" src=\"static/UtilityImages/TrainingSquiggle.png\"><br />\n'
    page += "\t\t\t<input type=\"radio\" name=\"Shape\" value=\"3\">Squiggle</center>\n\t\t</td>\n"
    page += "\t\t<td>\n\t\t\t&nbsp;&nbsp;&nbsp;&nbsp;\n\t\t</td>\n"
    page += "\t\t<td>\n\t\t\t<center><img width=\"55\" src=\"static/UtilityImages/TrainingOval.png\"><br />\n"
    page += "\t\t\t<input type=\"radio\" name=\"Shape\" value=\"2\">Oval</center>\n\t\t</td>\n"
    page += "\t\t<td>\n\t\t\t&nbsp;&nbsp;&nbsp;&nbsp;\n\t\t</td>\n"
    page += "\t\t<td>\n\t\t\t<center><img width=\"55\" src=\"static/UtilityImages/TrainingDiamond.png\"><br />\n"
    page += "\t\t\t<input type=\"radio\" name=\"Shape\" value=\"1\">Diamond</center>\n\t\t</td>\n\t</tr>\n"
    page += "\t<caption><h3>Shape</h3></caption>\n</table>\n<br /><br />\n"
    return page

# def getCardIndex() :
#     goalNumber = request.get_cookie("goalNumber")
#     return index