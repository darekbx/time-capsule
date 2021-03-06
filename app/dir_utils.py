import os
import zipfile
import urllib.parse
import time, datetime as dt
from dateutil.parser import parse

class DirUtils:
	
	FILE_PREVIEW_LIMIT = 1024 * 1024 # 1MB

	def is_image(self, path):
		return path.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif', '.svg'))

	def is_SQLite3(self, path):
		if not os.path.isfile(path):
			return False
		if self.file_size(path) < 100:
			return False

		with open(path, 'rb') as fd:
			header = fd.read(100)
		return header[:16].decode() == 'SQLite format 3\x00'

	def read_file_contents(self, path):
		if self.file_size(path) > self.FILE_PREVIEW_LIMIT:
			return None, "File is too big to open"
		with open(path, "rb") as handle:
			return handle.read(), None

	def make_backup(self, main_path):
		backups = "_backups"
		backup_dir = os.path.join(main_path, backups)
		backup_time = time.strftime("%Y_%m_%d_%H_%M")

		if not os.path.exists(backup_dir):
			os.makedirs(backup_dir)
		
		out_file = backup_dir + "/" + 'backup_{0}.zip'.format(backup_time)
		zipf = zipfile.ZipFile(out_file, 'w', zipfile.ZIP_DEFLATED)

		for root, dirs, files in os.walk(main_path):
			for file in files:
				if os.path.basename(os.path.normpath(root)) == backups:
					continue
				zipf.write(os.path.join(root, file))

		zipf.close()
		return out_file

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
				"path": urllib.parse.quote(relative_dir + "/" + file_name),
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

	def obtain_file_to_save(self, path, filename):
		file_to_save = os.path.join(path, filename)
		if os.path.exists(file_to_save):
			name, extension = os.path.splitext(filename)
			sufix = int(time.time())
			file_to_save = os.path.join(path, "{0}_{1}{2}".format(name, sufix, extension))
		return file_to_save

	def delete_file(self, path):
		os.remove(path)

	def make_dir(self, path, name):
		new_dir = os.path.join(path, name)
		if os.path.exists(new_dir):
			sufix = int(time.time())
			os.mkdir("{0}_{1}".format(new_dir, sufix))
		else:
			os.mkdir(new_dir)

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