import ast
from bottle import default_app, route, run, template, static_file, request, response
import numpy as np
import os
import itertools
from SetUtilities import *

# Two lines below are executed when the pythonanywhere.com web app is restarted on the pythonanywhere
# web account control page.
cardDeck = generateCardDeck()
trainingCardDeck = generateTrainingDeck()

# The 'static/images' paragraph below is not used on PythonAnywhere which maps 'static' files 
# as a configuration item.
if os.path.isfile('OnlyOnVisualStudio.txt'):
    @route('/static/CardImages/BlackShapes/<filename>')
    def send_image(filename):
        cardPath = 'C:\\Users\\Walt\\OneDrive\\Documents\\Programming\\Python\\SameOrDifferent\\static\\CardImages\\BlackShapes\\'
        return static_file(filename, root=cardPath)

    @route('/static/CardImages/ColoredShapes/<filename>')
    def send_image(filename):
        cardPath = 'C:\\Users\\Walt\\OneDrive\\Documents\\Programming\\Python\\SameOrDifferent\\static\\CardImages\\ColoredShapes\\'
        return static_file(filename, root=cardPath)

    @route('/static/UtilityImages/<filename>')
    def send_image(filename):
        cardPath = 'C:\\Users\\Walt\\OneDrive\\Documents\\Programming\\Python\\SameOrDifferent\\static\\UtilityImages\\'
        return static_file(filename, root=cardPath)

    @route('/static/<filename>')
    def send_file(filename):
        return static_file(filename, root='C:\\Users\\Walt\\OneDrive\\Documents\\Programming\\Python\\SameOrDifferent\\static\\')

# The line below is required for PythonAnywhere and doesn't seem to interfere 
# with the Visual Studio localhost operation.
application = default_app()

# Write all the HTML stuff used to define the non-training page.  Training page is different.
pageHTML = "<!DOCTYPE html>\n<html lang=\"en-US\">\n<head>\n\t<title>Same Or Different</title>\n"
pageHTML += "\t<meta charset=\"utf-8\" />\n"
pageHTML += "\t<link type=\"text/css\" rel=\"stylesheet\" href=\"/static/SameOrDifferent.css\">\n"
pageHTML += "\t<link rel=\"icon\" href=\"/static/FCB-1.ico\" type=\"image/x-icon\">\n</head>\n<body>\n"
pageHTML += "\t<div class=\"column\">\n\t\t<div class=\"column tableau\">\n"
pageHTML += "\t\t\t<iframe src=\"/twelve\" name=\"twelve\" style=\"border:none\" width=\"100%\" height=\"600px\"></iframe>\n\t\t</div>\n"
pageHTML += "\t\t<div class=\"column results\">\n"
pageHTML += "\t\t\t<iframe src=\"/results\" name=\"Results\" style=\"border:none\" width=\"100%\" height=\"480px\"></iframe>\n"
pageHTML += "\t\t\t<hr>\n"
pageHTML += "\t\t\t<iframe src=\"/hints\" name=\"Hints\" style=\"border:none\" width=\"100%\" height=\"90px\"></iframe>\n"
pageHTML += "\t\t</div>\n\t</div>\n</body>\n"
pageHTML += "</center>\n</html>"

@route('/', method="get")
def SetPage():
    if request.get_cookie("cardFolder"):
        cardFolder = request.get_cookie("cardFolder")
    else:
        response.set_cookie("cardFolder", "ColoredShapes")
    response.set_cookie("numberOfHints", "0")
    response.set_cookie("numberOfSets", "0")
    response.set_cookie("foundSets", "[]")
    response.set_cookie("confirmedSets", "[]")
    return pageHTML

@route('/', method="post")
def SetPage():
    if request.get_cookie("cardFolder") == "ColoredShapes" :
        cardFolder = "BlackShapes"
        response.set_cookie("cardFolder", "BlackShapes")
    else:
        cardFolder = "ColoredShapes"
        response.set_cookie("cardFolder", "ColoredShapes")
    response.set_cookie("numberOfHints", "0")
    response.set_cookie("numberOfSets", "0")
    response.set_cookie("foundSets", "[]")
    response.set_cookie("confirmedSets", "[]")
    return pageHTML

