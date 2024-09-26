import time

from loguru import logger


class Program:
    def __init__(self):
        self.initialized = False
        self.running = False

    def start(self):
        self.running = True
        logger.log("API", "API available at http://localhost:5359")
        logger.log("PROGRAM", "Program started")

    def run(self):
        while self.running:
            time.sleep(1)

    def stop(self):
        self.running = False
        logger.log("PROGRAM", "Program stopped")