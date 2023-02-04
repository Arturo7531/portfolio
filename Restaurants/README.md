Restaurant QR Menu App:

This Django application was intended to become an application for ordering at restaurants without a need to interact with a waiter. During the beginning of the pandemic there was a need for a solution to allow for the least interactions possible between individuals. Our application allowed users at restaurants to order by using a QR code and an online menu, which would deliver the order to the kitchen directly.

My participation in this project was mainly the building of the data pipeline, from the model of the database to the DevOps of our virtual server. I had to engineer the entire backend to ensure the proper communication of the application with front-end.

Included in this folder are two files:
- models.py - Includes the logic for Django to execute the creation of the database that would sustain the application.
- DATABASE_DESIGN.png - A diagram of how the database ends up looking like.

The application was designed to be deployed on an Ubuntu server using Nginx.