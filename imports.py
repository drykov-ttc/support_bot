import logging
import os
import sys
import signal
from openpyxl import load_workbook
from datetime import datetime
import telebot
from telebot import types, apihelper
import requests
import time
import config
from tabulate import tabulate
import threading


ROOT_DIR = None
logFile = os.path.join(config.WORK_DIR, config.LOG_DIR, config.LOG_STABLE)
picDir = os.path.join(config.WORK_DIR, "pic/")
raspDir = os.path.join(config.WORK_DIR, "Rasp/")
curr_month = datetime.now().strftime("%m.%Y")
fileNAme = os.path.join(raspDir, curr_month + ".xlsx")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    filename=logFile,
)

logger = logging.getLogger(__name__)


# Общие функции
def init_root_directory():
    global ROOT_DIR
    if getattr(sys, "frozen", False):
        ROOT_DIR = os.path.dirname(sys.executable)
    else:
        current_dir = os.path.abspath(os.path.dirname(__file__))
        while not os.path.exists(os.path.join(current_dir, "config.py")):
            current_dir = os.path.dirname(current_dir)
        ROOT_DIR = current_dir


init_root_directory()
