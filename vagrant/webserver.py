from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

class webserverHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			if self.path.endswith("/hello"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>"
				output += "Hello!"
				output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text"><input type="submit" value="Submit"></form>'''		
				output += "</body></html>"
				self.wfile.write(output)
				#print output
				return

			if self.path.endswith("/hola"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>"
				output += "&#161Hola <a href = '/hello'>Back to Hello</a>"
				output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text"><input type="submit" value="Submit"></form>'''				
				output += "</body></html>"
				self.wfile.write(output)
				#print output
				return

			if self.path.endswith("/restaurant"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				restaurants = session.query(Restaurant).all()

				output = ""
				output += "<html><body>"

				for r in restaurants:
					output += r.name
					output += "</br> <a href='/restaurant/%s/edit'>Edit</a> </br>" % r.id
					output += "<a href='/restaurant/%s/delete'>Delete</a> </br> </br>" % r.id
				output += "<a href='/restaurant/new'>Add a new restaurant</a>"
				output += "</body></html>"
				self.wfile.write(output)
				return

			if self.path.endswith("/restaurant/new"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>"
				output += "<h2> Add a new Restaurant </h2>"
				output += '''<form method='POST' enctype='multipart/form-data' action='/restaurant/new'><input name="new" type="text"><input type="submit" value="Create"></form>'''
				output += "</html></body>"
				self.wfile.write(output)
				return

			if self.path.endswith("/edit"):
				r_id = self.path.split("/")[2]
				r = session.query(Restaurant).filter_by(id=r_id).one()

				if r.name:
					self.send_response(200)
					self.send_header('Content-type', 'text/html')
					self.end_headers()

					output = ""
					output += "<html><body>"
					output += "<h1> %s <h1>" % r.name
					output += '''<form method='POST' enctype='multipart/form-data' action='/restaurant/%s/edit'><input name="updated" type="text"><input type="submit" value="Update"></form>''' % r_id
					output += "</body></html>"
					self.wfile.write(output)
				else:
					self.send_response(200)
					self.send_header('Content-type', 'text/html')
					self.end_headers()

					output = ""
					output += "<html><body></h2>Restaurant doesn't exists!!!</h2></html></body>"
					self.wfile.write(output)

			if self.path.endswith("/delete"):
				r_id = self.path.split("/")[2]
				r = session.query(Restaurant).filter_by(id=r_id).one()

				if r.name:
					self.send_response(200)
					self.send_header('Content-type', 'text/html')
					self.end_headers()

					output = ""
					output += "<html><body>"
					output += "<h1>%s will be deleted. Are you sure?<h1>" % r.name
					output += '''<form method='POST' enctype='multipart/form-data' action='/restaurant/%s/delete'><input type="submit" value="Delete"></form>''' % r_id
					output += "</body></html>"
					self.wfile.write(output)
				else:
					self.send_response(200)
					self.send_header('Content-type', 'text/html')
					self.end_headers()

					output = ""
					output += "<html><body></h2>Restaurant doesn't exists!!!</h2></html></body>"
					self.wfile.write(output)



				
		except:
			self.send_error(404, "File Not found %s" % self.path)

	def do_POST(self):
		try:
			if self.path.endswith("/restaurant/new"):
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields=cgi.parse_multipart(self.rfile, pdict)
					r_name = fields.get('new')

				print r_name[0]

				AddRestaurant = Restaurant(name = r_name[0])
				session.add(AddRestaurant)
				session.commit()

				self.send_response(301)
				self.send_header('Content-type', 'text/html')
				self.send_header('Location', '/restaurant')
				self.end_headers()

			if self.path.endswith("/edit"):
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields=cgi.parse_multipart(self.rfile, pdict)
					r_name = fields.get('updated')
					r_id = self.path.split("/")[2]

				print r_name[0]
				print r_id

				UpdateRestaurant = session.query(Restaurant).filter_by(id=r_id).one()
				UpdateRestaurant.name = r_name[0]
				session.add(UpdateRestaurant)
				session.commit()

				self.send_response(301)
				self.send_header('Content-type', 'text/html')
				self.send_header('Location', '/restaurant')
				self.end_headers()

			if self.path.endswith("/delete"):
				r_id = self.path.split("/")[2]

				print r_id

				DeleteRestaurant = session.query(Restaurant).filter_by(id=r_id).one()
				session.delete(DeleteRestaurant)
				session.commit()

				self.send_response(301)
				self.send_header('Content-type', 'text/html')
				self.send_header('Location', '/restaurant')
				self.end_headers()

			if self.path.endswith("/hello"):
				self.send_response(301)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields=cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('message')

				output = ""
				output += "<html><body>"
				output += "<h2> Okay, how about this: </h2>"
				output += "<h1> %s </h1>" %messagecontent[0]

				output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text"><input type="submit" value="Submit"></form>'''
				output += "</body></html>"
				self.wfile.write(output)


		except:
			pass

def main():
	try:
		port = 8080
		server = HTTPServer(('',port), webserverHandler)
		print "Web server running on port %s" % port
		server.serve_forever()

	except KeyboardInterrupt:
		print "^C entered, stopping web server..."
		server.socket.close()

if __name__=='__main__':
	main()
