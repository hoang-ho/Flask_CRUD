from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


class webServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                restaurants = session.query(Restaurant).all()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<p><a href='/new'>Make a New Restaurant</a></p>"
                for i in range(len(restaurants)):
                    output += f"<br> {restaurants[i].name} </br>"
                    output += f"<p><a href = '/restaurants/{i}/edit'>edit</a></p>"
                    output += f"<p><a href = '/restaurants/{i}/delete'>delete</a></p>"
                output += "</body></html>"
                self.wfile.write(output.encode("utf-8"))
                return

            if self.path.endswith("/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Make a New Restaurant</h1>"
                output += "<form method='POST' enctype='multipart/form-data' action='/new'>"
                output += "<input name='newRestaurantName' type='text' placeholder='New Restaurant Here'>"
                output += "<input type='submit' value='Create'>"
                output += "</form></body></html>"
                self.wfile.write(output.encode("utf-8"))
                return

            if self.path.endswith("/edit"):
                restaurantID = self.path.split("/")[2]
                restaurantID = str((int(restaurantID) + 1))
                queryRestaurant = session.query(
                    Restaurant).filter_by(id=restaurantID).one()
                if queryRestaurant:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

                    output = ""
                    output += "<html><body>"
                    output += f"<h1>{queryRestaurant.name}</h1>"
                    output += f"<form method='POST' enctype='multipart/form-data' action='/restaurants/{restaurantID}/edit'>"
                    output += f"<input name='newRestaurantName' type='text' placeholder='{queryRestaurant.name}'>"
                    output += "<input type='submit' value='Rename'>"
                    output += "</form></body></html>"

                    self.wfile.write(output.encode("utf-8"))
            
            if self.path.endswith("/delete"):
                restaurantID = self.path.split("/")[2]
                restaurantID = str((int(restaurantID) + 1))
                queryRestaurant = session.query(Restaurant).filter_by(id=restaurantID).one()
                if queryRestaurant:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += f"<h1>Are you sure you want to delete {queryRestaurant.name}</h1>"
                    output += f"<form method='POST' enctype='multipart/form-data' action='/restaurants/{restaurantID}/delete'>"
                    output += "<input type='submit' value='Delete'>"
                    output += "</form></body></html>"

                    self.wfile.write(output.encode("utf-8"))


        except IOError:
            self.send_error(404, f'File Not Found: {self.path}')

    def do_POST(self):
        try:
            if self.path.endswith("/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.get('content-type'))
                pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                    messagecontent[0] = messagecontent[0].decode("utf-8")

                    newRestaurant = Restaurant(name=messagecontent[0])
                    session.add(newRestaurant)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(
                    self.headers.get('content-type'))
                pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
                if ctype == 'multipart/form-data':
                    restaurantID = self.path.split("/")[2]
                    queryRestaurant = session.query(
                        Restaurant).filter_by(id=restaurantID).one()
                    if queryRestaurant:
                        fields = cgi.parse_multipart(self.rfile, pdict)
                        messagecontent = fields.get('newRestaurantName')
                        messagecontent[0] = messagecontent[0].decode("utf-8")
                        queryRestaurant.name = messagecontent[0]

                        session.add(queryRestaurant)
                        session.commit()

                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()

            if self.path.endswith("/delete"):
                restaurantID = self.path.split("/")[2]
                queryRestaurant = session.query(Restaurant).filter_by(id=restaurantID).one()
                if queryRestaurant:
                    session.delete(queryRestaurant)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print(f"Web Server running on port {port}")
        server.serve_forever()
    except KeyboardInterrupt:
        print(" ^C entered, stopping web server....")
        server.socket.close()


if __name__ == '__main__':
    main()
