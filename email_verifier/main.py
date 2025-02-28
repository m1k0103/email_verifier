import re
from multiprocessing import Pool, cpu_count
import dns.resolver
import smtplib
import yaml


def join_lists(list_array):
	final_list = []
	for l in list_array:
		final_list.extend(l)
	return final_list

# will get the contents of a specified file and return an array
def get_file_contents(path):
	with open(path, "r") as f:
		return list(f.readlines())


# gets the path from the config file
def get_file_paths():
	with open("paths.cfg") as p:
		contents = yaml.safe_load(p)
		path_array = contents["paths"]
	return list(path_array)


#checks the syntax of the emails using regex
def check_email_syntax(email):
	if re.findall('([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', email) == 0:
		return email
	else:
		return

#checks the domain that an email is using
def check_email_domain(email_list):
	domain =  # wrote all wrong. fix later #### CARRY ON HERE
	try:
		dns.resolver.resolve(domain, "MX")
		return 
		
	except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.Timeout):
		return
	


# main function
def main():
	#uses multiprocessing to get contents of multiple files faster
	with Pool(cpu_count()) as p:
		paths = get_file_paths()
		contents = p.map(get_file_contents, paths)
		# contents is currently a 2D array, so i use function to combine it into a 1D array
		emails = join_lists(contents)
		print(len(emails))
	
	#uses multiprocessing to run these contents though
	with Pool(cpu_count()) as p:
		correct_syntax_emails = p.map(check_email_syntax, emails)
		print(len(correct_syntax_emails))
		
		emails = None # not sure if needed, but setting the variable with the old emails to Null to free momery. does it help????
	
	#uses multiprocessing again to then process all the correct_syntax_emails and check if their domains are active/valid
	with Pool(cpu_count()) as p:
		domain_valid_emails = p.map(check_email_domain, correct_syntax_emails)
		pass # carry on from here
