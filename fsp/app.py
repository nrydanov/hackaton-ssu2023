import os
from flask import Flask, request, session, abort

from db.utils import init_connection
from utils import is_none_or_empty, hash_password
from service import UserService

from sqlalchemy import MetaData

from entity import User
from db.base import Base

app = Flask(__name__)

secret = os.environ.get('SECRET')
if secret is None:
    raise RuntimeError('Please, set the SECRET environment variable')
app.secret_key = secret

engine, session = init_connection('postgresql+psycopg2://postgres:postgres@localhost/postgres')

user_service = UserService(session)

# @app.post('/auth/login')
# async def login():
#     """
#     Аутентифицирует пользователя по `login` и `password`.
#     Проверяет предоставленный логин, в случае успеха
#     устанавливает поля `login` и `claims` во Flask
#     session-куки.

#     400 Bad Request, если логин неверный или пользователя с
#     именем `login` не существует.
#     """

#     body = request.json
#     if body is None: # Content-Type не равен application/json
#         abort(400)

#     # логин или пароль не предоставлены
#     if is_none_or_empty(body['login']) or is_none_or_empty(body['password']):
#         abort(400)

#     login = body['login']
#     password = body['password']
#     user = TODO_get_user_by_login(login)

#     # если пароль неверный
#     if not bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
#         abort(401)

#     # пользователя с таким именем не существует
#     if user is None:
#         abort(400)

#     hashed_password = user.password
    
#     # пароль неверный
#     if not TODO_check_password(hashed_password, password):
#         abort(400)

#     session['login'] = user.username
#     session['claims'] = user.claims
    
#     return '', 200

@app.post('/auth/register')
def register():
    """
    Регистрирует нового пользователя по `login` и `password`.
    Возможно добавить `first_name`, `last_name` и другую
    обязательную информацию.
    
    При успешной регистрации ответ 201 Created.
    Если имя занято, возвращает 400 Bad Request.
    """

    body = dict(request.json)
    if body is None: # Content-Type не равен application/json
        abort(400)

    # username или пароль не предоставлены
    # user: User = user_service.get_by_login(body['email'])

    # # # пользователя с таким именем существует
    # if user is not None:
    #     print('aboba')
    #     abort(400)

    # if any([is_none_or_empty(v) for v in body.values()]):
    #     print('aboba2')
    #     abort(400)

    body['password'] = hash_password(body['password'])



    try:
        user = User(**body)
        ok = user_service.add(user)
    except Exception as e:
        print(e)
        abort(400)
    
    ok = True

    return ('', 201) if ok else ('', 400)