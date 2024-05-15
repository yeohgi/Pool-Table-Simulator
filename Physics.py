import phylib
import sqlite3
import os

HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="700" height="1375" viewBox="-25 -25 1400 2750"
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink">
<rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />"""
FOOTER = """</svg>\n"""

################################################################################
# import constants from phylib to global varaibles
BALL_RADIUS = phylib.PHYLIB_BALL_RADIUS
BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER
HOLE_RADIUS = phylib.PHYLIB_HOLE_RADIUS
TABLE_LENGTH = phylib.PHYLIB_TABLE_LENGTH
TABLE_WIDTH = phylib.PHYLIB_TABLE_WIDTH
SIM_RATE = phylib.PHYLIB_SIM_RATE
VEL_EPSILON = phylib.PHYLIB_VEL_EPSILON
DRAG = phylib.PHYLIB_DRAG
MAX_TIME = phylib.PHYLIB_MAX_TIME
MAX_OBJECTS = phylib.PHYLIB_MAX_OBJECTS
FRAME_INTERVAL = 0.02 #0.01
# add more here

################################################################################
# the standard colours of pool balls
# if you are curious check this out:  
# https://billiards.colostate.edu/faq/ball/colors/

BALL_COLOURS = [ 
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",             # no LIGHTRED
    "MEDIUMPURPLE",     # no LIGHTPURPLE
    "LIGHTSALMON",      # no LIGHTORANGE
    "LIGHTGREEN",
    "SANDYBROWN",       # no LIGHTBROWN 
    ]

################################################################################
class Coordinate( phylib.phylib_coord ):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass


################################################################################
class StillBall( phylib.phylib_object ):
    """
    Python StillBall class.
    """

    def __init__( self, number, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_STILL_BALL, 
                                       number, 
                                       pos, None, None, 
                                       0.0, 0.0 )
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = StillBall


    # add an svg method here
    def svg( self ):
        return """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" %(self.obj.still_ball.pos.x, self.obj.still_ball.pos.y,  BALL_RADIUS, BALL_COLOURS[self.obj.still_ball.number])

