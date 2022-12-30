#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from flask import Flask, send_file, request, jsonify
from flask_cors import CORS, cross_origin
from makeMusic import create_music
from imageProcessing import imgProcess
from pathlib import Path
import os, glob


app = Flask(__name__)
CORS(
    app,
    support_credentials=True,
    resources={r"/*": {"credentials": True, "origins": "http://127.0.0.1:8000"}},
)
XLSX_MIMETYPE = "audio/midi"


@app.route("/", methods=["GET", "POST"])
@cross_origin(supports_credentials=True)
def index():
    create_music()

    downloadFileName = "sample.mid"
    downloadFile = "./sample.mid"

    return send_file(
        downloadFile,
        as_attachment=True,
        download_name=downloadFileName,
        mimetype=XLSX_MIMETYPE,
    )


@app.route("/process/img", methods=["GET", "POST"])
@cross_origin(supports_credentials=True)
def processImg():
    return imgProcess(request.form["file"])


@app.route("/process/complete", methods=["GET"])
@cross_origin(supports_credentials=True)
def getFiles():
    return jsonify(
        {
            "pathList": [
                Path(file).name
                for file in glob.glob(os.path.dirname(__file__) + "/output/*")
            ]
        }
    )


@app.route("/process/download", methods=["GET"])
@cross_origin(supports_credentials=True)
def getFile():
    downloadFile = "output/" + request.args.get("ID")
    downloadFileName = request.args.get("ID")

    return send_file(
        downloadFile,
        as_attachment=True,
        download_name=downloadFileName,
        mimetype=XLSX_MIMETYPE,
    )


@app.route("/uploadFile", methods=["POST"])
@cross_origin(supports_credentials=True)
def uploadFile():
    return request.form["file"]


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
