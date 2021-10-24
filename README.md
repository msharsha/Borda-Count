# Borda-Count
![image](https://user-images.githubusercontent.com/28890884/138312855-99d746a4-bb9a-4396-9f87-1e7908a36284.png)

> This project is to build a website to implement borda count.  It’s a method of aggregating individual preferences into a social preference.  An administrator creates an event, which is a choice among K objects (e.g. times for a meeting). N different users then rank the K objects, and the website uses the Borda Count to deliver the top choice. Extensions use other algorithms also, like bidding with points.

>The application implements the aggregation algorithm and a Python Django application for the users to submit their choice. Stakeholders for this project are Dr. Korok Ray, Dr. Duncan Walker.

![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=darkgreen) ![Django](https://img.shields.io/badge/Django-0b4b33?style=for-the-badge&logo=Django&logoColor=white)

## Installation

To create Virtual Environment(First Only, skip this step and activate Virtual Environment if you have the setup already.)
> python3 -m venv myvenv

To activate Virtual Environment:
> source myvenv/bin/activate

To update pip (First time only, skip this step if you're not setting up the application)
> python -m pip install --upgrade pip

To install necessary packages for the applications use:
> pip install -r requirements.txt
Note: `requirements.txt` has the required packages for this application. Do `pip freeze > requirements.txt` to add newly installed packages.