#!/usr/bin/env python
# coding: utf-8
# Copyright 2013 Abram Hindle
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# You can start this by executing it in python:
# python server.py
#
# remember to:
#     pip install flask


import flask
from flask import Flask, request
import json
app = Flask(__name__, template_folder="static", static_folder="static")
app.debug = True


class World:
    def __init__(self):
        self.space = dict()

    def update(self, entity, key, value):
        entry = self.space.get(entity, dict())
        entry[key] = value
        self.space[entity] = entry

    def set(self, entity, data):
        self.space[entity] = data

    def clear(self):
        self.space = dict()

    def get(self, entity):
        return self.space.get(entity, dict())
    
    def world(self):
        return self.space

# you can test your webservice from the commandline
# curl -v   -H "Content-Type: application/json" -X PUT http://127.0.0.1:5000/entity/X -d '{"x":1,"y":1}' 


myWorld = World()


def flask_post_json():
    """ The joys of frameworks! They do so much work for you that they get in the way of sane operation!"""
    if request.json is not None:
        return request.json
    elif request.data is not None and request.data.decode("utf8") != u'':
        return json.loads(request.data.decode("utf8"))
    else:
        return json.loads(request.form.keys()[0])


@app.route("/")
def hello():
    """Return something coherent here. perhaps redirect to /static/index.html """
    return flask.render_template("index.html")


@app.route("/entity/<entity>", methods=['POST', 'PUT'])
def update(entity):
    """update the entities via this interface"""
    myWorld.set(entity, flask_post_json())
    return flask.Response(json.dumps(myWorld.get(entity)), status=200, mimetype="application/json")


@app.route("/world", methods=['POST', 'GET'])
def world():
    """you should probably return the world here"""
    return flask.Response(json.dumps(myWorld.world()), status=200, mimetype="application/json")


@app.route("/entity/<entity>")
def get_entity(entity):
    """This is the GET version of the entity interface, return a representation of the entity"""
    response = json.dumps(myWorld.get(entity))
    return flask.Response(response, status=200, mimetype="application/json")


@app.route("/clear", methods=['POST', 'GET'])
def clear():
    """Clear the world out!"""
    myWorld.clear()
    return flask.Response(json.dumps(dict()), status=200, mimetype="application/json")


if __name__ == "__main__":
    app.run()
