# Hockey-data website
This project daily scrapes [CapFriendly](https://www.capfriendly.com/), stores the contents in a database and visualizes it in a [website](http://hockeydata-env.eba-ygf8p3ma.us-east-1.elasticbeanstalk.com/bracket).

All\* of this is done in the [AWS-cloud](https://aws.amazon.com/):
The scraping is done by a [Lambda](https://aws.amazon.com/lambda/), the database is in [RDS](https://aws.amazon.com/rds/) and the website is hosted with [Elastic Beanstalk](https://aws.amazon.com/elasticbeanstalk/).

The whole application is serverless.
## File overview
- [logos/](./logos/) &rightarrow; contains the NHL logos
- [application.py](./application.py) &rightarrow; contains the routing and skeleton for our [dash](https://plotly.com/dash/) app
- [plotting.py](./plotting.py) &rightarrow; contains the exact plots to insert into the skeleton
- [requirements.txt](./requirements.txt) &rightarrow; contains the requirements also used for the elastic beanstalk
- [scraping.py](./scraping.py) &rightarrow; does the scraping and with slight adaptions can also be used in the Lambda
- [sql_connection.py](./sql_connection.py) &rightarrow; wrangling and connecting with the database.
- [team_dict.py](./team_dict.py) &rightarrow; contains basic information about the teams and the conferences
## Database
### Table schema
The database is only in second normal form as in the information table we have some aggregations already pre-computed. Right now, we do not need the non-aggregated values, but might need them in the future, so I left them for future-proofing.
### RDS configuration
To make life easier, choose a **public** database, but with a non-trivial password and user. Note the credentials well, as they can't be found.

Select a MySQL instance and the free tier in this case.
### Setup tables
Since the instance is public, we can setup the tables with the function *setup_tables()* from *sql_connection.py* from our local machine.

Next, the team information has to be setup with the function *populate_teams('year')* from *sql_connection.py*.

Afterwards, run *scraping.py* for the first scrape.

If everything worked out, we have the first usable results!
## Lambda
### Configuration
Things to do:
- Copy code from local editor to Lambda editor
- Adjust said code
	- Make lambda_handler work
	- Import environment variables correctly
- Give correct permissions to RDS
- Give correct VPC &rightarrow; if we want to easily connect to internet, then give no VPC
- Create and use correct layer
- Test
- Give (cron) trigger 
### Create Lambda layer
Only use the libraries used for scraping, not dashly etc., they are marked with a # in the same line. The size of the layer is only rather small and valuable.

`pip install -r requirements.txt --target ./python`
`zip python`
Upload to S3 and add as layer.

## Elastic Beanstalk
The main  file **has to** be named *application.py*, otherwise much more complicated.

*requirements.txt* will be downloaded from pip to get the libraries.

**ZIP THE FILES DIRECTLY, NOT THE FOLDER WITH THE FILES**

## How to make the project better
- Different database users
- Different VPCs and subnets
	- Database only in private subnet
	- Scraping and Elastic Beanstalk only connected to database via private subnet
		- Elastic Beanstalk is annoying with a VPC
	- Problem: this needs a (costly, but not expensive) NAT in the public subnet
- Proper domain and routing to it
- Can select data/year in website
- Proper test framework
