# ZeroMQ-Assessment

## Dependencies

Python3 3.11.5 <br>
Pip3 23.2.1 <br>
PostgreSQL 14 <br>
Pyzmq <br>
Pyscopg2-binary <br>

## Setup

<b> 1. Clone this repository </b><br>
<b> 2. Install dependencies </b><br>

ZeroMQ Pyzmq Library <br>
`pip3 install pyzmq`

Psycopg2-binary <br>
`pip3 install psycopg2-binary`

Install [PostgreSQL](https://www.postgresql.org/download/) | This program utilizes PostgreSQL 14. <br>

<b> 3. Set up database </b> <br>

a. Open PostgreSQL <br>
b. Create database <br>
c. Open psql terminal on new database <br>
d. Execute the following script: <br>

```
CREATE TABLE "public.lat_long_messages" (
	"ID" serial NOT NULL,
	"lat_rad" DECIMAL(8,5) NOT NULL,
	"long_rad" DECIMAL(8,5) NOT NULL,
	CONSTRAINT "lat_long_messages_pk" PRIMARY KEY ("ID")
) WITH (
  OIDS=FALSE
);
```

e. Navigate to program directory, access `dbmodule.py`, change lines 9 and 10 to reflect your database settings. 

<b> 4. Run the program! </b> This can be done in multiple ways. <br>
   a. Run each script (`proxy.py` , `mqsubscriber.py` , `mqpublisher.py`) individually, any order is acceptable. Example: `python3 proxy.py` etc. <br>
   b. Run `run_program.py` which will run all 3 concurrently. This will only terminate by interruption. <br>
   c. Run `run_program_test.py` which will run all 3, but with test flags. This will terminate after 5 iterations. <br>

### Prompt

Write a program that subscribes to a ZeroMQ `lat/lon` publisher and ingests messages into a database.
 
`lat/lon` messages should look like this:

```
{
    "lat": 32.10030,
    "lon": 89.10230
}
```
 
The subscriber program should enter a "while" loop to wait for incoming `lat/lon` messages.  When it receives one, it converts the `lat/lon` message from degrees to radians.  It then stores the message (in radians) in a database (relational or non relational - your choice).

Your working solution should include the following:  
- [x] Documentation (how to setup and run)
- [x] ZeroMQ publisher
- [x] ZeroMQ subscriber
- [x] Degrees to radians conversion
- [x] Database (solution of your choice)
- [x] Scalability implementation(s) (e.g. service discovery)
- [x] Testing 

### MVP

Our MVP will be a program that includes both a 0MQ subscriber and publisher. Our publisher will send lat/long messages to our subscriber, and these messages will then be stored in a relational database. 

### Future Roadmap

- Expanded testing suite: Integration testing, test mock sockets
- Build pipleline to automate tests
- Impement a more complex pattern to: cache messages for late joining subscribers to receive updates from, add backup server, add heartbeats to inform client of server failures/inaccessibility
