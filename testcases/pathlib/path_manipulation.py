import sys
import pathlib

class PathManipulator():
	def pathlib_path(self,tainted_file_path):
		p = pathlib.Path(tainted_file_path) # CWEID 73
		print(p.read_text())


		print(p.stat()) # CWEID 73
		print(p.chmod(777)) # CWEID 73
		print(p.exists()) # CWEID 73

		with p.open() as f: # CWEID 73
			print(f.readline())
	
		p.rename('foo.py') # CWEID 73

		p = pathlib.PosixPath(tainted_file_path) # CWEID 73
		print(p.read_text())


if __name__=='__main__':
	path_manipulation = PathManipulator()
	path_manipulation.pathlib_path(sys.argv[1])
