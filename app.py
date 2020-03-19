# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 13:10:06 2020

@author: joy.ramos
"""

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify