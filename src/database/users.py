async def get_user(cursor, data):
    query = """
    SELECT * FROM users WHERE id = %s
    """
    cursor.execute(query, data)
    result = cursor.fetchone()
    cursor.close()
    if result:
        return {"response": result}
    else:
        return {"error": "No data found!"}
    
async def get_all(cursor):
    query = """
    SELECT * from users;
    """
    cursor.execute(query)
    result = cursor.fetchall()
    if result:
        return {"response": result}
    else:
        return {"error": "No data found!"}

async def create_user(cursor, data, request):
    query = """
    INSERT INTO users (name, email, age)
    VALUES (%s, %s, %s)
    """

    record = (data.name, data.email, data.age)
    cursor.execute(query, record)
    request.app.state.db.commit()
    return {
        "message": "Success"
    }


async def delete_user(cursor, data, request):
    query = """
    DELETE FROM users WHERE id = %s
    """
    try:
        cursor.execute(query, data)
        request.app.state.db.commit()
        return {
            "message": "Success"
        }
    except Exception as e:
        return {
            "error": str(e)
        }