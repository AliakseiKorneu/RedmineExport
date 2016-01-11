import urllib
import urllib2
import sys
import argparse
import re
import json
import xmltodict

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
	return match


# Get issues info.
def get_issues_info (arguments, limit, offset):
	if (arguments.format == 'xml'):
		url = (arguments.host+'/issues.xml?project_id='+arguments.project+'&limit=%d&offset=%d') % (limit, offset)
	if (arguments.format == 'json'):
		url = (arguments.host+'/issues.json?project_id='+arguments.project+'&limit=%d&offset=%d') % (limit, offset)
	try:
		response = urllib2.urlopen(url)
		info = response.read()
		result = parse_result(info, arguments.format)
		# if not all elemets loaded, we need to load more
		if result['total_count'] > (offset + limit):
			result['projects'] += get_issues_info(arguments, limit, offset + limit)
	except Exception:
		sys.exit('Unable to get info. Please, check the entered data')

	return info

# Get projects info.
def get_projects_info (arguments, limit, offset):
	if (arguments.format == 'xml'):
		url = (arguments.host+'/projects.xml?limit=%d&offset=%d') % (limit, offset)
	if (arguments.format == 'json'):
		url = (arguments.host+'/projects.json?limit=%d&offset=%d') % (limit, offset)
	try:
		response = urllib2.urlopen(url)
		info = response.read()
		result = parse_result(info, arguments.format)
		# if not all elemets loaded, we need to load more
		if result['total_count'] > (offset + limit):
			result['projects'] += get_projects_info(arguments, limit, offset + limit)

	except Exception:
		sys.exit('Unable to get info. Please, check the entered data')

	return result['projects']

# Parse results returned from Redmine endpoint
def parse_result(info, format):
	if format == 'xml':
		data = xmltodict.parse(info)
		parsed = {}
		parsed['projects'] = json.loads(json.dumps(data['projects']['project']))
		parsed['total_count'] = int(data['projects']['@total_count'])
		return parsed

	if format == 'json':
		return json.loads(info)

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
			result = get_issues_info(arguments, 100, 0)
	if (arguments.object == 'projects'):
		result = get_projects_info(arguments, 100, 0)

	print (result)

redmine_export()
