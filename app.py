from flask import Flask, url_for, request, render_template

app = Flask(__name__)

temp = 0
womens = 15
mens = 20
data = {}

def make_weights(weight):
    denominations = {50:'red',40:'blue',30:'yellow',20:'green',10:'white'}
    visual_mapping = {}
    weight -= mens
    for denomination in denominations.keys():
        if (weight-denomination) > 0:
            weight -= denomination
            visual_mapping.update({denominations[denomination]:'T'})

    print(visual_mapping)
    return visual_mapping

@app.route('/')
def home_page():
    global data
    print(data)
    cookie = request.headers.get('Cookie')
    if cookie in data:
        return render_template('home_page.html', weight=data[cookie])

    data.update({cookie: 0})
    colors = make_weights(data[cookie])
    return render_template('home_page.html', weight=data[cookie], color_switch=colors)


@app.route('/set_weight', methods=['POST'])
def set_weight():
    global data
    cookie = request.headers.get('Cookie')
    if cookie not in data:
        data.update({cookie: 0})

    if not request.form['weight']:
        return render_template('home_page.html', weight=data[cookie])

    data[cookie] = int(request.form['weight'])
    make_weights(data[cookie])
    colors = make_weights(data[cookie])
    return render_template('home_page.html', weight=data[cookie], color_switch=colors)


@app.route('/add_weight', methods=['POST'])
def add_weight():
    global data
    cookie = request.headers.get('Cookie')
    if cookie not in data:
        data.update({cookie: 0})

    if request.form.getlist('plus_1'):
        data[cookie] += 1
    if request.form.getlist('plus_2'):
        data[cookie] += 2
    if request.form.getlist('plus_3'):
        data[cookie] += 3
    if request.form.getlist('plus_4'):
        data[cookie] += 4
    if request.form.getlist('plus_5'):
        data[cookie] += 5
    make_weights(data[cookie])
    colors = make_weights(data[cookie])
    return render_template('home_page.html', weight=data[cookie], color_switch=colors)

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         return do_the_login()
#     else:
#         return show_the_login_form()
#
# @app.route('/rici')
# def rici_world():
#     return 'is beauts'
#
# @app.route('/s')
# def stuff():
#     return app.send_static_file('skulpty.html')
#
# @app.route('/rici/<int:user>')
# def rici_user(user):
#     return "User {}" .format(user)
#
# @app.route('/sidebar')
# def sidebar():
#     return render_template('sidebar.html')
#

# def do_the_login():
#     return 'logged in'
#
# def show_the_login_form():
#     return 'log in form'
#
# @app.route('/user/<username>')
# def profile(username):
#     return '{}\'s profile'.format(username)
#
# @app.route('/hello/')
# @app.route('/hello/<name>')
# def hello(name=None):
#     return render_template('hello.html', name=name)


with app.test_request_context():
    print(url_for('home_page'))
    print(url_for('set_weight'))
    print(url_for('add_weight'))
    # print(url_for('hello_world'))
    # print(url_for('login'))
    # print(url_for('login', next='/'))
    # print(url_for('profile', username='John Doe'))
    # print(url_for('rici_user', user=12))
    # print(url_for('login', _method='POST'))
    # print(url_for('static', filename='style.css'))

#with app.test_request_context('/set_weight', method='POST'):
#     # now you can do something with the request until the
#     # end of the with block, such as basic assertions:
#     assert request.path == '/login'
#     assert request.method == 'POST'
#     print(request.data)
#     print(request.get_data())
#     print(request.base_url)

if __name__ == '__main__':
    app.run()
