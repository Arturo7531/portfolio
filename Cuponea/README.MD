Cuponea App:

This Django application is an ongoing project planned to be deployed in Panama this year. It will serve as a coupon app intended to fill in a technological gap in the country, allowing for several industries to centralize their offers in a single platform. 

My participation in this project was mainly the building of the data pipeline, from the model of the database to the DevOps of our virtual server. I had to engineer the entire backend to ensure the proper communication of the application with front-end.

Since this is an ongoing project, only files relevant to this portfolio are included, in particular de model of the databases built.

Included in this folder are three files:
- redeem/models.py - Includes the logic for Django to execute the creation of the database that would sustain the phone application of the project, where users would log in to obtain offers.
- panel/models.py - Includes the logic for Django to execute the creation of the database that would sustain the webapp that would be used by our customers to interact with their deployed offers on the platform.
- DATABASE_DESIGN.png - A diagram of how the database ends up looking like. The tables in blue are the 'redeem' tables, and the green ones are the 'panel' tables.

The application was designed to be deployed on an Ubuntu server using Nginx.