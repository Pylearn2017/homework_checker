from flask import Flask, render_template

app = Flask(__name__, static_url_path='/static')


def prepare_data(data):
    sprinklers = {}
    for line in data:
        arr = line.split(',')
        key = arr[0]
        sprinklers[key] = arr[1].strip()
    return sprinklers

def get_sprinklers():
    with open('./database/sprinklers.csv', 'r') as file:
        data = file.readlines()
    sprinklers = prepare_data(data)
    return sprinklers    

def save_sprinklers(data):
    with open('./database/sprinklers.csv', 'w') as file:
        for line in data:
            file.write(f'{line}, {data[line]}\n')

def do_all(switch):
    sprinklers = {}
    data = get_sprinklers()
    num = 0
    for key in data.keys():
        sprinklers[key] = switch
        num = num + 1
    save_sprinklers(sprinklers)
    return num


@app.route('/')
def control():
    return render_template('control.html')

@app.route('/all-on')
def all_on():
    number = do_all('true')
    return render_template('all-on.html', num=number)

@app.route('/all-off')
def all_off():
    number = do_all('false')
    return render_template('all-off.html', num=number)

@app.route('/sprinklers')
def index():
    data = get_sprinklers()
    return render_template('sprinklers.html', data=data)


app.run(host='0.0.0.0', port=88)
