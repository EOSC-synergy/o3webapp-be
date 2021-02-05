from flask import Flask,url_for,redirect,request
from userManager import UserManager
# Backend interface responsible for listening to the user request from frontend
app = Flask(__name__)

# url list:

# url for homepage
@app.route('/', methods=['GET', 'POST'])
def handle_request_on_homepage():
    if request.method == 'GET':
        userManager = UserManager(request)
        return userManager.handle_process_on_homepage()
    else:
        return redirect(url_for('static', filename='plotpage.html'))
    

# url for plotpage with operation ID 
@app.route('/plot/<opID>', methods=['GET', 'POST'])
def handle_request_on_plotpage(opID):
    if request.method == 'POST':
        userManager = UserManager(request)
        return userManager.handle_process_on_plotpage(opID)
    else:
        return redirect(url_for('static', filename='plotpage.html'))


# url for plotpage without operation ID
@app.route('/plot', methods=['GET', 'POST'])
def enter_plotpage():
    return redirect(url_for('static', filename='plotpage.html'))





#with app.test_request_context():

    #print(url_for('show_post', post_id ='342'))
    #print(url_for('static', filename='login.html'))
    

#with app.test_request_context('/hello/', method='POST'):
    # now you can do something with the request until the
    # end of the with block, such as basic assertions:
    #assert request.path == '/hello/'
    #assert request.method == 'POST'


    