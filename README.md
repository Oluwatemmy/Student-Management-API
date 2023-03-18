<!-- Back to Top Navigation Anchor -->
<a name="readme-top"></a>

<!-- Project Shields -->
<div align="center">

  [![Contributors][contributors-shield]][contributors-url]
  [![Forks][forks-shield]][forks-url]
  [![Stargazers][stars-shield]][stars-url]
  [![Issues][issues-shield]][issues-url]
  [![MIT License][license-shield]][license-url]
  [![Twitter][twitter-shield]][twitter-url]
</div>

<!-- Project Name -->
<div align="center">
  <h1>Student Management API</h1>
</div>

<div>
  <p align="center">
    <a href="https://github.com/Oluwatemmy/Student-Management-API#readme"><strong>Explore the Documentation »</strong></a>
    <br />
    <a href="https://github.com/Oluwatemmy/Student-Management-API/blob/main/images/student_api_full_page.png">View Demo</a>
    ·
    <a href="https://github.com/Oluwatemmy/Student-Management-API/issues">Report Bug</a>
    ·
    <a href="https://github.com/Oluwatemmy/Student-Management-API/issues">Request Feature</a>
  </p>
</div>

---

<!-- Table of Contents -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-student-api">About Student Management API</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li><a href="#knowledge-acquired">Knowledge Acquired</a></li>
    <li><a href="#project-scope">Project Scope</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#installaton">Installation</a></li>
    <li><a href="#sample">Sample</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
  <p align="right"><a href="#readme-top">back to top</a></p>
</details>

---

<!-- About the Project -->
## About Student Management API

Student Management API does the main function of a school and explains how it works. It enables the school to create an admin account. It allows the registration of students and lecturers. Also, the API allows the school admin to create courses and handling the grading system for the student.

CRUD operations can be carried out on the student data and the courses data, with an easy-to-use Swagger UI setup for testing and integration with the front end.

A Student account have limited access to the app, as a student can only change their profile details and view their profile, courses, grades and GPA.

This Student Management API was built with Python's Flask-RESTX by <a href="https://www.github.com/Oluwatemmy">Ajayi Oluwaseyi</a> during Backend Engineering live classes at <a href="https://altschoolafrica.com/schools/engineering">AltSchool Africa</a>. This was built as my third semester final capstone project in <b>AltSchool Africa</b>. 

<p align="right"><a href="#readme-top">back to top</a></p>

### Built With:

![Python][python]
![Flask][flask]
![SQLite][sqlite]

<p align="right"><a href="#readme-top">back to top</a></p>

---
<!-- Lessons from the Project -->
## Knowledge Acquired

Creating this API helped me learn and practice:
* API Development with Python
* Unit Testing using pytest and Postman
* Routing
* Swagger Documentation
* Debugging
* Database Management
* App Security
* User Authentication and Authorization

<p align="right"><a href="#readme-top">back to top</a></p>

---
<!-- What the API can do -->
## Project Scope

The Student Management API handles the following:
* Admin Registration
* Lecturer Registration
* Student Registration
* Getting Student Information and applying the CRUD operation
* Course Creation
* Getting a Course details and using the CRUD operation
* Multiple Course Registration for Students
* Assigning a Lecturer to a course
* Adding a Student Score
* Calculating a Student GPA using the 4.0 Grading System.

The future Versions will cover more aspects and features as needed soon.

---

<!-- GETTING STARTED -->
## Usage

To explore and use this API, follow these steps:

1. Open the web app on your browser: https://student-flask-api.herokuapp.com/

2. Create an admin or student or lecturer account:
   - Click 'auth' to reveal a dropdown menu of the authentication routes, then register an admin account via the '/auth/signup' route. Input your details and input 'admin' in the 'user-type' to create an admin account.
   - Click 'auth' to reveal a dropdown menu of the authentication routes, then register a student account via the '/auth/signup' route. Input your details and input 'student' in the 'user-type' to create an admin account.
   - Click 'auth' to reveal a dropdown menu of the authentication routes, then register a lecturer account via the '/auth/signup/lecturer' route. Input your details to create a lecturer account.

3. Login via the '/auth/login' route to generate a JWT token. Copy the access token only without the quotation marks

4. Scroll back up to click <b>Authorize</b> at top right. Enter the JWT token in the given format, for example:
   ```
   Bearer eyJhbtestXVCJ9.eyJbmMzd9.this_rQh8_tl2V1iDlsl_wAOMHcing5334
   ```

