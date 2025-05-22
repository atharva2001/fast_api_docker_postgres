async def get_item(cursor, data):
    query = """
    SELECT * FROM items WHERE id = %s;
    """
    cursor.execute(query, data)
    result = cursor.fetchone()
    cursor.close()
    if result:
        return {"response": result}
    else:
        return {"error": "Item not found"}
    
async def get_all(cursor):
    query = """
    SELECT * from items;
    """
    cursor.execute(query)
    result = cursor.fetchall()
    if result:
        return {"response": result}
    else:
        return {"error": "No data found!"}
    
async def create_item(cursor, data, request):
    query = """
    INSERT INTO items (category, name, price)
    VALUES (%s, %s, %s)
    """

    record = (data.category, data.name, data.price)
    cursor.execute(query, record)
    request.app.state.db.commit()
    return {
        "message": "Success"
    }

async def delete_item(cursor, data, request):
    try:
        query = """
        DELETE FROM items WHERE id = %s;
        """
        cursor.execute(query, data)
        request.app.state.db.commit()
        return {
            "message": "Success"
        }
    except Exception as e:
        return {"error": str(e)}
