import requests as rq
from fastapi import HTTPException
from pydantic import json
from application.models import Users, Countries


async def get_user_from_request(user_name,
                                url = "https://api.nationalize.io/?name=") -> json:
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                      " AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/132.0.0.0 Safari/537.36"
    }

    user = rq.get(url + user_name, headers=headers)
    return user.json()


async def add_to_database(user, session) -> Users:
    try:
        if user.__class__ is dict:
            user = Users(name=user.get("name"),
                         country=[Countries(**i) for i in user.get("country")])
        else:
            user = Users(name=user.name,
                         country=[Countries(**i.dict()) for i in user.country])
    except Exception:
        raise HTTPException(status_code=500, detail="Can't create user")

    session.add(user)
    session.commit()
    return user