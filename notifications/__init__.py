from fastapi import FastAPI
from enum import Enum
import smtplib
from typing import Dict
from fastapi.websockets import WebSocket, WebSocketDisconnect