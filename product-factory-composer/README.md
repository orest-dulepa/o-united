# OU MarketPlace

## Design Choices
A concept called "ProductMap" defines what a product does. The ProductMap comprises a set of nested Capabilities in a tree-like structure. ProductMap helps to ensure that people understand what a product does, which sounds obvious however to date frameworks have only focussed on the work to be done and not what the product does.

The work to be done on a product is organised separately to the ProductMap but in a related way.  The units of work are defined as Tasks, and these are grouped into Initiatives. 

Whilst we deliberately separate what the product does (ProductMap) from the work (Initiatives/Tasks) to be done, these are related:

* Initiatives belong to a Capability in the ProductMap
* An Initiative's Tasks are by default related to the same Capability as that Initiative
* The Capability-Task relationship can be overriden, Tasks are allowed to relate to a different Capability than their Initiative if desired

### Capability
Capability is a way of breaking down the functional and non-functional areas of the product. The nested set of Capabilities related to a Product is referred to as the ProductMap.  An example ProductMap from Mailchimp:

* Audience Management
  * Marketing CRM
    * Audience dashboard
    * Import contacts
    * Export data
    * Segmentation tool
  * Signup Forms
  * Segmentation
  * Behavioral Targeting
  * Predicted Demographics
* Creative Tools
  * Content Studio
  * Creative Assistant (Beta)
  * Dynamic Content
  * Subject Line Helper
  * Campaign Templates
* Marketing Automation
  * Customer Journeys
  * Integration
  * Transactional Email
* Insight & Analytics
  * Reports
  * Smart Recommentations
  * A/B Testing
  * Serverys
    
### Task
Tasks are units of work to be done. Tasks are grouped into Initiatives and both Tasks and Initiatives relate to a capability in the ProductMap. 

For example, a Task might be: As a user, I want to be able to tag contacts. Implement the ability for contacts to be tagged in the UI and backend.

### Initiative
Initiatives are a group of Tasks that relate to each other. Each initiative belongs to a Capability and can have multiple Tasks. The stories by default have their initiative's Category.

For example, an Initiative might be: Create new Admin Console

## How to run the project

1. Initialize project submodules
```
git submodule init
git submodule update
```

2. Create backend/.env file from backend/.env.template and update the file variables with your information.
```
cp backend/.env.template backend/.env
```

3. Run backend and frontend:
```sh
docker-compose up
```
> You need to have [docker engine](https://docs.docker.com/engine/install/) and [docker-compose](https://docs.docker.com/compose/install/) installed.

4. Import dummy data
If you want to set initial default data for testing please run this command to fill the database with some information.
```
docker-compose exec backend python manage.py dummy_data
```

5. Create a superuser
```sh
docker-compose exec backend python manage.py createsuperuser
```

6. Open the application [http://0.0.0.0:8080](http://0.0.0.0:8080)

7. The admin panel is available [http://0.0.0.0:8080/admin](http://0.0.0.0:8080/admin)

8. The application works in development mode (max 2 products & 5 users/persons).
Set license value in `LICENSE_TRIAL_KEY` variable and run the `python manage.py create_trial_license` command to create a trial license.


if after starting the project in the console the error is: "Invalid HTTP_HOST header: 'localhost:8000'. You may need to add 'localhost' to ALLOWED_HOSTS", and frontend crashes after first render.
1. Create a local_settings.py under product-factory-composer/backend/backend folder.
2. Add the following codes.
```
ALLOWED_HOSTS = [
    "localhost",
    "localhost:3000"
]
```


### Frontend
The default application is in development mode, where fake user authorization is available in the system `/switch-test-user`.
To prevent this page from being accessed and authorizing using AM:
1. Create the `frontend/.env` file.
2. Define `APPLICATION_MODE=production` variable.


## Running tests

1. Backend tests:
```
docker-compose exec backend pytest
```

2. Frontend tests:
```
docker-compose exec frontend npm test
```

## Github integration
1. Create a local_settings.py under backend/backend folder.
2. Add the following codes.
```
GIT_ACCESS_TOKEN = "<GIT_ACCESS_TOKEN>"
GIT_OWNER = "<GIT_USERNAME>"
DOMAIN = "<lt domain>"
ALLOWED_HOSTS = ["<lt domain>", "localhost:8000", "localhost:3000", "localhost", "127.0.0.1"]
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
CORS_ORIGIN_WHITELIST = [
    'http://localhost:3000'
]
```
3. How to get lt domain? Please check how to use [localtunnel](https://github.com/localtunnel/localtunnel).
4. Replace it with domain created by localtunnel.