@route('/hints', method="get")
def hints():
    page = "<!DOCTYPE html>\n<html lang=\"en-US\">\n<head>\n"
    page += "\t<link type=\"text/css\" rel=\"stylesheet\" href=\"/static/SameOrDifferent.css\">\n</head>\n<body>\n<center>\n"
    page += "<form action=\"/hints\" method=\"post\" target=\"Hints\">\n"
    page += "\t<input value=\"<=== Hints\" type=\"submit\"/>\n</form>\n"
    page += "</body>\n</center>\n</html>"
    return page

@route('/hints', method="post")
def hints():
    cardFolder = request.get_cookie("cardFolder")
    page = "<!DOCTYPE html>\n<html lang=\"en-US\">\n<head>\n"
    page += "\t<link type=\"text/css\" rel=\"stylesheet\" href=\"/static/SameOrDifferent.css\">\n</head>\n<body>\n<center>\n"
    page += "<form action=\"/hints\" method=\"post\" target=\"Hints\">\n"
    page += "<input value=\"<=== Hints\" type=\"submit\"/>"
    page += "</form>\n"

    numberOfHints = int(request.get_cookie("numberOfHints"))
    numberOfHints +=1
    foundSets = []
    foundSets = ast.literal_eval(request.get_cookie("foundSets"))
    confirmedSets = []
    confirmedSets = ast.literal_eval(request.get_cookie("confirmedSets"))

    for confirmedSet in confirmedSets:
        if confirmedSet not in foundSets:
            count = 0
            page += "\n<table border=\"1\">\n\t<tr>"
            for card in confirmedSet:
                if count < numberOfHints:
                    if cardFolder == "ColoredShapes":
                        page += "\n\t\t<td><img width=\"65\" src=\"static\\CardImages\\ColoredShapes\\" + cardDeck[card][4] + "\">"
                    else:
                        page += "\n\t\t<td><img width=\"65\" src=\"static\\CardImages\\BlackShapes\\" + cardDeck[card][4] + "\">"
                    count += 1
                else:
                    break
            break   # Only show one confirmed not-found set, not every confirmed not-found set.
    response.set_cookie("numberOfHints", str(numberOfHints))
    page += "\n\t</tr>\n</table>\n"
    page += "</body>\n</center></html>"
    return page

@route('/results', method="get")
def results():
    page = "<!DOCTYPE html>\n<html lang=\"en-US\">\n<head>\n"
    page += "\t<link type=\"text/css\" rel=\"stylesheet\" href=\"/static/SameOrDifferent.css\">\n</head>\n<body><center>\n"
    page += "<h3>Results</h3>"
    page += "</center>\n</body>\n</html>"
    return page

@route('/results', method="post")
def results():
    numberOfSets = request.get_cookie("numberOfSets")
    foundSets = []
    foundSets = ast.literal_eval(request.get_cookie("foundSets"))
    cardFolder = request.get_cookie("cardFolder")
    page = "<!DOCTYPE html>\n<html lang=\"en-US\">\n<head>\n"
    page += "\t<link type=\"text/css\" rel=\"stylesheet\" href=\"/static/SameOrDifferent.css\">\n</head>\n<body><center>\n"
    page += "<h3>Results</h3>"
    page += "<p class=\"scrunch\">There are <b>" + numberOfSets + "</b> groups.</p>\n"

    cardsSent = []
    for card in request.forms.getall('cardNumber'):
        cardsSent.append(int(card))
    cardsSent.sort()
    if len(cardsSent) != 3:
        page += "<p class=\"scrunch\"><b>Ouch!</b> Please click exactly <b>three</b> cards.</p>"
        page += printFoundSets (cardDeck, foundSets, cardFolder)

        return page
    page += testForSet(cardDeck, int(cardsSent[0]), int(cardsSent[1]), int(cardsSent[2]))
    if 'Great' in testForSet(cardDeck, int(cardsSent[0]), int(cardsSent[1]), int(cardsSent[2])):
        response.set_cookie("numberOfHints", "0")
        if cardsSent not in foundSets:
            foundSets.append(cardsSent)
            response.set_cookie("foundSets", str(foundSets))
        else:
            page += "<p class=\"scrunch\"><b>Duplicate of a group you already found.</b></p>"
    page += printFoundSets (cardDeck, foundSets, cardFolder)
    page += "</center>\n</body>\n</html>"

    return page

