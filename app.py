from flask import Flask, url_for, request, render_template

app = Flask(__name__)

temp = 0
womens = 20
mens = 25
denominations = {
                50: 'red',
                40: 'blue',
                30: 'yellow',
                20: 'green',
                10: 'white',
                5: 'small_red',
                4: 'small_blue',
                3: 'small_yellow',
                2: 'small_green',
                1: 'small_white'
                }
data = {}
visual_list = []
first_recurse = True

def make_weights(weight, first_recurse, visual_list):
    if first_recurse:
        weight -= mens
        first_recurse = False

    # print('current weight: {}'.format(weight))
    for denomination in denominations.keys():
        # print("{} denom weight".format(denomination))
        if (weight-denomination) > 0:
            weight -= denomination
            visual_list.append(denominations[denomination])
            # print('break weight {}' .format(weight))
            break
        elif (weight-denomination) in [0]:
            visual_list.append(denominations[denomination])
            # print('final denom {}' .format(denomination))
            return visual_list


    if weight < 0:
        return visual_list

    # print(visual_list)
    return make_weights(weight, first_recurse, visual_list)

@app.route('/')
def home_page():
    global data
    global visual_list
    global first_recurse
    #print(data)
    cookie = request.headers.get('Cookie')
    if cookie in data:
        return render_template('home_page.html', weight=data[cookie])

    data.update({cookie: 0})
    visual_list = []
    first_recurse = True
    colors = make_weights(data[cookie], first_recurse, visual_list)
    print(colors)
    return render_template('home_page.html', weight=data[cookie], color_switch=colors)


@app.route('/set_weight', methods=['POST'])
def set_weight():
    global data
    global visual_list
    global first_recurse

    cookie = request.headers.get('Cookie')
    if cookie not in data:
        data.update({cookie: 0})

    if not request.form['weight']:
        return render_template('home_page.html', weight=data[cookie])

    data[cookie] = int(request.form['weight'])
    visual_list = []
    first_recurse = True
    colors = make_weights(data[cookie], first_recurse, visual_list)
    return render_template('home_page.html', weight=data[cookie], color_switch=colors)


@app.route('/add_weight', methods=['POST'])
def add_weight():
    global data
    global visual_list
    global first_recurse
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
    visual_list = []
    first_recurse = True
    colors = make_weights(data[cookie], first_recurse, visual_list)
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
