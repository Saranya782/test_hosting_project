from fastapi import FastAPI
from mangum import Mangum
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../backend'))

from main import app

# Wrap FastAPI app with Mangum for AWS Lambda compatibility
handler = Mangum(app)

