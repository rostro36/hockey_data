from team_dict import TEAMS, DIVISIONS, CONFERENCES
from sqlalchemy import create_engine
import pandas as pd
import pymysql

user = 'user'
password = 'password'
host = 'host'
port = '3306'
db_name = 'hockey_teams'

connector_string = "mysql+pymysql://"+user + \
    ":"+password+"@"+host+":"+port+"/"+db_name


def setup_tables():
    mydb = pymysql.connect(
        host=host, user=user, password=password)
    mycursor = mydb.cursor()
    try:
        mycursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(db_name))
        mycursor.execute("USE {}".format(db_name))
    except pymysql.Error as err:
        print("Database {} does not exists.".format(db_name))
        print(err)
        exit(1)
    try:
        mycursor.execute("SHOW TABLES LIKE 'team_data';")
        if mycursor.fetchone() is None:
            mycursor.execute(
                '''CREATE TABLE team_data (
                Team_name varchar(30),
                Start_year int,
                Conference varchar(10),
                Divison varchar(20),
                Colour varchar(20),
                PRIMARY KEY(Team_name, Start_year));''')
        mycursor.execute("SHOW TABLES LIKE 'salary_data';")
        if mycursor.fetchone() is None:
            mycursor.execute(
                '''CREATE TABLE salary_data (
        Team_name varchar(30),
        Scraping_date DATE,
        OFF_players00 FLOAT,
        OFF_players01 FLOAT,
        OFF_players02 FLOAT,
        OFF_players03 FLOAT,
        OFF_players04 FLOAT,
        OFF_players05 FLOAT,
        OFF_players06 FLOAT,
        OFF_players07 FLOAT,
        OFF_players08 FLOAT,
        OFF_players09 FLOAT,
        OFF_players10 FLOAT,
        Players_OFF FLOAT,
        DEF_players00 FLOAT,
        DEF_players01 FLOAT,
        DEF_players02 FLOAT,
        DEF_players03 FLOAT,
        DEF_players04 FLOAT,
        DEF_players05 FLOAT,
        DEF_players06 FLOAT,
        DEF_players07 FLOAT,
        DEF_players08 FLOAT,
        DEF_players09 FLOAT,
        DEF_players10 FLOAT,
        Players_DEF FLOAT,
        G_players00 FLOAT,
        G_players01 FLOAT,
        G_players02 FLOAT,
        G_players03 FLOAT,
        G_players04 FLOAT,
        G_players05 FLOAT,
        G_players06 FLOAT,
        G_players07 FLOAT,
        G_players08 FLOAT,
        G_players09 FLOAT,
        G_players10 FLOAT,
        Players_G FLOAT,
        Comb_players00 FLOAT,
        Comb_players01 FLOAT,
        Comb_players02 FLOAT,
        Comb_players03 FLOAT,
        Comb_players04 FLOAT,
        Comb_players05 FLOAT,
        Comb_players06 FLOAT,
        Comb_players07 FLOAT,
        Comb_players08 FLOAT,
        Comb_players09 FLOAT,
        Comb_players10 FLOAT,
        Total_players FLOAT,
        OFF_salaries00 FLOAT,
        OFF_salaries01 FLOAT,
        OFF_salaries02 FLOAT,
        OFF_salaries03 FLOAT,
        OFF_salaries04 FLOAT,
        OFF_salaries05 FLOAT,
        OFF_salaries06 FLOAT,
        OFF_salaries07 FLOAT,
        OFF_salaries08 FLOAT,
        OFF_salaries09 FLOAT,
        OFF_salaries10 FLOAT,
        Salaries_OFF FLOAT,
        DEF_salaries00 FLOAT,
        DEF_salaries01 FLOAT,
        DEF_salaries02 FLOAT,
        DEF_salaries03 FLOAT,
        DEF_salaries04 FLOAT,
        DEF_salaries05 FLOAT,
        DEF_salaries06 FLOAT,
        DEF_salaries07 FLOAT,
        DEF_salaries08 FLOAT,
        DEF_salaries09 FLOAT,
        DEF_salaries10 FLOAT,
        Salaries_DEF FLOAT,
        G_salaries00 FLOAT,
        G_salaries01 FLOAT,
        G_salaries02 FLOAT,
        G_salaries03 FLOAT,
        G_salaries04 FLOAT,
        G_salaries05 FLOAT,
        G_salaries06 FLOAT,
        G_salaries07 FLOAT,
        G_salaries08 FLOAT,
        G_salaries09 FLOAT,
        G_salaries10 FLOAT,
        Salaries_G FLOAT,
        Comb_salaries00 FLOAT,
        Comb_salaries01 FLOAT,
        Comb_salaries02 FLOAT,
        Comb_salaries03 FLOAT,
        Comb_salaries04 FLOAT,
        Comb_salaries05 FLOAT,
        Comb_salaries06 FLOAT,
        Comb_salaries07 FLOAT,
        Comb_salaries08 FLOAT,
        Comb_salaries09 FLOAT,
        Comb_salaries10 FLOAT,
        Total_salaries FLOAT);''')
        mydb.commit()
    except ValueError as vx:
        print(vx)
        exit(1)
    except Exception as ex:
        print(ex)
        exit(1)
    finally:
        mycursor.close()
        mydb.close()
    return


def populate_teams():
    mydb = pymysql.connect(
        host=host, user=user, password=password, database=db_name)
    mycursor = mydb.cursor()
    sql = "INSERT INTO team_data (Start_year, Team_name, Conference, Divison, Colour) VALUES (%s, %s, %s, %s, %s)"
    teams = [['2021']+[str(value) for value in TEAMS[team]] for team in TEAMS]
    divisions = [['2021']+[str(value) for value in DIVISIONS[team]]
                 for team in DIVISIONS]
    conferences = [
        ['2021']+[str(value) for value in CONFERENCES[team]] for team in CONFERENCES]
    nhl = [['2021', 'NHL', '-', '-', str((0, 0, 0))]]
    val = teams+divisions+conferences+nhl
    try:
        mycursor.executemany(sql, val)
        mydb.commit()
    except ValueError as vx:
        print(vx)
        exit(1)
    except Exception as ex:
        print(ex)
        exit(1)
    finally:
        mycursor.close()
        mydb.close()
    return str(mycursor.rowcount) + "was inserted."


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


def get_latest_date(latest_date):
    mydb = pymysql.connect(
        host=host, user=user, password=password, database=db_name)
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
        start_year = str(date.year)
        if date.month < 9:
            start_year = start_year - 1
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
