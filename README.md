## Service to book cab for developers

## QUICK START INSTRUCTIONS
### DB setup
1. Setup a local mysql db with docker or mysql
2. Create database named `cab-booking`
3. Run the migrations from `https://github.com/engineersLab/database.cab-booking`.

### Service Setup
1.  Clone this repo
2.  Reinitialize your virtual environment:  `rm -rf venv/ && python3 -m venv venv`
3.  Activate your virtual environment:  `source venv/bin/activate`
4.  Install pip requirements: `pip install -r requirements.txt`
5. `flask run`
6. The service will be open and start at http://localhost:5000/.

### Logic behind booking a cab
1. Seating capacity of a cab is limited to 4 members
2. A cab booking can either have 100% front-end developers or 100% back-end developers.
3. Or a cab booking can have either 50% front-end developers and 50% back-end developers.

Code part that handles the booking `service/utils/util/get_cab`

### How it handles
1. The database model `cab` has `reserved_for`, `type_id` and `available_seats` properties. 
2. These properties helps in handling the cab-booking.
 - reserved_for -> reserves the cab for either frontend or backend developer
 - type_id -> stores the value of occupied developer (frontend or backend)
 - available_seats -> has the number of vacant seats in a cab

### APIS
1. Signup(POST):
    ```
    endPoint -> `/signup`
    bodyParams ->{
        "name": "name",
        "email": "name@gmail.com",
        "password": "password",
        "type": "frontend" // can be only frontend/backend
    }
    ```
2. Signin(POST):
    ```
    endPoint -> `/signin`
    bodyParams ->{
        "email": "name@gmail.com",
        "password": "password",
    }
    ```
3. Create Booking(POST):
    ```
    endPoint -> `/book-cab`
    bodyParams ->{
        "developerId": 1 // the id of the developer to book the cab
    }
    ```
4. Booking details(GET):
    ```
    endPoint -> `/booking-details/<int:booking_id>`
    ```
