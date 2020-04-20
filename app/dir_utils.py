import os
import time, datetime as dt
from dateutil.parser import parse

class DirUtils:
	
	def fetch_content(self, absolute_dir, relative_dir, is_root):
		files_in_directory = os.listdir(absolute_dir)
		output = []

		if not is_root:
			head, tail = os.path.split(relative_dir)
			output.append({ "name": "[..]", "path": head, "date": "_", "is_dir": True })

		for file_name in files_in_directory:
			path = absolute_dir + "/" + file_name
			file_size = self.file_size(path)
			file_date = self.file_date(path)
			file_date_time = self.file_date_time(file_date)
			is_dir = os.path.isdir(path)
			output.append({
				"name": "{0}".format(file_name) if is_dir else file_name,
				"path": relative_dir + "/" + file_name,
				"size": self.sizeof_fmt(file_size),
				"date": file_date_time.strftime('%Y-%m-%d %H:%M:%S'),
				"is_dir": is_dir
			})


		return sorted(output, key=lambda item: (item['is_dir'], item['date']), reverse=True)

	def file_date_time(self, file_date):
		return parse(str(time.ctime(file_date)))

	def file_size(self, path):
		return os.stat(path).st_size

	def file_date(self, path):
		return os.path.getmtime(path)

	def sizeof_fmt(self, num, suffix='B'):
		for unit in ['','K','M','G','T','P','E','Z']:
			if abs(num) < 1024.0:
				return "%3.1f%s%s" % (num, unit, suffix)
			num /= 1024.0
		return "%.1f%s%s" % (num, 'Yi', suffix)

	def dir_size(self, dir_path):
		total_size = 0
		for dirpath, dirnames, filenames in os.walk(dir_path):
			for f in filenames:
				fp = os.path.join(dirpath, f)
				if not os.path.islink(fp):
					total_size += os.path.getsize(fp)
		return total_size