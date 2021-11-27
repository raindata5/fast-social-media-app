from fastapi import FastAPI
from . import models
from .db import engine
from .routers import post, user, auth, favorite
from fastapi.middleware.cors import CORSMiddleware

#fetch('http://localhost:8000/').then(res => res.json()).then(console.log)


# models.Base.metadata.create_all(bind=engine)

origins =[
    "*"
]
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# while True:
#     try:
#         conn = psycopg2.connect(host='localhost',database='fastapidb', user='postgres',password= 'd041667837', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("connection realized")
#         cursor.close()
#         break
#     except Exception as error:
#         print("issue when connecting to db")
#         print(error)
#         time.sleep(3)


in_mem_posts = [
    {"title":"my post",
    "content": "my content",
    "id": 1},
    {"title":"my post2",
    "content": "my content2",
    "id": 2}
]


@app.get("/")
def root():
    return {"message": "test"}


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(favorite.router)

# @app.get('/sqlalchemy')
# def testing(db: Session = Depends(get_db)):
#     posts = db.query(models.PostModelORM).all()
#     # print(posts)
#     return {'data': posts}