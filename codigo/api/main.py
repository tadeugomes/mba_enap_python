import pandas as pd
print(
pd.DataFrame([
  {"one": 0, "two": 1, "three": 2, "four": 3}, {"one": 4, "two": 5,
  "three": 6, "four": 7}, {"one": 8, "two": 9, "three": 10, "four": 11},
  {"one": 12, "two": 13, "three": 14, "four": 15}
]).to_markdown())


from flask import Flask

app = Flask(__name__)



@app.route('/')
def hello_world():
    return {'message': 'Hello World'}

if __name__ == '__main__':
    app.run(debug=True)
