import os

def start():
	# create input file folder
	if "inputs" not in os.listdir("./email_verifier/"):
		os.mkdir("email_verifier/inputs")

	# creates the paths.cfg file
	if "paths.cfg" not in os.listdir():
		f = open("paths.cfg", "w+")
		f.write("""paths: ['/your/path/here', './second/path/here']""")
		f.close()

	from email_verifier.main import main
	main()
