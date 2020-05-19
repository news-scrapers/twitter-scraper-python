FROM kennethreitz/pipenv

COPY . .

# -- Replace with the correct path to your app's main executable
CMD python3 main.py