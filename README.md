1. You need to upload the project to a public repository in gitlab
2. The test project must be run in docker
3. You need to create a readme page about starting and using the project

Develop a service for working with a dataset

Initial data schema:
    - 'category' (client's favorite category)
    - 'firstname'
    - 'lastname'
    - 'email'
    - 'gender'
    - 'birthDate

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