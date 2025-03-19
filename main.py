from flask import Flask, render_template,request
from sqlalchemy import create_engine,text
# All imports go in top

app = Flask(__name__) # special Python variable that holds the name of the module.
# Connection string is in the format mysql://user:password@server/database
# --------------------vConnect to DataBasev--------------
connectionString = 'mysql://root:cset155@localhost/boatdb'
Engine = create_engine(connectionString, echo = True)
engineConnection = Engine.connect()
# -------------------------------------------------------
@app.route('/')
def greeting():
    return "Welcome"
# --------------------------------------

# ---------------------------------------------------------
@app.route('/DataBoats')
def SeeBoats():
    
    BoatTbl = engineConnection.execute(text('select * from boats')).all()
    
    return render_template('Boat.html',boats = BoatTbl)

@app.route('/Insert',methods = ['GET'])
def insertForm():
    return render_template('Insert.html')

@app.route('/Insert',methods = ['POST'])
def CreateBoat():
    try:
        engineConnection.execute(text("Insert Into boats Values (:id,:name,:type,:owner_id,:rental_price)"), request.form)
        return render_template('Insert.html',error = None, success = "successful")
    except:
        return render_template('Insert.html',error = "Failed", success = None)

@app.route('/Test/<name>')
def DisplayHTML(name = None):
    return render_template('Base.html',person = name)






if __name__ == '__main__':  #Ensures the app.run is executed only when main.py is run directly, not when it's imported in another module.
    app.run(debug=True) # debug=True argument enables debug mode, which provides: The server restart with any change and displays interactive error pages in the browser
#--------^^^^^ this Must be the last line
