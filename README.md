# RedmineExport
This script allows to export information about Redmine projects or issues in XML or JSON format.

```
usage: export.py [-h] -f {json,xml} -ht HOST -o {issues,projects}
                      [-p PROJECT]
optional arguments:
  -h, --help            show this help message and exit
  -f {json,xml}, --format {json,xml}
                        Export Format
  -ht HOST, --host HOST
                        Redmine Host. Format: http(s)://...
  -o {issues,projects}, --object {issues,projects}
                        Export Projects or Issues Data
  -p PROJECT, --project PROJECT
                        Project ID (if issues selected)
```
Example:
```
python export.py --format xml --host http://demo.redmine.org --objects issues --project devops-test-project > issues.xml
```

Save info about issues from project "devops-test-project" from host "http://demo.redmine.org" in XML format in issues.xml file.


TODO:
* Add limit selection
* Add opportunity to get info about ALL projects/issues
* Add sorting
* Add XML Validation
