#!/usr/env/bin python3
#coding: utf-8

__name__="LangAPI"
__version__= 0.1
__standard__="ISO 639-2"

import requests
from flask_api import FlaskAPI, status, exceptions
from flask import request, url_for


app = FlaskAPI(__name__)
app.config['DEFAULT_RENDERERS'] = [
    'flask_api.renderers.JSONRenderer',
    'flask_api.renderers.BrowsableAPIRenderer',
]
@app.route("/lang/", methods=['GET'])
def show_langs():
    return {"fre": "Français", "esp": "Espagnol"}

@app.route("/lang/name/<string:lang_code>/", methods=['GET'])
def lang_name(lang_code):
    """
    Given a code get the full name of the langage
    """
    if len(lang_code) == 2:
        return "Invalid code format for lang '%s' has to be in 3 letters format", status.HTTP_406_

    else:
        if request.method == 'GET':
            try:
                return lang[lang_code], status.HTTP_200_
            except KeyError:
                return "%s not found", status.HTTP_404_

@app.route("/lang/code/<string:lang_name>/", methods=['GET'])
def lang_code(lang_code):
    """
    Given a name and get the code of the corresponding langage
    """
    if request.method == 'GET':

        code = [{v:k} for k,v in lang.iteritems() if v.startswith(lang_code)]
        if len(code) > 0:
            return code[0], status.HTTP_200_
        else:
            return "Lang '%s' not found", status.HTTP_404_
