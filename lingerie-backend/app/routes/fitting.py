from flask import Blueprint,jsonify,request,send_from_directory
from app.models import User,Measurement,Product,Order,OrderItem
from app.db import db
import re
import os

# create student blueprint
fitting_bp=Blueprint("fitting",__name__,url_prefix="/fitting")