5. Click <b>Authorize</b> and then <b>Close</b>.

6. Now authorized, you can create, view, update and delete students, courses and grades via the routes in <b>'students'</b> and **'courses'**. You can also see the information about:
    - All students taking a course
    - All courses taken by a student
    - A student's grades in percentage (example: 84.0) and letters (eg: B+)
    - A student's GPA, calculated using the 4.0 grading system based on all grades from all courses they are taking (example: 3.3)
   
7. Go to the **Course** Namespace and create a new course before adding a student to the course

8. Then go on ahead to perform other operations and test all the routes. <b>_Enjoy!_</b>

9. When you're done, click 'Authorize' at top right again to then 'Logout'. Also, head on to the **'/auth/logout'** route to log the user out and revoke the access token.

**Note:** Any registered user can request to reset their password through the **'/auth/password-reset-request'** route and the link to reset their password will be sent to the user's mail.
    Copy the token from the link that was sent to your mail and paste it in the token field in the **'/auth/password-reset/<token>'** route. Then you can go on to change your password.

<p align="right"><a href="#readme-top">back to top</a></p>

---

<!-- Installing this app on your machine locally -->
## Installation

<div></div>
<ul style="font-size:18px;">
    <li>Clone the repository to your local machine.</li>
    <li>Navigate to the project directory.</li>
    <li>Create a virtual environment and activate it:</li>
    <li>Open the requirements.txt file amd remove the uwsgi package</li>
    <li>Install the dependencies:</li>
    <li>Run the application:</li>
</ul>

### To create a virtual environment called 'venv' and activate it.

```console
python -m venv venv
source venv/bin/activate
```

**Note:** Open the requirements.txt file and remove the uwsgi package which is also the last package. It is likely for you to run into an error if you don't remove it because this is the dyno used to run the app on heroku and will not work on your local machine. After doing this, you can go ahead and install the rest with this command. 

```console
pip install -r requirements.txt
```

### To create your database locally.

```console
flask shell     # press enter
db              # press enter
User            # press enter
Admin           # press enter
Student         # press enter
Course          # press enter
StudentCourse   # press enter
Score           # press enter
db.create_all() # press enter
exit()          # press enter
```

### Finally, To run the application.

```console
python app.py
```

# Endpoints for the Student Management API

<div style="margin-top:8px; margin-bottom:10px; font-size:20px; font-weight:bold;">Auth EndPoint</div>
<!-- Tables for routing in each models -->

| ROUTE                          | METHOD | DESCRIPTION                                   | AUTHORIZATION          | USER TYPE |
|--------------------------------| ------ |-----------------------------------------------|------------------------|-----------|
| `/auth/signup`                 | _POST_ | Creation of students and admin account        | `None`                 | Any       |
| `/auth/login`                  | _POST_ | Creation of JWT Tokens for students and admin | `None`                 | Any       |
| `/auth/refresh`                | _POST_ | Creation of Access Tokens for all account     | `Bearer Refresh-Token` | Any       |
| `/auth/signup/lecturer`        | _GET_  | Creation of lecturers account                 | `Bearer Access-Token`  | Admin     |
| `/auth/logout`                 | _POST_ | LogOut User and revoke access/refresh tokens  | `Bearer Access-Token`  | Any       |
| `/auth/password-reset-request` | _POST_ | Request for password reset                    | `None`                 | Any       |
| `/auth/password-reset/{token}` | _POST_ | Reset password                                | `None`                 | Any       |

<div style="margin-top:20px; margin-bottom:10px; font-size:20px; font-weight:bold;">Student EndPoint</div>

| ROUTE                                       | METHOD   | DESCRIPTION                                          | AUTHORIZATION         | USER TYPE         |
|---------------------------------------------|----------|------------------------------------------------------| --------------------- |-------------------|
| `/students/`                                | _GET_    | Get all Students                                     | `Bearer Access-Token` | Admin             |
| `/students/studentcourse/score/{course_id}` | _PUT_    | Update a student course score by the course lecturer | `Bearer Access-Token` | Lecturer          |
| `/students/{student_id}`                    | _GET_    | Get a student by ID                                  | `Bearer Access-Token` | Admin or Lecturer |
| `/students/{student_id}`                    | _DELETE_ | Delete a student by ID                               | `Bearer Access-Token` | Admin             |
| `/students/{student_id}`                    | _PUT_    | Update a student by ID                               | `Bearer Access-Token` | Admin or Lecturer |
| `/students/{student_id}/courses`            | _GET_    | Get a student courses by ID                          | `Bearer Access-Token` | Admin or Lecturer |
| `/students/{student_id}/courses/grades`     | _GET_    | Get a student all courses and grades by ID           | `Bearer Access-Token` | Admin or Lecturer |
| `/students/{student_id}/{course_id}/gpa`    | _GET_    | Calculate a Student Course GPA                       | `Bearer Access-Token` | Admin or Lecturer |