@route('/twelve', classmethod="get")
def twelve():
    cardFolder = request.get_cookie("cardFolder")
    foundSets = []
    response.set_cookie("foundSets", str(foundSets))
    twelveCards = np.random.choice(list(range(80)), 12, replace=False)
    print("\nThe twelve cards are =")
    print(twelveCards)
    candidates = itertools.combinations(sorted(twelveCards),3)
    confirmedSets = []
    for candidate in candidates:
        if 'Great' in testForSet(cardDeck, candidate[0], candidate[1], candidate[2]):
            confirmedSets.append(candidate)
    confirmedSets = int32toInt(confirmedSets)
    print("\nThe confirmed groups are =")
    print(confirmedSets)
    print("\n")
    response.set_cookie("confirmedSets", str(confirmedSets))
    numberOfSets = len(confirmedSets)
    response.set_cookie("numberOfSets", str(numberOfSets))

    page = "<!DOCTYPE html><html lang=\"en-US\">\n<head>\n"
    page += "\t<link type=\"text/css\" rel=\"stylesheet\" href=\"/static/SameOrDifferent.css\">\n"
    page += "</head>\n<body>\n<center>\n"
    page += "<h2>Same Or Different</h2>"
    page += "<center>\n<form action=\"/results\" method=\"post\" target=\"Results\">\n"
    page += "\t<table border=\"1\">\n"
    counter = 0
    for j in range(3):
        page += "\t\t<tr>\n\t\t\t"
        for i in range(4):
            if cardFolder == "ColoredShapes":
                page += "<td align=\"center\"><img width=\"175\" src=\"static\\CardImages\\ColoredShapes\\" + cardDeck[twelveCards[counter]][4] + "\">"
            else:
                page += "<td align=\"center\"><img width=\"175\" src=\"static\\CardImages\\BlackShapes\\" + cardDeck[twelveCards[counter]][4] + "\">"
            page += "<br />\n\t\t\t<input type=\"checkbox\" name=\"cardNumber\" value=\"" + str(twelveCards[counter]) + "\">"
            page += "</td>"
            if i == 3:
                page += "\n"
            else:
                page += "\n\t\t\t"
            counter += 1
        page += "\t\t</tr>\n"
    page += "\t</table>\n"
    page += "<p>There are <b>" + str(numberOfSets) + "</b> groups above.\n"
    page += "<input value=\"Test ====>\" type=\"submit\" /></p>\n"
    page += "</form>\n</center>\n"

    if os.path.isfile('OnlyOnVisualStudio.txt'):
        page += "<p class=\"leftAlign\"><a href=\"http://localhost:8888\" target=\"_top\">New Game</a></p>\n"
    else:
        page += "<p class=\"leftAlign\"><a href=\"http://firstcoolbreeze.pythonanywhere.com\" target=\"_top\">New Game</a></p>\n"
    page += "<form action=\"/\" method=\"post\" target=\"_top\">\n"
    page += "<p class=\"leftAlign\"><input value=\"Use Other Color Scheme\" type=\"submit\" /></p>\n"
    page += "</form>"
    page += "</body>\n</html>"
    return page

