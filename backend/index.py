#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from flask import Flask, send_file
from flask_cors import cross_origin
from makeMusic import create_music

app = Flask(__name__)
XLSX_MIMETYPE = 'audio/midi'

@app.route("/")
@cross_origin(supports_credentials=True) 
def index():
  create_music()

  downloadFileName = 'sample.mid'
  downloadFile = './sample.mid'

  return send_file(downloadFile, as_attachment = True, \
      download_name = downloadFileName, \
      mimetype = XLSX_MIMETYPE)

if __name__ == "__main__":
  app.run(host="127.0.0.1", port=5000)