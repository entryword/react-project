import logging
import logging.handlers
import logging.config
import yaml
import os
import zlib
import time
import gzip

def namer(name):
	return name + ".gz"


def rotator(source, dest):
	print(f"compressing {source} -> {dest}")
	with open(source, "rb") as sf:
		data = sf.read()
		compressed = zlib.compress(data, 9)
		with open(dest, "wb") as df:
			df.write(compressed)
	os.remove(source)


class MyRotatingFileHandler(logging.handlers.TimedRotatingFileHandler):

	# 覆寫TimedRotatingFileHandler
	def __init__(
		self,
		filename,
		mode="a",
		maxBytes=0,
		backupCount=0,
		encoding=None,
		delay=0,
		when="h",
		interval=1,
		utc=False,
	):
		if maxBytes > 0:
			mode = "a"
		logging.handlers.TimedRotatingFileHandler.__init__(
			self, filename, when, interval, backupCount, encoding, delay, utc
		)
		self.maxBytes = maxBytes
		self.backupCount = backupCount

	def shouldRollover(self, record):
		""" Determine if rollover should occur. """
		# 確認 rollover 大小
		if self.stream is None:	 
			self.stream = self._open()
		if self.maxBytes > 0:  
			msg = "%s\n" % self.format(record)
			self.stream.seek(0, 2)	
			if self.stream.tell() + len(msg) >= self.maxBytes:
				return 1
		t = int(time.time())
		if t >= self.rolloverAt:
			return 1
		return 0

	def rotate(self, source, dest):
		print(f"compressing {source} -> {dest}")
		os.rename(source, dest)
		f_in = open(dest, "rb")
		f_out = gzip.open("%s.gz" % dest, "wb")
		f_out.writelines(f_in)
		f_out.close()
		f_in.close()
		os.remove(dest)


class LoggerCalss(object):
	def __init__(self):
		logging.config.dictConfig(yaml.load(open("config.yaml").read()))
		self.logger = logging.getLogger(__name__)
		self.logger.info("Completed configuring logger()!")

	def debug(self, text):
		self.logger.debug(text)

	def info(self, text):
		self.logger.info(text)

	def warning(self, text):
		self.logger.warning(text)

	def error(self, text):
		self.logger.error(text)

	def critical(self, text):
		self.logger.critical(text)

