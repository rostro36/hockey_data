from sqlalchemy import create_engine
import pandas as pd
import pymysql
import os

# using environment variables or hardcoded here
env = False

if env:
    reader_user = os.environ['READER_USER']
    reader_password = os.environ['READER_PASSWORD']
    host = os.environ['HOST']
    port = os.environ['PORT']
    db_name = os.environ['DB_NAME']
else:
    reader_user = 'root'
    reader_password = 'jannik'
    host = 'localhost'
    port = '3306'
    db_name = 'hockey_teams'

connector_string = "mysql+pymysql://"+reader_user + \
    ":"+reader_password+"@"+host+":"+port+"/"+db_name


def get_latest_date(latest_date):
    mydb = pymysql.connect(
        host=host, user=reader_user, password=reader_password, database=db_name)
    mycursor = mydb.cursor()
    date = None
    try:
        mycursor.execute(
            "SELECT MAX(Scraping_date) FROM salary_data WHERE Scraping_date <= '"+latest_date+"';")
        date = mycursor.fetchone()[0]
    except ValueError as vx:
        print(vx)
        exit(1)
    except Exception as ex:
        print(ex)
        exit(1)
    finally:
        mycursor.close()
        mydb.close()
    if date is None:
        raise Exception(
            'Date_error', 'There is no record in the database older than the requested date '+str(latest_date))
    else:
        start_year = date.year
        if date.month < 9:
            start_year = start_year - 1
        start_year = str(start_year)
    latest_date = date.strftime('%Y-%m-%d')
    return (latest_date, start_year)


def get_data(tablename, latest_date):
    if tablename == 'team_data':
        start_year = latest_date
    else:
        (latest_date, start_year) = get_latest_date(latest_date)
    con = create_engine(connector_string).connect()
    # mydb = mysql.connector.connect(host="localhost", user="root", password="jannik", database="hockey_teams")
    try:
        if tablename == 'salary_data':
            df = pd.read_sql("SELECT * FROM salary_data" +
                             " WHERE Scraping_date = '"+latest_date+"';", con)
        elif tablename == 'team_data':
            df = pd.read_sql("SELECT * FROM team_data" +
                             " WHERE Start_year = '"+start_year+"';", con)
        elif tablename == 'combined':
            df = pd.read_sql('''SELECT t.Team_name, t.Start_year, t.Conference, t.Divison, t.Colour, s.Scraping_date, s.OFF_players00 ,
        s.OFF_players01 ,
        s.OFF_players02 ,
        s.OFF_players03 ,
        s.OFF_players04 ,
        s.OFF_players05 ,
        s.OFF_players06 ,
        s.OFF_players07 ,
        s.OFF_players08 ,
        s.OFF_players09 ,
        s.OFF_players10 ,
        s.Players_OFF ,
        s.DEF_players00 ,
        s.DEF_players01 ,
        s.DEF_players02 ,
        s.DEF_players03 ,
        s.DEF_players04 ,
        s.DEF_players05 ,
        s.DEF_players06 ,
        s.DEF_players07 ,
        s.DEF_players08 ,
        s.DEF_players09 ,
        s.DEF_players10 ,
        s.Players_DEF ,
        s.G_players00 ,
        s.G_players01 ,
        s.G_players02 ,
        s.G_players03 ,
        s.G_players04 ,
        s.G_players05 ,
        s.G_players06 ,
        s.G_players07 ,
        s.G_players08 ,
        s.G_players09 ,
        s.G_players10 ,
        s.Players_G ,
        s.Comb_players00 ,
        s.Comb_players01 ,
        s.Comb_players02 ,
        s.Comb_players03 ,
        s.Comb_players04 ,
        s.Comb_players05 ,
        s.Comb_players06 ,
        s.Comb_players07 ,
        s.Comb_players08 ,
        s.Comb_players09 ,
        s.Comb_players10 ,
        s.Total_players ,
        s.OFF_salaries00 ,
        s.OFF_salaries01 ,
        s.OFF_salaries02 ,
        s.OFF_salaries03 ,
        s.OFF_salaries04 ,
        s.OFF_salaries05 ,
        s.OFF_salaries06 ,
        s.OFF_salaries07 ,
        s.OFF_salaries08 ,
        s.OFF_salaries09 ,
        s.OFF_salaries10 ,
        s.Salaries_OFF ,
        s.DEF_salaries00 ,
        s.DEF_salaries01 ,
        s.DEF_salaries02 ,
        s.DEF_salaries03 ,
        s.DEF_salaries04 ,
        s.DEF_salaries05 ,
        s.DEF_salaries06 ,
        s.DEF_salaries07 ,
        s.DEF_salaries08 ,
        s.DEF_salaries09 ,
        s.DEF_salaries10 ,
        s.Salaries_DEF ,
        s.G_salaries00 ,
        s.G_salaries01 ,
        s.G_salaries02 ,
        s.G_salaries03 ,
        s.G_salaries04 ,
        s.G_salaries05 ,
        s.G_salaries06 ,
        s.G_salaries07 ,
        s.G_salaries08 ,
        s.G_salaries09 ,
        s.G_salaries10 ,
        s.Salaries_G ,
        s.Comb_salaries00 ,
        s.Comb_salaries01 ,
        s.Comb_salaries02 ,
        s.Comb_salaries03 ,
        s.Comb_salaries04 ,
        s.Comb_salaries05 ,
        s.Comb_salaries06 ,
        s.Comb_salaries07 ,
        s.Comb_salaries08 ,
        s.Comb_salaries09 ,
        s.Comb_salaries10 ,
        s.Total_salaries
    FROM(
    SELECT *
    FROM team_data '''+"WHERE Start_year= '"+start_year+"') AS t"+'''
    JOIN(
    SELECT *
    FROM salary_data
    WHERE Scraping_date= \''''+latest_date+'''\') AS s
    ON t.Team_name = s.Team_name;''', con)
        else:
            raise Exception('Wrong table identifier', str(
                tablename)+" was given as identifier.")
    except ValueError as vx:
        print(vx)
        exit(1)
    except Exception as ex:
        print(ex)
        exit(1)
    finally:
        con.close()
    return df
