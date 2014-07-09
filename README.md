qtofnotebook
============

Install python and virtualenv:
http://docs.python-guide.org/en/latest/starting/install/win/

In this directory, set up virtualenv once:
```
virtualenv .
```

Then, once, and again if the requirements ever change, run this:
```
bin/pip install -r requirements.txt
```

Run the server:
```
bin/python formserver.py
```

Edit ```form.json```.

Browse to http://localhost:8080/ to see the form. Submitting the form will append rows to ```out.csv```. Each reload of the page will catch changes in ```form.json``` and in the other directories it reads. You don't have to restart.