@route('/training', classmethod="get")  # First visit to training or "new game" from within training page.
def training():
    # Choose two random cards to evaluate.  Need to use "generateCardDeck" as source because all those are
    # valid cards.  The "generateTrainingDeck" has all the cards corresponding to non-specified choices.  
    twoCards = np.random.choice(list(range(80)), 2, replace=False)
    print("\nThe two cards are =")  # this output is to the VS Code console for debugging.
    print(twoCards)   # this output is to the VS Code console for debugging.
    # Set cookies to keep track of the two cards being evaluated for the Training exercise.
    response.set_cookie("trainingCardOne", str(twoCards[0]))
    response.set_cookie("trainingCardTwo", str(twoCards[1]))
    # Set cookies for the value of the four traits in the goal card.  Starts with "4" for all.
    response.set_cookie("goalNumber", str(4))
    response.set_cookie("goalShape", str(4))
    response.set_cookie("goalFill", str(4))
    response.set_cookie("goalColor", str(4))
    
    # Use trait values to calculate card index number.  Same idea will be used after every successful user choice.
    # Subtract 1 from each of the values, concatenate into single number, convert from base 4 to base 10.
    indexNumber = 64 * (4 - 1)
    indexNumber += 16 * (4 - 1)
    indexNumber += 4 * (4 - 1)
    indexNumber += 1 * (4 - 1)
    page = ''
    page += printTrainingHeader()
    page += printNumberChoices()
    page += "<table class=\"noBorder\"\n\t<tr>\n"
    page += "\t\t<td>\n\t\t\t<img width=\"275\" src=\"static\\CardImages\\BlackShapes\\" + cardDeck[twoCards[0]][4] + "\">\n"
    page += "\t\t</td>\n"
    page += "\t\t<td>\n\t\t\t<img width=\"275\" src=\"static\\CardImages\\BlackShapes\\" + trainingCardDeck[indexNumber][4] + "\"></td>\n"
    page += "\t\t<td>\n\t\t\t<img width=\"275\" src=\"static\\CardImages\\BlackShapes\\" + cardDeck[twoCards[1]][4] + "\">\n"
    page += "\t\t</td>\n\t</tr>\n</table>\n<br /><br />\n"
    # For the "get" condition, print a table containing three tables
    page += "<table class=\"noBorder\">\n\t<tr>\n\t\t<td>\n\t\t\t"
    page += printColorChoices()
    page += "\n\t\t</td>\n\t\t<td>\n\t\t\t&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\n"
    page += "\t\t</td>\n\t\t<td>\n\t\t\t"
    page += printFillChoices()
    page += "\n\t\t</td>\n\t\t<td>\n\t\t\t&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\n"
    page += "\t\t\t<td>\n\t\t\t\t"
    page += printShapeChoices()
    page += "\n\t\t</td>\n\t</tr>\n</table>\n"
    page += "<input type=\"submit\" value=\"Test\">\n</form>\n"
    if os.path.isfile('OnlyOnVisualStudio.txt'):
        page += "<p class=\"error\"><a href=\"http://localhost:8888/training\" target=\"_top\">New Exercise</a></p>\n"
    else:
        page += "<p class=\"error\"><a href=\"http://firstcoolbreeze.pythonanywhere.com/training\" target=\"_top\">New Exercise</a></p>\n"
    page += "</center>\n</body>\n</html>"
    return page

@route('/trainingOne', classmethod="get")  # First visit to training or "new game" from within training page.
def trainingOne():
    # Choose two random cards to evaluate.  Need to use "generateCardDeck" as source because all those are
    # valid cards.  The "generateTrainingDeck" has all the cards corresponding to non-specified choices.  
    twoCards = np.random.choice(list(range(80)), 2, replace=False)
    print("\nThe two cards are =")  # this output is to the VS Code console for debugging.
    print(twoCards)   # this output is to the VS Code console for debugging.
    # Set cookies to keep track of the two cards being evaluated for the Training exercise.
    response.set_cookie("trainingCardOne", str(twoCards[0]))
    response.set_cookie("trainingCardTwo", str(twoCards[1]))
    # Set cookies for the value of the four traits in the goal card.  Starts with "4" for all.
    response.set_cookie("goalNumber", str(4))
    response.set_cookie("goalShape", str(4))
    response.set_cookie("goalFill", str(4))
    response.set_cookie("goalColor", str(4))
    
    # Use trait values to calculate card index number.  Same idea will be used after every successful user choice.
    # Subtract 1 from each of the values, concatenate into single number, convert from base 4 to base 10.
    indexNumber = 64 * (4 - 1)
    indexNumber += 16 * (4 - 1)
    indexNumber += 4 * (4 - 1)
    indexNumber += 1 * (4 - 1)
    page = ''
    page += printTrainingHeader()
    page += "<table class=\"noBorder\"\n\t<tr>\n"
    page += "\t\t<td>\n\t\t\t<img width=\"275\" src=\"static\\CardImages\\BlackShapes\\" + cardDeck[twoCards[0]][4] + "\">\n"
    page += "\t\t</td>\n"
    page += "\t\t<td>\n\t\t\t<img width=\"275\" src=\"static\\CardImages\\BlackShapes\\" + trainingCardDeck[indexNumber][4] + "\"></td>\n"
    page += "\t\t<td>\n\t\t\t<img width=\"275\" src=\"static\\CardImages\\BlackShapes\\" + cardDeck[twoCards[1]][4] + "\">\n"
    page += "\t\t</td>\n\t</tr>\n</table>\n<br /><br />\n"
    page += printNumberChoices()
    page += "<input type=\"submit\" value=\"Test\">\n</form>\n"
    if os.path.isfile('OnlyOnVisualStudio.txt'):
        page += "<p class=\"error\"><a href=\"http://localhost:8888/trainingOne\" target=\"_top\">New Exercise</a></p>\n"
    else:
        page += "<p class=\"error\"><a href=\"http://firstcoolbreeze.pythonanywhere.com/trainingOne\" target=\"_top\">New Exercise</a></p>\n"
    page += "</center>\n</body>\n</html>"

    return page


