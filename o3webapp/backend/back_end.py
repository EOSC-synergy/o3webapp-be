from flask import Flask,request
from userManager import UserManager

# Backend interface, which is responsible for :
# 1. listening to the user request from frontend,
# 2. passing all the information following the url
# 3. and the request-object to the user manager handling request with the corresponding process.
app = Flask(__name__)

########################################
# url list:                             
########################################

# url for homepage
@app.route('/', methods=['GET', 'POST'])
def handle_request_on_homepage():
    userManager = UserManager(request)
    return userManager.handle_process_on_homepage()

# url for plotpage with operation ID 
@app.route('/plot/<opID>', methods=['GET', 'POST'])
def handle_request_on_plotpage(opID):
    userManager = UserManager(request)
    return userManager.handle_process_on_plotpage(opID)

# url for plotpage without operation ID
@app.route('/plot', methods=['GET', 'POST'])
def enter_plotpage():
    userManager = UserManager(request)
    return userManager.handle_process_on_plotpage("api_info")
#TODO url of frontend pages
#with app.test_request_context():
    #print(url_for('/plot/', opID ='api_info'))
    #print(url_for('static', filename='plotpage.html'))

#with app.test_request_context('/plot/', method='POST'):
    #assert request.path == '/plot/'
    #assert request.method == 'POST'