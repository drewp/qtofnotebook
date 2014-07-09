qtofnotebook
============

Install python and virtualenv:
http://docs.python-guide.org/en/latest/starting/install/win/

In the directory with this README, set up virtualenv (do this once):
```
virtualenv .
```

Then run this (once, and again if the requirements ever change):
```
Scripts\pip install -r requirements.txt
```

Run the web server:
```
Scripts\python formserver.py
```

Edit ```form.json```.

Browse to http://localhost:8080/ to see the form. Submitting the form will append rows to ```out.csv```. Each reload of the page will catch changes in ```form.json``` and in the other directories it reads. You don't have to restart.


