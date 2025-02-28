import socks
import re
from multiprocessing import Pool, cpu_count
import dns.resolver
import smtplib
import yaml
import string
import random
from urllib.parse import urlparse


# i love stack overflow.
proxy_url = urlparse('socks5://p.webshare.io:9999')

def _smtplib_get_socket(self, host, port, timeout):
    # Patched SMTP._get_socket
    return socks.create_connection(
        (host, port),
        timeout,
        self.source_address,
        proxy_type=socks.HTTP,
        proxy_addr=proxy_url.hostname,
        proxy_port=int(proxy_url.port)
    )



def generate_fake_email():
	id = "".join(random.choices(string.ascii_lowercase + string.digits, k=9))
	return f"noreply.{id}@example.com"


def join_lists(list_array):
	final_list = []
	for l in list_array:
		final_list.extend(l)
	return final_list


# will get the contents of a specified file and return an array
def get_file_contents(path):
	with open(path, "r") as f:
		content = list(f.readlines())
		cleaned = [i.strip("\n") for i in content]
		return cleaned


# gets the path from the config file
def get_file_paths():
	with open("paths.cfg") as p:
		contents = yaml.safe_load(p)
		path_array = contents["paths"]
	return list(path_array)


#checks the syntax of the emails using regex
def check_email_syntax(email):
	if re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b',email):
		return email
	else:
		return

#checks the domain that an email is using
def check_email_domain_smtp(email):
	try:
		# check domain
		domain = email.split("@")[1] # wrote all wrong. fix later #### CARRY ON HERE
		mx_records = dns.resolver.resolve(domain, "MX")
		mx_host = str(mx_records[0].exchange)

		#check SMTP
		server = smtplib.SMTP(timeout=1)
		server.connect(mx_host)
		server.helo()
		server.mail(generate_fake_email())
		code, _ = server.rcpt(email)
		server.quit()
		print(f"!!! valid {email}")
		if code == 250:
			return email
	except Exception as e:
		print(e)
		print(f"{email} invalid")
		return
	except ConnectionRefusedError:
		print("--- Connection refused")


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
		
	
	#uses multiprocessing again to then process all the correct_syntax_emails and check if their domains are active/valid
	with Pool(cpu_count()) as p:
		valid_emails = p.map(check_email_domain_smtp, correct_syntax_emails)
	with open("out.txt", "a") as f:
		for e in valid_emails:
			f.write(f"{e}\n")
	print("done finally....")