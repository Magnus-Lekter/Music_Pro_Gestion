from flask import Flask
from flask_pymongo import pymongo
from models2 import Proyecto
app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'host': "mongodb+srv://vicelis:duocuc@musicpro.ecxcb8k.mongodb.net/?retryWrites=true&w=majority",
    'alias': 'default'
}


uri = "mongodb+srv://vicelis:duocuc@musicpro.ecxcb8k.mongodb.net/?retryWrites=true&w=majority"

client = pymongo.MongoClient(uri)
db = client.get_database('musicpro')


@app.route('/')
def flask_mongodb_atlas():
    #get a project
    proyecto = db.proyecto.find_one({'nombre': 'musicpro'})
    return "flask mongodb atlas!"
if __name__ == '__main__':
    app.run(port=8000)