# qc-ui-test
Automation Testing project of QC UI

## Setup

1. Clone the project [repository](https://git.itim.vn/coccoc/labs-qc-site-test)
2. Install python3.7 and pip (python 3)
3. Run `pip install -r requirements.txt` to install used libraries

## Local
1. Install Google Chrome (version xx.xx)
2. Download corresponding Chrome Driver with version that you download Google Chrome (version xx.xx)
   
For Windows:
3. Extract Chrome Driver and copy extracted Chrome Driver to Python37_Path/Scripts
4. Set Environment variables to Python37_Path, Python37_Path/Script
5. Run `set_environments_variables.bat` with admin permission to set `PYTHONPATH` for project
    
For Linux:
   TBD

## Run all tests
If not yet set `pythonpath`:
```bash
robot -L DEBUG --outputdir results --pythonpath resources --pythonpath libs --pythonpath libs/page_object --pythonpath libs/page_object4 "tests"
```

If set `pythonpath`:
```bash
robot -L DEBUG --outputdir results "tests"
```

## Run single test case
```bash
robot -L DEBUG --outputdir results --pythonpath resources --pythonpath libs --pythonpath libs/page_object --pythonpath libs/page_object4 
```

If set `pythonpath`:
```bash
robot -L DEBUG --outputdir results -t "test_case_name" "test_case_file_path"
```

## References
[Selenium 2 library](http://robotframework.org/Selenium2Library/Selenium2Library.html)
[Python](https://www.python.org/)
[Selenium](https://www.selenium.dev/)