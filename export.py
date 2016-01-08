import urllib
import urllib2
import sys
import argparse
import re

# Set arguments and their parametrs: is required, help messages, etc.
def create_parser ():
	parser = argparse.ArgumentParser(prog = 'Redmine Export')
	parser.add_argument ('-f', '--format', choices = ['json','xml'], required = True, help = 'Export Format')
	parser.add_argument ('-ht', '--host', required = True, help = 'Redmine Host. Format: http(s)://...')
	parser.add_argument ('-o', '--object', choices = ['issues', 'projects'], required = True, help = 'Export Projects or Issues Data')
	parser.add_argument ('-p', '--project', help = 'Project ID (if issues selected)')

	return parser 

# Check host address. 
def check_host_address (url):
	regex = re.compile(
			r'^(?:http|ftp)s?://' 
			r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' 
			r'localhost|' 
			r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' 
			r'(?::\d+)?' 
			r'(?:/?|[/?]\S+)$', re.IGNORECASE)
	match = regex.match(url)
	if (match):
		return True
	else:
		return False

# Get issues info.		
# There is no requirements for the limit of returned projects/issues and for order. Left by default.
# There is no XML validation. We get data that Redmine returnes.
def get_issues_info (arguments):
	if (arguments.format == 'xml'):
		url = arguments.host+'/issues.xml?project_id='+arguments.project
	if (arguments.format == 'json'):
		url = arguments.host+'/issues.json?project_id='+arguments.project
	try:
		response = urllib2.urlopen(url)
		info = response.read()
	except Exception:
		sys.exit('Unable to get info. Please, check the entered data')

	return info

# Get projects info.
def get_projects_info (arguments):
	if (arguments.format == 'xml'):
		url = arguments.host+'/projects.xml'
	if (arguments.format == 'json'):
		url = arguments.host+'/projects.json'
	try:
		response = urllib2.urlopen(url)
		info = response.read()
	except Exception:
		sys.exit('Unable to get info. Please, check the entered data')

	return info

def redmine_export ():
	parser = create_parser()
	# Convert arguments to lower case. It allows to enter argements in any case.
	raw_arguments = map(str.lower,sys.argv[1:])
	arguments = parser.parse_args(raw_arguments)
	isValid = check_host_address(arguments.host)

	if (isValid == False):
		sys.exit('Please, check the format of host address. Format: http(s)://...')
	# If Issues object is selected, user must enter project ID
	if (arguments.object == 'issues'):
		if (arguments.project is None):
			sys.exit('Please, enter project ID')
		else:
			result = get_issues_info(arguments)
	if (arguments.object == 'projects'):
		result = get_projects_info(arguments)

	print (result)

redmine_export()