@route('/ExerciseEval', method="post")  # Testing some choices from the Exercise training page.
def ExerciseEval():
    # First task is to recreate the same two cards being tested as we rewrite the whole page.
    theCards = [int(request.get_cookie("trainingCardOne")), int(request.get_cookie("trainingCardTwo"))]
    # Then use trait values to generate progress from previous choices in the center goal card.
    goalNumber = int(request.get_cookie("goalNumber"))
    goalShape = int(request.get_cookie("goalShape"))
    goalFill = int(request.get_cookie("goalFill"))
    goalColor = int(request.get_cookie("goalColor"))
    errorResponse = ""
    displayNumberAgain = True
    displayShapeAgain = True
    displayFillAgain = True
    displayColorAgain = True
    page = ""
    page += printTrainingHeader()
    # Start evaluating user choices.  Could be anything from none to four values incoming.
    # For each choice, evaluate it.  If it is correct, don't display that choice table again, but
    # do update the corresponding cookie value to match, and update the goal card displayed to match.  If the
    # choice is incorrect, display that choice table and update an error message.
    # Check to see if Number has already been successfully reset from the default value of 4.
    if request.get_cookie('goalNumber') == str(4) : 
        if request.forms.get('Number') :
            # Evaluate by using modulo on that trait for all three cards.  
            testNumber = int(request.forms.get('Number')) + cardDeck[theCards[0]][0] + cardDeck[theCards[1]][0]
            if testNumber % 3 != 0:  # User choice is wrong.  
                errorResponse += "Problem with Number. "
                # Since the user got it wrong, display the Number choices again.
                displayNumberAgain = True
            else :  # User choice is right.  Modify trait for goal card.  
                goalNumber = int(request.forms.get('Number'))
                displayNumberAgain = False
                response.set_cookie('goalNumber', request.forms.get('Number'))
        else :  # There was no choice for Number so display the Number table.  
            displayNumberAgain = True
    else :
        displayNumberAgain = False

    if request.get_cookie('goalShape') == str(4) : 
        if request.forms.get('Shape') :
            # Evaluate by using modulo on that trait for all three cards.  
            testShape = int(request.forms.get('Shape')) + cardDeck[theCards[0]][1] + cardDeck[theCards[1]][1]
            if testShape % 3 != 0:  # User choice is wrong.  
                errorResponse += "Problem with Shape. "
                # Since the user got it wrong, display the Number choices again.
                displayShapeAgain = True
            else :  # User choice is right.  Modify trait for goal card.  
                goalShape = int(request.forms.get('Shape'))
                displayShapeAgain = False
                response.set_cookie('goalShape', request.forms.get('Shape'))
        else :  # There was no choice for Shape so display the Shape table.  
            displayShapeAgain = True
    else :
        displayShapeAgain = False

    if request.get_cookie('goalFill') == str(4) : 
        if request.forms.get('Fill') :
            # Evaluate by using modulo on that trait for all three cards.  
            testFill = int(request.forms.get('Fill')) + cardDeck[theCards[0]][2] + cardDeck[theCards[1]][2]
            if testFill % 3 != 0:  # User choice is wrong.  
                errorResponse += "Problem with Fill. "
                # Since the user got it wrong, display the Number choices again.
                displayFillAgain = True
            else :  # User choice is right.  Modify trait for goal card.  
                goalFill = int(request.forms.get('Fill'))
                displayFillAgain = False
                response.set_cookie('goalFill', request.forms.get('Fill'))
        else :  # There was no choice for Fill so display the Fill table.  
            displayFillAgain = True
    else :
        displayFillAgain = False

    if request.get_cookie('goalColor') == str(4) : 
        if request.forms.get('Color') :
            # Evaluate by using modulo on that trait for all three cards.  
            testColor = int(request.forms.get('Color')) + cardDeck[theCards[0]][3] + cardDeck[theCards[1]][3]
            if testColor % 3 != 0:  # User choice is wrong.  
                errorResponse += "Problem with Color. "
                # Since the user got it wrong, display the Color choices again.
                displayColorAgain = True
            else :  # User choice is right.  Modify trait for goal card.  
                goalColor = int(request.forms.get('Color'))
                displayColorAgain = False
                response.set_cookie('goalColor', request.forms.get('Color'))
        else :  # There was no choice for Color so display the Color table.  
            displayColorAgain = True
    else :
        displayColorAgain = False

    # Start the display.  
    if displayNumberAgain == True :
        page += printNumberChoices()

    # Display the two source cards and the current progress on the goal card.  
    indexNumber = 64 * (goalNumber - 1)
    indexNumber += 16 * (goalShape - 1)
    indexNumber += 4 * (goalFill - 1)
    indexNumber += 1 * (goalColor - 1)
    page += "<table class=\"noBorder\"\n\t<tr>\n"
    page += "\t\t<td>\n\t\t\t<img width=\"275\" src=\"static\\CardImages\\BlackShapes\\" + cardDeck[theCards[0]][4] + "\">\n"
    page += "\t\t</td>\n"
    page += "\t\t<td>\n\t\t\t<img width=\"275\" src=\"static\\CardImages\\BlackShapes\\" + trainingCardDeck[indexNumber][4] + "\">\n\t\t</td>\n"
    page += "\t\t<td>\n\t\t\t<img width=\"275\" src=\"static\\CardImages\\BlackShapes\\" + cardDeck[theCards[1]][4] + "\">\n"
    page += "\t\t</td>\n\t</tr>\n</table>\n<br /><br />\n"

    # Display the three other trait choices only if necessary.  Three tables in one overall table.
    page += "<table class=\"noBorder\">\n\t<tr>\n\t\t<td>\n\t\t\t"
    if displayColorAgain == True :
         page += printColorChoices()
    page += "\n\t\t</td>\n\t\t<td>\n\t\t\t&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\n"
    page += "\t\t</td>\n\t\t<td>\n\t\t\t"
    if displayFillAgain == True :
        page += printFillChoices()
    page += "\n\t\t</td>\n\t\t<td>\n\t\t\t&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\n"
    page += "\t\t\t<td>\n\t\t\t\t"
    if displayShapeAgain == True :
        page += printShapeChoices()
    page += "\n\t\t</td>\n\t</tr>\n</table>\n"

    # Display error messages if necessary.
    if errorResponse != "" :
        page += "<p class=\"error\">" + errorResponse + "</p>"

    # Display the submit button if necessary. If done, display "new game"