################################################################################
class RollingBall( phylib.phylib_object ):
    """
    Python RollingBall class.
    """

    def __init__( self, number, pos, vel, acc):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_ROLLING_BALL, 
                                       number, 
                                       pos, vel, acc, 
                                       0.0, 0.0 )

        # this converts the phylib_object into a StillBall class
        self.__class__ = RollingBall


    # add an svg method here
    def svg( self ):
        return """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" %(self.obj.rolling_ball.pos.x, self.obj.rolling_ball.pos.y,  BALL_RADIUS, BALL_COLOURS[self.obj.still_ball.number])

################################################################################
class Hole( phylib.phylib_object ):
    """
    Python Hole class.
    """

    def __init__( self, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HOLE, 
                                       None, 
                                       pos, None, None, 
                                       0.0, 0.0 )

        # this converts the phylib_object into a StillBall class
        self.__class__ = Hole


    # add an svg method here
    def svg( self ):
       return """ <circle cx="%d" cy="%d" r="%d" fill="black" />\n""" %(self.obj.hole.pos.x, self.obj.hole.pos.y, HOLE_RADIUS)

################################################################################
class HCushion( phylib.phylib_object ):
    """
    Python HCushion class.
    """

    def __init__( self, y ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HCUSHION, 
                                       None, 
                                       None, None, None, 
                                       0.0, y)

        # this converts the phylib_object into a StillBall class
        self.__class__ = HCushion


    # add an svg method here
    def svg( self ):
        if(self.obj.hcushion.y == 0):
            return """ <rect width="1400" height="25" x="-25" y="%d" fill="darkgreen" />\n""" %-25
        else:
            return """ <rect width="1400" height="25" x="-25" y="%d" fill="darkgreen" />\n""" %(2700)

################################################################################
class VCushion( phylib.phylib_object ):
    """
    Python VCushion class.
    """

    def __init__( self, x ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_VCUSHION, 
                                       None, 
                                       None, None, None, 
                                       x , 0.0 )

        # this converts the phylib_object into a StillBall class
        self.__class__ = VCushion


    # add an svg method here
    def svg( self ):
        if(self.obj.vcushion.x == 0):
            return """ <rect width="25" height="2750" x="%d" y="-25" fill="darkgreen" />\n""" %-25
        else:
            return """ <rect width="25" height="2750" x="%d" y="-25" fill="darkgreen" />\n""" %(1350)

################################################################################
class Table( phylib.phylib_table ):
    """
    Pool table class.
    """

    def __init__( self ):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__( self )
        self.current = -1

    def __iadd__( self, other ):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object( other )
        return self

    def __iter__( self ):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        return self

    def __next__( self ):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1  # increment the index to the next object
        if self.current < MAX_OBJECTS:   # check if there are no more objects
            return self[ self.current ] # return the latest object

        # if we get there then we have gone through all the objects
        self.current = -1    # reset the index counter
        raise StopIteration  # raise StopIteration to tell for loop to stop

    def __getitem__( self, index ):
        """
        This method adds item retreivel support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object( index ) 
        if result==None:
            return None
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion
        return result

    def __str__( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = ""    # create empty string
        result += "time = %6.1f\n" % self.time    # append time
        for i,obj in enumerate(self): # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i,obj)  # append object description
        return result  # return the string

    def segment( self ):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """

        result = phylib.phylib_table.segment( self )
        if result:
            result.__class__ = Table
            result.current = -1
        return result

    # add svg method here
    def svg( self ):

        svg = HEADER

        for item in self:

            if(item is not None):

                svg += str(item.svg())

        svg += FOOTER

        return svg
    
    def cueBall( self ):

        for item in self:

            if(item is not None):

                if item.type == phylib.PHYLIB_STILL_BALL and item.obj.still_ball.number == 0:
                    self.current = -1
                    return item
                    
        self.current = -1
        return None
    
    def roll( self, t ):
        new = Table()
        for ball in self:
            if isinstance( ball, RollingBall ):
                # create4 a new ball with the same number as the old ball
                new_ball = RollingBall( ball.obj.rolling_ball.number,
                                        Coordinate(0,0),
                                        Coordinate(0,0),
                                        Coordinate(0,0) )
                # compute where it rolls to
                phylib.phylib_roll( new_ball, ball, t )
                # add ball to table
                new += new_ball
            if isinstance( ball, StillBall ):
                # create a new ball with the same number and pos as the old ball
                new_ball = StillBall( ball.obj.still_ball.number,
                                    Coordinate( ball.obj.still_ball.pos.x,
                                    ball.obj.still_ball.pos.y ) )
                # add ball to table
                new += new_ball
            # return table
        return new
    
    def newTable(self):
        for ball in self:
            if isinstance( ball, RollingBall ) or isinstance( ball, StillBall ):
                self.remove(ball)
        self.current = -1

        count = 1
        for i in range(0,5):
            # print(525 + i * 37.5, 525 + i * 75)
            for j in range(5 - i,0, -1):
                pos = Coordinate((525 + i * 37.5) + 75 * (5-j-i), (525 + i * 60))
                if count == 11:
                    sb = StillBall(8, pos)
                elif count == 8:
                    sb = StillBall(11, pos)
                else:
                    sb = StillBall(count, pos)
                count += 1
                count = count % 16
                self += sb

        pos = Coordinate(675, 2025)
        sb = StillBall(0, pos)
        self += sb

        




class Database():

    conn = None

    def __init__(self, reset=False):

        if(reset is True):
            if(os.path.exists('phylib.db')):
                os.remove('phylib.db')
            # print("Reset Database")

        self.conn = sqlite3.connect('phylib.db')

    def createDB(self):

        if(self.conn is None):
            self.conn = sqlite3.connect('phylib.db')
        cursor = self.conn.cursor()

        cursor.execute('''SELECT name FROM sqlite_master''')

        tables = cursor.fetchall()
        
        if(('Ball',) not in tables):
            cursor.execute('''CREATE TABLE Ball(
                            BALLID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            BALLNO INTEGER,
                            XPOS FLOAT,
                            YPOS FLOAT,
                            XVEL FLOAT,
                            YVEL FLOAT
            );''')

        if(('TTable',) not in tables):
            cursor.execute('''CREATE TABLE TTable(
                            TABLEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            TIME FLOAT
            );''')

        if(('BallTable',) not in tables):
            cursor.execute('''CREATE TABLE BallTable(
                        BALLID INTEGER,
                        TABLEID INTEGER,
                        FOREIGN KEY(BALLID) REFERENCES Ball,
                        FOREIGN KEY(TABLEID) REFERENCES TTable
            );''')

        if(('Shot',) not in tables):
            cursor.execute('''CREATE TABLE Shot(
                        SHOTID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        PLAYERID INTEGER,
                        GAMEID INTEGER,
                        FOREIGN KEY(PLAYERID) REFERENCES Player,
                        FOREIGN KEY(GAMEID) REFERENCES Game
            );''')

        if(('TableShot',) not in tables):
            cursor.execute('''CREATE TABLE TableShot(
                        TABLEID INTEGER,
                        SHOTID INTEGER,
                        FOREIGN KEY(TABLEID) REFERENCES TTable,
                        FOREIGN KEY(SHOTID) REFERENCES Shot
            );''')

        if(('Game',) not in tables):
            cursor.execute('''CREATE TABLE Game(
                        GAMEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        GAMENAME VARCHAR(64)
            );''')

        if(('Player',) not in tables):
            cursor.execute('''CREATE TABLE Player(
                        PLAYERID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        GAMEID INTEGER,
                        PLAYERNAME VARCHAR(64),
                        FOREIGN KEY(GAMEID) REFERENCES Game
            );''')

        cursor.close()
        self.conn.commit()

    def readTable( self, tableID ):

        if(self.conn is None):
            self.conn = sqlite3.connect('phylib.db')
        cursor = self.conn.cursor()

        table = Table()

        readCommand = f"SELECT * FROM Ball, BallTable WHERE Ball.BALLID = BallTable.BALLID AND BallTable.TABLEID = {tableID + 1}"
        cursor.execute(readCommand)
        balls = cursor.fetchall()

        readCommand = f"SELECT TIME FROM TTable WHERE TTable.TABLEID = {tableID + 1}"
        cursor.execute(readCommand)

        times = cursor.fetchone()

        if(times is None):
            return None

        time = times[0]

        table.time = time * FRAME_INTERVAL
            
        for ball in balls:

            if(ball[4] == 0 and ball[5] == 0):

                ballNum = ball[1]
                x = ball[2]
                y = ball[3]

                table += StillBall(ballNum, Coordinate(x,y))
            
            else:

                ballNum = ball[1]
                x = ball[2]
                y = ball[3]
                xv = ball[4]
                yv = ball[5]

                if(phylib.phylib_length(Coordinate(xv,yv)) > VEL_EPSILON):
                    xacc = -xv / phylib.phylib_length(Coordinate(xv,yv)) * DRAG
                    yacc = -yv / phylib.phylib_length(Coordinate(xv,yv)) * DRAG
                else:
                    xacc = 0
                    yacc = 0

                table += RollingBall(ballNum, Coordinate(x,y), Coordinate(xv,yv), Coordinate(xacc,yacc))

        #comment when done
        with open("table-" + str(tableID) + ".svg", "w") as fptr:
            fptr.write(table.svg())
        return table

    def writeTable( self, table ):

        if(self.conn is None):
            self.conn = sqlite3.connect('phylib.db')
        cursor = self.conn.cursor()

        time = float(table.time)

        insertTTableCommand = f"""INSERT INTO TTable (TIME) VALUES({time})"""
        cursor.execute(insertTTableCommand)

        insertTTableCommand = f"""SELECT MAX(TABLEID) FROM TTable"""
        cursor.execute(insertTTableCommand)
        tid = cursor.fetchone()[0]

        for object in table:

            if object is not None and object.type == phylib.PHYLIB_STILL_BALL:

                number = object.obj.still_ball.number

                x = object.obj.still_ball.pos.x

                y = object.obj.still_ball.pos.y
            
                insertStillBallCommand = f"""INSERT INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL) VALUES({number}, {x}, {y}, 0, 0)"""
                cursor.execute(insertStillBallCommand)

                insertStillBallCommand = f"""SELECT MAX(BALLID) FROM Ball"""
                cursor.execute(insertStillBallCommand)
                bid = cursor.fetchone()[0]

                insertBallTableCommand = f"""INSERT INTO BallTable (BALLID, TABLEID) VALUES({bid}, {tid})"""
                cursor.execute(insertBallTableCommand)

            if object is not None and object.type == phylib.PHYLIB_ROLLING_BALL:

                number = object.obj.rolling_ball.number

                x = object.obj.rolling_ball.pos.x

                y = object.obj.rolling_ball.pos.y

                xv = object.obj.rolling_ball.vel.x

                yv = object.obj.rolling_ball.vel.y
            
                insertStillBallCommand = f"""INSERT INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL) VALUES({number}, {x}, {y}, {xv}, {yv})"""
                cursor.execute(insertStillBallCommand)

                insertStillBallCommand = f"""SELECT MAX(BALLID) FROM Ball"""
                cursor.execute(insertStillBallCommand)
                bid = cursor.fetchone()[0]

                insertBallTableCommand = f"""INSERT INTO BallTable VALUES({bid}, {tid})"""
                cursor.execute(insertBallTableCommand)

        table.current = -1
        self.conn.commit()
        return tid

    def getGame(self, gameID):

        if(self.conn is None):
            self.conn = sqlite3.connect('phylib.db')
        cursor = self.conn.cursor()

        readCommand = f"SELECT Game.GAMENAME, Player.PLAYERNAME FROM Game, Player WHERE Game.GAMEID == {gameID} and Player.GAMEID == {gameID}"
        cursor.execute(readCommand)
        rows = cursor.fetchall()

        return rows

    def setGame(self, gameName, player1Name, player2Name):

        if(self.conn is None):
            self.conn = sqlite3.connect('phylib.db')
        cursor = self.conn.cursor()

        insertGameCommand = f"""INSERT INTO Game (GAMENAME) VALUES('{gameName}')"""
        cursor.execute(insertGameCommand)

        insertGameCommand = f"""SELECT MAX(GAMEID) FROM Game"""
        cursor.execute(insertGameCommand)
        gid = cursor.fetchone()[0]

        insertGameCommand = f"""INSERT INTO Player (GAMEID, PLAYERNAME) VALUES({gid}, '{player1Name}')"""
        cursor.execute(insertGameCommand)

        insertGameCommand = f"""INSERT INTO Player (GAMEID, PLAYERNAME) VALUES({gid}, '{player2Name}')"""
        cursor.execute(insertGameCommand)

        self.conn.commit()

    def newShot(self, gameID, playerID):

        if(self.conn is None):
            self.conn = sqlite3.connect('phylib.db')
        cursor = self.conn.cursor()

        insertShotCommand = f"""INSERT INTO Shot (PLAYERID, GAMEID) VALUES({playerID}, {gameID})"""
        cursor.execute(insertShotCommand)

        selectShotCommand = f"""SELECT MAX(SHOTID) FROM Shot"""
        cursor.execute(selectShotCommand)
        sid = cursor.fetchone()[0]

        self.conn.commit()

        return sid
    
    def close(self):
        self.conn.commit()
        self.conn.close()

    #comment
    integerman = 1
class Game():

    gameID = None
    gameName = None
    player1Name = None
    player2Name = None

    def __init__( self, gameID=None, gameName=None, player1Name=None, player2Name=None ):

        self.gameID = gameID
        self.gameName = gameName
        self.player1Name = player1Name
        self.player2Name = player2Name

        if(gameID is not None):

            gameID += 1

            db = Database()

            db.getGame(gameID)

            self.gameName = gameName
            self.player1Name = player1Name
            self.player2Name = player2Name

        elif (gameName is not None and player1Name is not None and player2Name is not None):

            print("creating game with no id")

            db = Database()

            if(db.conn is None):
                db.conn = sqlite3.connect('phylib.db')
            cursor = db.conn.cursor()

            db.setGame(gameName, player1Name, player2Name)

            selectGameCommand = f"""SELECT MAX(GAMEID) FROM Game"""
            cursor.execute(selectGameCommand)
            gid = cursor.fetchone()[0]

            self.gameID = gid

        else:
            raise TypeError

    def shoot( self, gameName, playerName, table, xvel, yvel ):

        db = Database()

        if(db.conn is None):
            db.conn = sqlite3.connect('phylib.db')
        cursor = db.conn.cursor()

        # print(self.gameID)
        # print(playerName)

        selectPlayerCommand = f"""SELECT Player.PLAYERID FROM Player WHERE Player.GAMEID = {self.gameID} AND Player.PLAYERNAME = '{playerName}'"""
        cursor.execute(selectPlayerCommand)
        pid = cursor.fetchone()[0]

        # for row in pid:
        #     print(row)

        sid = db.newShot(self.gameID, pid)

        ball = table.cueBall()

        xpos = ball.obj.still_ball.pos.x
        ypos = ball.obj.still_ball.pos.y

        ball.type = phylib.PHYLIB_ROLLING_BALL

        ball.obj.rolling_ball.number = 0
        ball.obj.rolling_ball.pos.x = xpos
        ball.obj.rolling_ball.pos.y = ypos
        ball.obj.rolling_ball.vel.x = xvel
        ball.obj.rolling_ball.vel.y = yvel

        vel = Coordinate(xvel, yvel)

        if(phylib.phylib_length(vel) > VEL_EPSILON):
            xacc = -xvel / phylib.phylib_length(vel) * DRAG
            yacc = -yvel / phylib.phylib_length(vel) * DRAG
        else:
            xacc = 0
            yacc = 0

        ball.obj.rolling_ball.acc.x = xacc
        ball.obj.rolling_ball.acc.y = yacc

        while table:
            # print(table)
            time = table.time
            newTable = table.segment()
            if(newTable is not None):
                time = (newTable.time - time)/FRAME_INTERVAL
                time = round(time, 0)

                for i in range(0, int(time)):
                    writeTable = table.roll(i*FRAME_INTERVAL)
                    writeTable.time = table.time/FRAME_INTERVAL + i
                    tid = db.writeTable(writeTable)

                    #comment
                    #tableshot
                    if(db.conn is None):
                        db.conn = sqlite3.connect('phylib.db')
                    cursor = db.conn.cursor()

                    insertTSCommand = f"""INSERT INTO TableShot (TABLEID, SHOTID) VALUES({tid}, '{sid}')"""
                    cursor.execute(insertTSCommand)
                    db.conn.commit()
            else:
                time = table.time
                time = time/FRAME_INTERVAL
                time = round(time, 0)
                table.time = time
                tid = db.writeTable(table)
                if(db.conn is None):
                    db.conn = sqlite3.connect('phylib.db')
                cursor = db.conn.cursor()

                insertTSCommand = f"""INSERT INTO TableShot (TABLEID, SHOTID) VALUES({tid}, '{sid}')"""
                cursor.execute(insertTSCommand)
                db.conn.commit()

            table = table.segment()
















