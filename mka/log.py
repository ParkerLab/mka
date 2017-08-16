import argparse
import logging
import os
import sys


class ColoringStreamHandler(logging.StreamHandler):
    LEVEL_COLORS = {
        logging.DEBUG: '\033[34m',
        logging.ERROR: '\033[31m',
        logging.FATAL: '\033[31m',
        logging.WARN: '\033[33m',
    }

    def emit(self, record):
        tty = os.isatty(self.stream.fileno())
        if tty:
            color = self.LEVEL_COLORS.get(record.levelno, None)
            if color:
                self.stream.write(color)

        self.stream.write(self.format(record))
        self.stream.write('\n')
        if tty:
            self.stream.write('\033[0m')
        self.flush()


class LoggingArgumentParser(argparse.ArgumentParser):
    def exit(self, status=0, message=None):
        if message:
            if status == 0:
                self._print_message(message, log=logging.info)
            else:
                self._print_message(message, log=logging.error)
        sys.exit(status)

    def _print_message(self, message, file=None, log=logging.info):
        log(message)
