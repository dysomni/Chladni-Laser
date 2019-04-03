import src.variables as v
import graphics as g

win = g.GraphWin("Update Values", 500, 500, autoflush=False)

def update():
    s = len(v.gui_displayed)
    r = []
    for i in range(s):
        for ii in range(s):
            r.append(Rectangle(Point(50 + ((400 / s) * ii), 50 + ((400 / s) * i)),
                               Point(50 + ((400 / s) * (ii + 1)), 50 + ((400 / s) * (i + 1)))))
    index = 0
    for i in r:
        i.setOutline("black")
        i.setWidth(2)
        if v.gui_displayed[index] is 0:
            i.setFill("white")
        if v.gui_displayed[index] is 1:
            i.setFill("red")
        i.draw(win)
    g.show()

    return

# will wait till there is a click within a square created by two points
def waitTillClick(p1, p2):
    click = g.Point(501,501)
    while (click.getX() < p1.getX() or click.getX() > p2.getX()) and (click.getY() < p1.getY() or click.getY() > p2.getY()):
        click = win.getMouse()

# will wait till a clikc is within a certain square and will then return which box it used
# parameters: boxes - array of boxes (two points) that represent the different places to click
# returns: the index of the box (two points) where the mouse was clicked
def waitTillClickSections(boxes):
    click = win.getMouse()
    out = False
    while True:
        index = 0
        for b in boxes:
            if click.getX() >= b.getP1().getX() and click.getX() <= b.getP2().getX() and click.getY() >= b.getP1().getY() and click.getY() <= b.getP2().getY():
                return index
            index += 1
        click = win.getMouse()

# will wait till a click is placed anywhere
def waitTillAnyClick():
    win.getMouse()
    return

