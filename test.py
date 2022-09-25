import subprocess
import time

for x in range(13):
	try:
		start = time.time()
		subprocess.run('python encode.py ' + str(x+1) + " 1 0 1 " + str(x+1), check=True)
		end = time.time()
		print(f"Elapsed time: {end - start} sec")
	except subprocess.CalledProcessError as e:
		print(e)
		exit();