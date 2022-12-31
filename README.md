# sjtu-python-api

This is the main repository of SJTU Web SSO API for Python.

## Purpose

It is annoying to enter the user name, password, then read a captcha and enter your solution to the text area when you are in a hurry, wanting to check your homework or grades in your SJTU online life.

So an automatic log-in method is always in desperate need.

## Principle

It is easy to access Internet and fetch information from servers in Python. And many operations in your SJTU life is on Web. So manually you always need a browser to finish the following task:

- Check curricula
- Check assignments
- Hand in assignments
- Discuss online
- Watch course videos
- Check grades

Before you doing these, you need to log in to `jaccount.sjtu.edu.cn` to get a pass to the other SJTU websites. And this pass is actually a cookie stored in the browser, called `JAAuthCookie`, encrypted and encoded in `Base64`. This cookie is http-only and session-alive, so when you let the browser quit, it will no longer exist. To store it persistently makes the automatic log-in possible.

But unfortunately, we need to manually input the solution to a captcha before loggin in. An OCR program is helpful to automatically read the captcha, saving human's life and energy. This project implements [Tesseract](https://github.com/tesseract-ocr/tesseract) and its wrapper [Tesserocr](https://github.com/sirfz/tesserocr) to finish this task.

## Usage

To install all the packages required of the project from PyPI, you can execute the following command in your favorite Python virtual environment at the root of this repository:

```python
pip install -r requirements.txt
```

Basically all you need are: `requests` for networking requests, `bs4` for HTML parsing, `tesserocr` for OCR operations about captcha auto-solving, `pillow` for image I/O support.

`demo.py` shows the usage of the API. As for now, it will directly show you the cookie value in the terminal after you correctly enter the user name and password and the program automatically solves the captcha.

When the developers get the value, they can manually save it in the browser with the built-in developer tools of it (or by Javascript). Also, network requests with this cookie sent (from browsers or agents) will have the access to SJTU online authenticated operations, as described above.

`classtable.py` shows how to get a class table of a undergraduate student in SJTU with this API. The output will be printed in the terminal in `json` format. Following operations could be parse the output and visualized in a GUI program.

## To-do

With logged-in state, spiders to be made will be able to fetch any convenient information and synthesize together, therefore make your online work smoother and more elegant.

## Known Issues

- Even after you entered correct user name and password, the login process may encounter "weak connection" errors. This may be caused by some protection strategies of the server and you are recommended to retry after waiting for at least 10 seconds.
