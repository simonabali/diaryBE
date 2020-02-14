from flask import Flask, request, jsonify
import json
from uuid import uuid4 #importing the randomizer for ids
from datetime import datetime
from flask_cors import CORS, cross_origin


app = Flask(__name__)
CORS(app)
# This simply applies CORS to the entire app, which we have referenced above. This is needed to deploy the API to the web


#------- Helper function -------
def load_db():
	# Look up and find the database file (database.JSON)
	# Save it as something or return it
	with open("database.JSON","r") as f: #f is a convention, given name, probably coming from "file"
		database = json.load(f) #turns the database to JSON
	return database
#------- End Helper function -------




#------- GET all REQUEST -------
@app.route("/diaryentry", methods=["GET"])
@cross_origin()
def get_all_diary_entries():
	db = load_db()
	n_entries = len(db)
	response = {
		"message": "Successfully got data",
		"entries": db,
		"count" : n_entries
	}
	return jsonify(response), 200 #jsonify makes the response easy to structure/ check the documentation for jsonify
	# I need a function to load my database
	# Then i need to make my database be JSON
	# Then i need to return this to the user
	# Do I need to do anything else
#------- end of GET all REQUEST -------


#------- GET one entry REQUEST -------
@app.route("/diaryentry/<entryid>", methods=["GET"])
@cross_origin() # protect endpoints (gets, post etc) so add @cross_origin(), in addition to add CORS(app) after defining app
def get_diary_entry(entryid):
# need to load the database
#  need to search the database for our entry id
#  return the entry associated with the entry ID
#  return the entry to the user with a success message
#  If the ID does not exist let the user know ID wasn't available
	db = load_db()
	our_entry = db.get(entryid)
	response = {
		"message": "Success",
		"entry": our_entry
	}
	if our_entry == 'None':
		print("Error 404")
	else:
		return jsonify(response), 200
#------- end of GET one entry REQUEST -------


#------- SAVE Helper function -------
def save_db(database):
	with open("database.JSON", "w") as f:
		json.dump(database, f, indent=4) #indent=4 will make our file look pretty   
#------- End of SAVE Helper function -------



#------- POST REQUEST -------
@app.route('/diaryentry', methods=["POST"])
@cross_origin()
def post_diary_entry():
	#get data from post request
	#save the data into a variable
	#load the database 
	#give the new entry and id

	data = json.loads(request.data)	#search request.data and response.data // loads - the s refers to string // contains what the user has sent you
	db = load_db()
	unique_id = str(uuid4())
	db[unique_id] = data
	db[unique_id]["createdat"] = str(datetime.now()) # stringify the date
	save_db(db)

	response = {
		"message": "New entry created",
		"data": data,
		"id": unique_id
	}
	return jsonify(response), 201
#------- end of POST REQUEST -------


#------- our Update  route -------
@app.route('/diaryentry/<unique_id>', methods=["PUT"])
@cross_origin()
def diary_entry_update(unique_id):
	db = load_db()
	data = json.loads(request.data)
	db[unique_id].update(data)
	db[unique_id]["updatedat"] = str(datetime.now())
	save_db(db)
	response = {
		"message": "Entry updated!",
		"data": data,
		"id": unique_id
	}
	return jsonify(response), 201
# retrieve diary entry
# overwrite message field
# overwrite title field
# save new field
#------- Update route  -------

@app.route('/diaryentry/<unique_id>', methods=["DELETE"])
@cross_origin()
def diary_entry_delete(unique_id):
	db = load_db()
	if unique_id in db:
		db.pop(unique_id)
		save_db(db)
	response = {
		"message": "Entry deleted!"
	}
	return jsonify(response), 201


# @app.route('/')
# @cross_origin()
# def home():
# if not session.get('logged_in'):
# return render_template('login.html')
# else:
# return render_template('index.html')

# request.form['password'] == 'founders'
# request.form['username'] == 'simona'


# @app.route('/login', methods=['POST'])
# def do_admin_login():
# if request.form['password'] == 'password' and request.form['username'] == 'admin':
# session['logged_in'] = True
# return render_template('diary.html')
# else:
# flash('wrong password!')
# return home()

# if __name__ == "__main__":
# app.secret_key = os.urandom(12)
# app.run(debug=True,host='0.0.0.0', port=4000)



# #------- our POST try (not working) -------
# 	key = uuid.uuid1()
# 	database_add = add_db()
# 	# database_add[key] = {
# 	#     "createdat": "2020-03-25 15:13:03.481511",
# 	#     "description": "This is our 2nd diary entry!!!",
# 	#     "title": "2nd Post!"}

# 	    database_add.update({key:["createdat"= "1", "description"= "something", "title"= "name"]})
	
# 	print("success")

# 	# we need to create a new key value pair into the database.JSON
# 	# long way: either get all data, add entry, and send back
# 	# short way: or add new key-value to the database.JSON








