from flask import Flask 	# impprt flask module
app = Flask(__name__)		# Create a new object
from app import api			# import the api file
