import sys
import cgi
import os
import phylib
import Physics

import json

# web server parts
from http.server import HTTPServer, BaseHTTPRequestHandler

# used to parse the URL and extract form data for GET requests
from urllib.parse import urlparse, parse_qsl

tables = 0
recentTableId = 0

# handler for our web-server - handles both GET and POST requests
class MyHandler( BaseHTTPRequestHandler ):

    #gets something that exists
    def do_GET(self):

        global tables
        global recentTableId

        parsed  = urlparse( self.path )

        #give shoot
        if parsed.path in [ '/players.html' ]:

            fp = open( '.'+self.path )
            content = fp.read()

            self.send_response( 200 )
            self.send_header( "Content-type", "text/html" )
            self.send_header( "Content-length", len( content ) )
            self.end_headers()

            self.wfile.write( bytes( content, "utf-8" ) )
            fp.close()

        elif parsed.path in [ '/liveshoot.html' ]:

            tables = 0
            recentTableId = 0

            fp = open( '.'+self.path )
            content = fp.read()

            self.send_response( 200 )
            self.send_header( "Content-type", "text/html" )
            self.send_header( "Content-length", len( content ) )
            self.end_headers()

            self.wfile.write( bytes( content, "utf-8" ) )
            fp.close()

        elif parsed.path in [ '/background.png' ]:

            fp = open('.' + self.path, 'rb')
            content = fp.read()

            self.send_response( 200 )
            self.send_header( "Content-type", "image/png" )
            self.send_header( "Content-length", len( content ) )
            self.end_headers()

            self.wfile.write( bytes(content) )
            fp.close()

        #give existing .svgs
        elif (parsed.path.endswith(".svg")):

            currentDir = os.getcwd()

            currentDir = os.path.join(currentDir,parsed.path[1:])

            if os.path.exists(currentDir):

                fp = open( currentDir, 'r')
                content = fp.read()

                splitContent = content.split('\n')

                savei = 0

                for i, line in enumerate(splitContent):
                    if 'WHITE' in line:
                        line = line[:-2] + 'onmousedown="oncue();"/>'
                        line = line[:8] + ' id="cueball"' + line[8:]
                        splitContent[i] = line
                    if '<svg width' in line:
                        line = line[:5] + 'id="mainsvg" ' + line[5:]
                        splitContent[i] = line
                        savei = i
                splitContent = splitContent[savei:-2] + [' <line id="stick" x1="0" y1="0" x2="0" y2="0" stroke="BROWN" stroke-width="0"/>'] + ['<line id="line" x1="0" y1="0" x2="0" y2="0" stroke="GRAY" stroke-width="0"/>'] + splitContent[-2:]

                content = '\n'.join(splitContent)

                print(content)

                self.send_response( 200 )
                self.send_header( "Content-type", "image/svg+xml" )
                self.send_header( "Content-length", len( content ) )
                self.end_headers()

                self.wfile.write( bytes(content, "utf-8") )
                fp.close()
            
            #otherwise 404
            else:
                self.send_response( 404 )
                self.end_headers()
                self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) )

        #otherwise 404
        else:
            self.send_response( 404 )
            self.end_headers()
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) )

    #makes something that doesnt exist
    def do_POST(self):

        global tables
        global recentTableId

        parsed = urlparse( self.path )

        #if display then we want to build html
        if parsed.path in [ '/display.html' ]:

            # get data send as Multipart FormData (MIME format)
            form = cgi.FieldStorage( fp=self.rfile,
                                     headers=self.headers,
                                     environ = { 'REQUEST_METHOD': 'POST',
                                                 'CONTENT_TYPE': 
                                                   self.headers['Content-Type'],
                                               } 
                                   )
            
            #get gwd and remove .svgs
            currentDir = os.getcwd()
            for file in os.listdir(currentDir):
                if file.endswith('.svg'):
                    os.remove(file)

            #format form
            fp = open('shoot.html')
            content = fp.read() % form

            #sb creation
            sb_x = float(form.getvalue("sb_x"))
            sb_y = float(form.getvalue("sb_y"))
            sb_pos = Physics.Coordinate(sb_x, sb_y)
            sb_number = int(form.getvalue("sb_number"))

            #rb creation
            rb_x = float(form.getvalue("rb_x"))
            rb_y = float(form.getvalue("rb_y"))
            rb_pos = Physics.Coordinate(rb_x, rb_y)

            rb_dx = float(form.getvalue("rb_dx"))
            rb_dy = float(form.getvalue("rb_dy"))
            rb_vel = Physics.Coordinate(rb_dx, rb_dy)

            if(phylib.phylib_length(rb_vel) > Physics.VEL_EPSILON):
                rb_acc_x = -rb_dx / phylib.phylib_length(rb_vel) * Physics.DRAG
                rb_acc_y = -rb_dy / phylib.phylib_length(rb_vel) * Physics.DRAG
            rb_acc = Physics.Coordinate(rb_acc_x, rb_acc_y)
            rb_number = int(form.getvalue("rb_number"))

            #make table
            table = Physics.Table()

            table += Physics.StillBall(sb_number, sb_pos)

            table += Physics.RollingBall(rb_number, rb_pos, rb_vel, rb_acc)

            #call simulation loops
            svgNum = 0

            if(table is not None):
                with open("table-" + str(svgNum) + ".svg", "w") as fptr:
                    fptr.write(table.svg())
                    svgNum = svgNum + 1

            while(table is not None and svgNum < 100):
                table = table.segment()
                if(table is not None):
                    with open("table-" + str(svgNum) + ".svg", "w") as fptr:
                        fptr.write(table.svg())
                        svgNum = svgNum + 1

            #header
            htmlHead = '<!DOCTYPE html> <html lang=”en”> <head> <meta charset=”utf-8” /> </head> <body style="background-color:#193319;"> <p style="font-size:48px; color:white;">Tables Generated</p> <br> <p style="font-size:32px; color:white;">Still Ball | Number: ' + str(sb_number) + ', X: ' + str(sb_x) + ', Y: ' + str(sb_y) +'</p> <br> <p style="font-size:32px; color:white;">Rolling Ball | Number: ' + str(rb_number) + ', X: ' + str(rb_x) + ', Y: ' + str(rb_y) + ', Vel X: ' + str(rb_dx) + ', Vel Y: ' + str(rb_dy) +'</p>'

            #start content building
            htmlContent = ""
            stop = False
            tNum = 0

            #keep adding .svgs and text until none remain
            while(not stop):

                if os.path.exists("table-" + str(tNum) + ".svg"):
                    htmlContent += '<img src="table-' + str(tNum) + '.svg" alt="table' + str(tNum) + '"style="width:480px;">'
                    tNum = tNum + 1
                    if(tNum % 6 == 0):
                        htmlContent += '<br>'
                        htmlContent += '<p style="font-size:32px; color:white;">Tables ' + str(tNum - 6) + '-' + str(tNum - 1) + '</p><br>'
                else:
                    stop = True
                    htmlContent += '<br>'
                    htmlContent += '<p style="font-size:32px; color:white;">Tables ' + str(tNum - (tNum % 6)) + '-' + str(tNum - 1) + '</p>'

            #add go back
            htmlContent += '<p style="font-size:32px; color:white;"> <a href="shoot.html">Click here</a> to go back </p>'

            #footer
            htmlFoot = "</body> </html>"

            #so epic
            htmlFinal = htmlHead + htmlContent + htmlFoot

            #send
            self.send_response( 200 )
            self.send_header( "Content-type", "text/html" )
            self.send_header( "Content-length", len( htmlFinal ) )
            self.end_headers()

            self.wfile.write( bytes( htmlFinal, "utf-8" ) )
            fp.close()

        if parsed.path in [ '/shot.html' ]:

            print("IM HERE", tables, recentTableId)
            
            #get gwd and remove .svgs
            currentDir = os.getcwd()
            for file in os.listdir(currentDir):
                if file.endswith('.svg'):
                    os.remove(file)

            contentLength = int(self.headers['Content-Length'])
            postData =  self.rfile.read(contentLength)
            data = json.loads(postData.decode("utf-8"))

            xvel= data[0]
            yvel= data[1]
            p1= data[2]
            p2= data[3]

            table = Physics.Table()

            if recentTableId == 0:
                table.newTable()
                db = Physics.Database(reset=True)
                db.createDB()
            else:
                db = Physics.Database()
                #get recent table
                table = db.readTable(recentTableId-1)
                print("1 table", table)

            #check cueball
            foundCB = False
            for obj in table:
                if obj is not None and obj.type == phylib.PHYLIB_STILL_BALL and obj.obj.still_ball.number == 0:
                    foundCB = True
            if not foundCB:
                sb_pos = Physics.Coordinate(675, 1350)
                table += Physics.StillBall(0, sb_pos)


            game = Physics.Game( gameName="game01", player1Name=p1, player2Name=p2 )

            game.shoot('game', p1, table, xvel, yvel )

            # #make svgs
            cur = db.conn.cursor()

            if recentTableId == 0:
                cur.execute(f"""SELECT TABLEID FROM TableShot""")
            else:
                cur.execute(f"""SELECT TABLEID FROM TableShot WHERE TableShot.TABLEID > {recentTableId}""")
        
            tableIDs = cur.fetchall()
            print(2, len(tableIDs) )
        
            print(2.5, recentTableId, recentTableId + len(tableIDs))
            for i in range( recentTableId, recentTableId + len(tableIDs) ):
                table = db.readTable( i )

            recentTableId += len(tableIDs)
            tables = len(tableIDs)

            print(3, table)

            self.send_response( 200 )
            self.send_header( "Content-type", "text/html" )
            self.send_header( "Content-length", len(str(len(tableIDs))))
            self.end_headers()

            print(4, str(len(tableIDs)))

            self.wfile.write(bytes(str(len(tableIDs)), "utf-8" ))

        #otherwise 404
        else:
            self.send_response( 404 )
            self.end_headers()
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) )

#main
if __name__ == "__main__":
    httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), MyHandler )
    print( "Server listing in port:  ", int(sys.argv[1]) )
    httpd.serve_forever()
