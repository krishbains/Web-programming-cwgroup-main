# Group49 - ECS639U Group Coursework

## Group Members

Group members

Vinu Anbarasu - Assigned Hobbies Management (Backend & Frontend), contributed to all assigned tasks, + Openshift deployment and Selenium testing 

Krish Bains - Assigned Project Setup, Git Repo creation, Login, Friend requests (Backend & Frontend), contributed to all assigned tasks, + helped fix Similar Users, Openshift deployment and Selenium testing 

Askari Abdur-Rahman Islam - Assigned API Validation, Pinia setup, Profile Editing (Backend + Frontend), contributed to all assigned tasks, + static types + Hobbies Management + Openshift deployment and Selenium testing

Monesh Satheeswaran - Assigned Similar users & Filtering (Backend + Frontend), Seleneium testing, contributed to all assigned tasks + Openshift deployment and Selenium testing 

## Deployed Application on EECS Openshift 
URL of Deployed Application: https://django-psql-persistent-web-apps-ec22663.apps.a.comp-teach.qmul.ac.uk/login/?next=/ 

## Testing
For Selenimum testing: Ensure requirements.txt has been run. Activate conda environment, make migrations, then run 'python manage.py test'

Below are the 6 test requirements from LearnOuts, and the test they are satisfied in.

1. Account Creation / Signup:

    Test Name: test_account_creation_and_login

2. Login:

    Test Name: test_account_creation_and_login

3. Editing All the User's Data on Their Profile Page:

    Test Name: test_profile_edit

4. Users Page with Filtering by Age:

    Test Name: test_profile_edit

5. Sending a Friend Request:

    Test Name: test_user_search_and_friend_request_acceptance

6. Login as the Other User and Accept the Friend Request Sent:

    Test Name: test_user_search_and_friend_request_acceptance



## For manual testing:

Details of Admin User

Username: admin

Password: admin 

Details of Test Users (x5)

Username: student1

Password: Student123!

Username: student2

Password: Student123!

Username: james_brown

Password: Pass123!

Username: professor

Password: Prof123!

Username: daniel_lopez

Password: Pass123!

## Local development

To run this project in your development machine, follow these steps:

1. Create and activate a conda environment. Ensure it is using Python Version 3.11

2. Download this repo as a zip and add the files to your own private repo.

3. Install Python dependencies (main folder):

    ```console
    pip install -r requirements.txt
    ```

4. Create a development database. Ensure the api/migrations folder contains only the file __init__.py, and no other migrations.

    ```console
    python manage.py makemigrations
    ```
    Then
    ```console
    python manage.py migrate
    ```


5. Install JavaScript dependencies (from 'frontend' folder):

    ```console
    npm install
    ```

6. If everything is alright, you should be able to start the Django development server from the main folder:

    ```console
    python manage.py runserver
    ```

7. and the Vue server from the 'frontend' sub-folder:

    ```console
    npm run dev
    ```

8. Open your browser and open http://127.0.0.1:8000/ and http://localhost:5173.

## OpenShift deployment

URL: https://django-psql-persistent-web-apps-ec22663.apps.a.comp-teach.qmul.ac.uk/login/?next=/

Once your project is ready to be deployed you will need to 'build' the Vue app and place it in Django's static folder.

1. The build command in package.json and the vite.config.ts files have already been modified so that when running 'npm run build' (on Mac and Linux) the generated JavaScript and CSS files will be placed in the mainapp static folder, and the index.html file will be placed in the templates folder:

    ```console
    $ npm run build
    ```

    If using Windows run

    ```console
    $ npm run build-windows
    ```

2. You should then follow the instruction on QM+ on how to deploy your app on EECS's OpenShift live server.

## License

This code is dedicated to the public domain to the maximum extent permitted by applicable law, pursuant to [CC0](http://creativecommons.org/publicdomain/zero/1.0/).
