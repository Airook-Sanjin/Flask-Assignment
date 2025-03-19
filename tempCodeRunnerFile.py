     print("SeeBoats route called")
        iD = request.form.get('id',type=int)
        name = request.form.get('name')
        BoatType = request.form.get('type')
        OwnerId = request.form.get('owner_id',type = int)
        rentalPrice = request.form.get('rental_price',type = float)
        print(f"Form Inputs: id={iD}, name={name}, type={BoatType}, owner_id={OwnerId}, rental_price={rentalPrice}")
        try:
            specificBoat = engineConnection.execute(text("Select id,name, type, owner_id ,rental_price from boats Where (:id is NULL OR id = :id) and (:name is NULL OR name = :name) and (:type is NULL Or type = :type) And (:owner_id is NULL OR owner_id = :owner_id) And (:rental_price is NULL OR rental_price = :rental_price)"), {
                'id':iD,
                'name':name,
                'type':BoatType,
                'owner_id':OwnerId,
                'rental_price': rentalPrice
            }).fetchall()
            print(f"Query Results: {specificBoat}")
            
            return render_template('Boat.html',boats = specificBoat)
        except Exception as e:
            print(f"error: {e}")
            BoatTbl = engineConnection.execute(text('select * from boats')).fetchall()
            return render_template('Boat.html',boats = BoatTbl)