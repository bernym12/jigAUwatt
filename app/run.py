from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import RadioField
from app import app
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index(states=list,states_to_str=str):
    file1 = open("onoff.txt", "r+")

    if request.method == 'POST':
        states: object = request.form.getlist('mycheckbox')
        print(states)
        states_to_str: object = ' '.join(states)
        print(states_to_str)
        file1.write(states_to_str)
        file1.close()
        return render_template('index.html')


    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')