import redis 
import psycopg2

conn = psycopg2.connect(
    host="127.0.0.1",
    port = "5432",
    database="testing",
    user="postgres",
    password="testing")

cursor = conn.cursor()

r = redis.Redis(host="127.0.0.1",port=6379,db=1)

r.set("me","ubuntu")

leaderboard = "players"

# for creating the user for the first time. 
def create_user(user_id,name):
    # 1st create user in redis and set score 0
    # create user in the database
    r.set(user_id,name)
    upsert_user_score(user_id,0)
    query = f"""Insert into user_leaderboard(user_id,username,points) values ('{user_id}','{name}',0)"""
    cursor.execute(query)
    conn.commit()

def upsert_user_score(user_id,score):
    r.zadd(leaderboard,{user_id:score})
    query = f"""Update user_leaderboard set points={score} where user_id = '{user_id}'"""
    cursor.execute(query)
    conn.commit()


def delete_user(user_id):
    # delete the user from redis and then from database
    r.zrem(leaderboard,user_id)
    r.rem(user_id)

# def get_top_leaderboard():
#     r.zrange()

def get_leaderboard():
    print(r.zrevrange(leaderboard,0,-1,withscores=True))

# create_user("u1","Adit")
upsert_user_score("u1",20)
get_leaderboard()