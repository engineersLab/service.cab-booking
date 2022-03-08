## Service to book cab for developers

### Logic behind booking a cab
1. Seating capacity of a cab is limited to 4 members
2. A cab booking can either have 100% front-end developers or 100% back-end developers.
3. Or a cab booking can have either 50% front-end developers and 50% back-end developers.


## QUICK START INSTRUCTIONS
### DB setup
1. Setup a local mysql db with docker or mysql
2. Create database named `cab-booking`
3. Run the migrations.

### Service Setup
1.  Clone this repo
1.  Reinitialize your virtual environment:  `rm -rf venv/ && python3 -m venv venv`
1.  Activate your virtual environment:  `source venv/bin/activate`
1.  Install pip requirements: `pip install -r requirements.txt`
1. `flask run`
1. The service will be open and start at http://localhost:5000/.
