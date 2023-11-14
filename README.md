# Task

Develop a service for working with a dataset

Initial data schema:
- `category` (client's favorite category)
- `firstname`
- `lastname`
- `email`
- `gender`
- `birthDate`

Without using third party libraries: read csv file
Write the received data to the database.
Display data as a table with pagination (but you can also use a simple json api)

Implement filters by values:
    category
    gender
    Date of Birth
    age
    age range (for example, 25 - 30 years)

Implement data export (in csv) according to the specified filters.

## Setup

- `docker build -t rexit .`
- `docker run -d --name clients_api -p 80:80 rexit`
  
## Usage 

The service has 2 enpoints:
- `/download`: Takes parameters for filtering (category, gender, birthdate, age or age_start and end_age) as query parameters. 
  - Example: `http://localhost:80/download/?category=toys&gender=female&birthdate=2001-10-06`
- `/clients`: Takes page and limit query parameters to request table with pagination
  - Example: `http://localhost:80/clients/?page=130&limit=1000`
