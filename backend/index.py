#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from flask import Flask
from flask_cors import CORS, cross_origin

app = Flask(__name__)

@app.route("/")

@cross_origin(supports_credentials=True)  # ■■■ この行すべて
def index():
  return """
  hello python!
  """

if __name__ == "__main__":
  app.run(host="127.0.0.1", port=5000)