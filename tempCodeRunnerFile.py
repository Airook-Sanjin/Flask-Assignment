@app.route('/UpdateBoat', methods = ['GET','POST'])
def UpdateBoats():
    BoatTbl = engineConnection.execute(text('select * from boats')).all()
    try:
        engineConnection.execute(text( "Update boats Set name = :name, type = :type, owner_id = :owner_id, rental_price = :rental_price Where id = :id"),request.form)
        
        return render_template('UpdateBoat.html',error = None, success = "Success",boats = BoatTbl)
    except:
        return render_template('UpdateBoat.html',error = "Failed", success = None, boats = BoatTbl)