#    if displayNumberAgain == False :
    if (((displayNumberAgain == False and displayColorAgain == False) and displayFillAgain == False)) and displayShapeAgain == False :
        page += "<p class=\"error\">Success!</p>\n"
        if os.path.isfile('OnlyOnVisualStudio.txt'):
            page += "<p class=\"error\"><a href=\"http://localhost:8888/training\" target=\"_top\">New Exercise</a></p>\n"
        else:
            page += "<p class=\"error\"><a href=\"http://firstcoolbreeze.pythonanywhere.com/training\" target=\"_top\">New Exercise</a></p>\n"
    else :
        page += "<input type=\"submit\" value=\"Test\">\n"
    page += "</form>\n</center>\n</body>\n</html>"
    return page

@route('/ExerciseEvalOne', method="post")  # Testing some choices from the Exercise training page.
def ExerciseEvalOne():
    # First task is to recreate the same two cards being tested as we rewrite the whole page.
    theCards = [int(request.get_cookie("trainingCardOne")), int(request.get_cookie("trainingCardTwo"))]
    # Then use trait values to generate progress from previous choices in the center goal card.
    goalNumber = int(request.get_cookie("goalNumber"))
    goalShape = int(request.get_cookie("goalShape"))
    goalFill = int(request.get_cookie("goalFill"))
    goalColor = int(request.get_cookie("goalColor"))
    errorResponse = ""
    displayNumberAgain = True
    displayShapeAgain = True
    displayFillAgain = True
    displayColorAgain = True
    page = ""
    page += printTrainingHeader()

# The line below is required for Visual Studio Code localhost operation, and makes PythonAnywhere fail!
if os.path.isfile('OnlyOnVisualStudio.txt'):
    run(host='localhost', port=8888, debug=True)

