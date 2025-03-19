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
    return render_template('Homepage.html')
# ---------------------------Update----------------

# ----------------------Search-----------------------------------
@app.route('/DataBoats', methods = ['GET','POST'])
def SeeBoats():
    
    print("SeeBoats route called")
    iD = request.form.get('id',type=int)
    name = request.form.get('name')
    BoatType = request.form.get('type')
    OwnerId = request.form.get('owner_id',type = int)
    rentalPrice = request.form.get('rental_price',type = float)
    print(f"Form Inputs: id={iD}, name={name}, type={BoatType}, owner_id={OwnerId}, rental_price={rentalPrice}")
    print(f"Request Form Data: {request.form}")
    try:
        specificBoat = engineConnection.execute(text("Select id,name, type, owner_id ,rental_price from boats Where (:id is NULL OR id = :id) and (:name is NULL OR name = :name) and (:type is NULL Or type = :type) And (:owner_id is NULL OR owner_id = :owner_id) And (:rental_price is NULL OR rental_price = :rental_price)"), {
            'id':iD,
            'name':name,
            'type':BoatType,
            'owner_id':OwnerId,
            'rental_price': rentalPrice
        }).all()
        print(f"Query Results: {specificBoat}")
        if specificBoat: 
            return render_template('Boat.html',Error = None, boats = specificBoat)
        else:
            BoatTbl = engineConnection.execute(text('select * from boats')).all()
            return render_template('Boat.html',Error = "Not Found", boats = BoatTbl)
    except Exception as e:
        print(f"error: {e}")
        BoatTbl = engineConnection.execute(text('select * from boats')).all()
        return render_template('Boat.html',boats = BoatTbl)
    
#-----------------------------------Insert----------------------------------- 
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
# ------------------------------------
@app.route('/Test/<name>')
def DisplayHTML(name = None):
    return render_template('Base.html',person = name)






if __name__ == '__main__':  #Ensures the app.run is executed only when main.py is run directly, not when it's imported in another module.
    app.run(debug=True) # debug=True argument enables debug mode, which provides: The server restart with any change and displays interactive error pages in the browser
#--------^^^^^ this Must be the last line