<div style="margin-top:20px; margin-bottom:10px; font-size:20px; font-weight:bold;">Course EndPoint</div>

| ROUTE                            | METHOD   | DESCRIPTION                              | AUTHORIZATION         | USER TYPE         |
|----------------------------------|----------|------------------------------------------| --------------------- |-------------------|
| `/courses/`                      | _GET_    | List all courses available               | `Bearer Access-Token` | Any               |
| `/courses/`                      | _POST_   | Create a new course                      | `Bearer Access-Token` | Admin             |
| `/courses/addcourse/{course_id}` | _DELETE_ | Delete a student from a course           | `Bearer Access-Token` | Lecturer          |
| `/courses/addcourse/{course_id}` | _POST_   | Register a student to a course           | `Bearer Access-Token` | Lecturer          |
| `/courses/{course_id}`           | _GET_    | Get a course by ID                       | `Bearer Access-Token` | Any               |
| `/courses/{course_id}`           | _DELETE_ | Delete a course by ID                    | `Bearer Access-Token` | Admin             |
| `/courses/{course_id}/students`  | _GET_    | List all registered students in a course | `Bearer Access-Token` | Admin or lecturer |


---

<!-- Sample Screenshot -->
## Sample

<br />

[![Student Management API Screenshot][student-management-api-screenshot]](https://github.com/Oluwatemmy/Student-Management-API/blob/main/images/Ze_School_Full_Page.png)

<br/>

<p align="right"><a href="#readme-top">back to top</a></p>

---

<!-- License -->
## License

Distributed under the MIT License. See <a href="https://github.com/Ze-Austin/ze-school/blob/main/LICENSE">LICENSE</a> for more information.

<p align="right"><a href="#readme-top">back to top</a></p>

---

<!-- Contact -->
## Contact

You can contact me with my social media handles:

[LinkedIn](https://www.linkedin.com/in/oluwatemmy15) | [Twitter](https://twitter.com/Oluwatemmy15) | [Github](https://github.com/Oluwatemmy) | Email: oluwaseyitemitope456@gmail.com

Project Link: [Student Management API](https://github.com/Oluwatemmy/Student-Management-API)

<p align="right"><a href="#readme-top">back to top</a></p>

---

<!-- Acknowledgements -->
## Acknowledgements

This project was made possible by:

* [AltSchool Africa School of Engineering](https://altschoolafrica.com/schools/engineering)
* [Caleb Emelike](https://github.com/CalebEmelike)

<p align="right"><a href="#readme-top">back to top</a></p>

---

<!-- Markdown Links & Images -->
[contributors-shield]: https://img.shields.io/github/contributors/Oluwatemmy/Student-Management-API.svg?style=for-the-badge
[contributors-url]: https://github.com/Oluwatemmy/Student-Management-API/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Oluwatemmy/Student-Management-API.svg?style=for-the-badge
[forks-url]: https://github.com/Oluwatemmy/Student-Management-API/network/members
[stars-shield]: https://img.shields.io/github/stars/Oluwatemmy/Student-Management-API.svg?style=for-the-badge
[stars-url]: https://github.com/Oluwatemmy/Student-Management-API/stargazers
[issues-shield]: https://img.shields.io/github/issues/Oluwatemmy/Student-Management-API.svg?style=for-the-badge
[issues-url]: https://github.com/Oluwatemmy/Student-Management-API/issues
[license-shield]: https://img.shields.io/github/license/Oluwatemmy/Student-Management-API.svg?style=for-the-badge
[license-url]: https://github.com/Oluwatemmy/Student-Management-API/blob/main/LICENSE
[twitter-shield]: https://img.shields.io/badge/-@Oluwatemmy15-1ca0f1?style=for-the-badge&logo=twitter&logoColor=white&link=https://twitter.com/ze_austin
[twitter-url]: https://twitter.com/Oluwatemmy15
[student-management-api-screenshot]: https://github.com/Oluwatemmy/Student-Management-API/blob/main/images/Ze_School_Full_Page.png
[python]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[flask]: https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white
[sqlite]: https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white