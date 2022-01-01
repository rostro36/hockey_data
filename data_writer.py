from sqlalchemy import create_engine
import os

# using environment variables or hardcoded here
env = False

if env:
    writer_user = os.environ['WRITER_USER']
    writer_password = os.environ['WRITER_PASSWORD']
    host = os.environ['HOST']
    port = os.environ['PORT']
    db_name = os.environ['DB_NAME']
else:
    writer_user = 'root'
    writer_password = 'jannik'
    host = 'localhost'
    port = '3306'
    db_name = 'hockey_teams'

connector_string = "mysql+pymysql://"+writer_user + \
    ":"+writer_password+"@"+host+":"+port+"/"+db_name


def append_data(df, tablename):  # hockey_teams or salary_data
    con = create_engine(connector_string).connect()
    # mydb = mysql.connector.connect(host="localhost", user="root", password="jannik", database="hockey_teams")
    try:
        df.to_sql(con=con, name=tablename, if_exists='append', index=False)
    except ValueError as vx:
        print(vx)
        exit(1)
    except Exception as ex:
        print(ex)
        exit(1)
    finally:
        con.close()
    return True
