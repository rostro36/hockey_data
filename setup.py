from team_dict import TEAMS, DIVISIONS, CONFERENCES
import pymysql
import os

# using environment variables or hardcoded here
env = True

if env:
    user = os.environ['USER']
    password = os.environ['PASSWORD']
    host = os.environ['HOST']
    port = os.environ['PORT']
    db_name = os.environ['DB_NAME']
else:
    user = 'root'
    reader_user = 'root'
    writer_user = 'root'
    password = 'jannik'
    reader_password = 'jannik'
    writer_password = 'jannik'
    host = 'host'
    port = '3306'
    db_name = 'hockey_teams'


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
        mycursor.execute(
            "SELECT * FROM mysql.user WHERE user = '"+reader_user+"';")
        if mycursor.fetchone() is None:
            mycursor.execute("CREATE USER '"+reader_user +
                             "'@'%' IDENTIFIED BY '"+reader_password+"';")
            mycursor.execute(
                "GRANT SELECT ON hockey_teams.* TO '"+reader_user+"'@'%';")

        mycursor.execute(
            "SELECT * FROM mysql.user WHERE user = '"+writer_user+"';")
        if mycursor.fetchone() is None:
            mycursor.execute("CREATE USER '"+writer_user +
                             "'@'%' IDENTIFIED BY '"+writer_password+"';")
            mycursor.execute(
                "GRANT SELECT, INSERT ON hockey_teams.* TO '"+writer_user+"'@'%';")
        mycursor.execute("FLUSH PRIVILEGES;")
    except ValueError as vx:
        print(vx)
        exit(1)
    except Exception as ex:
        print(ex)
        exit(1)
    finally:
        mycursor.close()
        mydb.close()
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
