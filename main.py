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
# --------------------------- UDPATE ----------------
@app.route('/UpdateBoat', methods = ['GET','POST'])
def UpdateBoats():
    BoatTbl = engineConnection.execute(text('select * from boats')).all()
    try:
        engineConnection.execute(text( "Update boats Set name = :name, type = :type, owner_id = :owner_id, rental_price = :rental_price Where id = :id"),request.form)
        BoatTbl = engineConnection.execute(text('select * from boats')).all()
        # engineConnection.commit()
        return render_template('UpdateBoat.html',Error = None, success = "Success",boats = BoatTbl)
    except:
        return render_template('UpdateBoat.html',Error = "Failed", success = None, boats = BoatTbl)
    
# ------------------DELETE-----------------------------------
@app.route('/DeleteBoat', methods = ['GET','POST'])
def DeleteBoats():
    BoatTbl = engineConnection.execute(text('select * from boats')).all()
    try:
        engineConnection.execute(text( "delete from boats Where id = :id"),request.form)
        # engineConnection.commit()
        BoatTbl = engineConnection.execute(text('select * from boats')).all()
        
        return render_template('DeleteBoat.html',Error = None, success = "Success",boats = BoatTbl)
    except:
        return render_template('DeleteBoat.html',Error = "Failed", success = None, boats = BoatTbl)

# ---------------------- Search -----------------------------------
@app.route('/DataBoats', methods = ['GET','POST'])
def SeeBoats():
    
    print("SeeBoats route called")
    try:
        specificBoat = engineConnection.execute(text("Select id,name, type, owner_id ,rental_price from boats Where :id is NULL OR id = :id"),request.form ).all()
        print(f"Query Results: {specificBoat}")
        if specificBoat: 
            return render_template('Boat.html',Error = None, boats = specificBoat)
        else:
            BoatTbl = engineConnection.execute(text('select * from boats')).all()
            return render_template('Boat.html',Error = "Not Found", boats = BoatTbl)
    except Exception as e:
        print(f"error: {e}")
        BoatTbl = engineConnection.execute(text('select * from boats')).all()
        return render_template('Boat.html', boats = BoatTbl)

    
#-----------------------------------Insert----------------------------------- 
@app.route('/Insert',methods = ['GET'])
def insertForm():
    return render_template('Insert.html')

@app.route('/Insert',methods = ['POST'])
def CreateBoat():
    try:
        engineConnection.execute(text("Insert Into boats Values (:id,:name,:type,:owner_id,:rental_price)"), request.form)
        return render_template('Insert.html',Error = None, success = "successful")
    except:
        return render_template('Insert.html',Error = "Failed", success = None)
# ------------------------------------
@app.route('/Test/<name>')
def DisplayHTML(name = None):
    return render_template('Base.html',person = name)






if __name__ == '__main__':  #Ensures the app.run is executed only when main.py is run directly, not when it's imported in another module.
    app.run(debug=True) # debug=True argument enables debug mode, which provides: The server restart with any change and displays interactive error pages in the browser
#--------^^^^^ this Must be the last line
