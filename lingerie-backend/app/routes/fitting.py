from flask import Blueprint,jsonify,request,send_from_directory
from app.models import User
from app.db import db
import re
import os

# create student blueprint
fitting_bp=Blueprint("student",__name__,url_prefix="/fitting")