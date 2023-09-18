# ZeroMQ-Assessment

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
- [ ] Documentation (how to setup and run)
- [ ] ZeroMQ publisher
- [ ] ZeroMQ subscriber
- [ ] Degrees to radians conversion
- [ ] Database (solution of your choice)
- [ ] Scalability implementation(s) (e.g. service discovery)
- [ ] Testing 

### MVP

Our MVP will be a program that includes both a 0MQ subscriber and publisher. Our publisher will send lat/long messages to our subscriber, and these messages will then be stored in a relational database. 
