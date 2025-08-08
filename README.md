# KanMind

KanMind is the backend for the KanMind-Project. The Frontend is provided by the Developer Akademie.
You can find the Frontend here:
https://github.com/Developer-Akademie-Backendkurs/project.KanMind

KanMind is a Tool to simplify and structurize workflows.

## Installation

Clone the repository to your computer via git bash.

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY
```

## Usage
Open the Project in your Code editor and open the Terminal for the project. Then follow these steps:

```python
#Install the dependencies
pip install -r requirements.txt

#Start the virtual environment
.\env\Scripts\Activate

#Start the backend
python manage.py runserver
```

To use this project without the Frontend you need to have software like Postman.

## Creating a user
Here you can create a user (only POST-Method allowed):
localhost/api/registration/

To registrate your request Body should look like this:
```bash
{
 "fullname": "John Doe",
 "email": "john@doe.de",
 "password": "example",
 "repeated_password": "example"
}
```

After creation you can get your Authtoken here:
localhost/api/login/

To login your request body should look like this:
```bash
{
 "email": "john@doe.de",
 "password": "example"
}
```
You will receive a Response from the backend containing your data. Copy the authtoken.

## Authentication
In the Header of your request add your authtoken as value.

## Boards
The boards hold all kind of information like the title of the project and how many tasks and members are part of each board.

Via the Endpoint localhost/api/boards/ you can use the GET-Method to get a List of all boards where you, the user, are either a member or the owner.

Using the POST-Method on the same Endpoint will create a board. To create a board you must be authenticated and your request body needs to look like this:
```bash
{
 "title": "New project",
 "members:[
   2,
   3
 ]
}
```
The members-key hold the id's of the members you want to add to your board. If you don't want to add members to the board you may leave it empty.


The next Endpoint allows the GET, PATCH and the DELETE-Method for requests:
localhost/api/boards/{board_id}/

A GET-request will return detailed information of the board with the given id. You need to be the owner or member of the board with the given id to use the GET-Method.

To use the PATCH-Method you also need to be registered as either the owner or the members of the board. This Endpoint is only meant to update the title or the members of the board.
The request-body should look like this:
```bash
{
 "title": "new title",
 "members": [
  1,
  3
 ]
}
```

You may delete a board via the DELETE-Method, however you need to be the owner of the board to do so.

## Email Check
Endpoint: localhost/api/email-check/

To check for a mail just enter the mail at the end of the Endpoint-url, e.g. localhost/api/email-check/?email=john@doe.de
This allows you to see if an email is already in use. You need to be authenticated to use this.

## Tasks
Here you can check Tasks which you are assigned to or where you are the reviewer. You can also create or edit new tasks.

Here you can create a new Task. You must be a member of the board to do so:

Method: POST

Endpoint: localhost/api/tasks/

request body:
```bash
{
 "board": 12, #id of the board you want to assign the task to
 "title": "Code-Review",
 "description": "Review the new code that was added yesterday",
 "status": "to-do", #you may choose between to-do, in-progress, review, done
 "priority": "high", #you may choose between low, medium, high
 "assignee_id": 4, #must be a member of the board
 "reviewer_id": 1, #must be a member of the board
 "due_date": "2026-01-29"
}
```

Update or delete an existing task:

Method: PATCH, DELETE

Permissions: To PATCH you need to be a member of the board that the task is part of. To DELETE you must be the task creator or the board owner.

Endpoint: localhost/api/tasks/{task_id}/

Request body (for PATCH):
```bash
{
 "title": "Refactoring",
 "description": "Refactor the new code that was approved today",
 "status": "done", #you may choose between to-do, in-progress, review, done
 "priority": "low", #you may choose between low, medium, high
 "assignee_id": 2, #must be a member of the board
 "reviewer_id": 2, #must be a member of the board
 "due_date": "2026-02-01" #yyyy-mm-dd
}
```

### Adding a comment to a task
Method: POST

Permissions: To add a comment to a task you need to be a member of the board that the task is part of.

Endpoint: localhost/api/tasks/{task_id}/comments/

Request body:
```bash
{
 "content": "This works just fine"
}
```

### Fetching all comments of a task
Method: GET

Permissions: To add a comment to a task you need to be a member of the board that the task is part of.

Endpoint: localhost/api/tasks/{task_id}/comments/

### Deleting a comment
Method: DELETE

Permissions: Only the creator of the comment can delete it.

Endpoint: localhost/api/tasks/{task_id}/comments/{comment_id}

### Fetching all tasks that are assigned to me
Method: GET

Permissions: You must be authenticated to use this method.

Endpoint: localhost/api/tasks/assigned-to-me/

### Fetching all tasks that im the reviewer of
Method: GET

Permissions: You must be authenticated to use this method.

Endpoint: localhost/api/tasks/reviewing/

## Contributing

It is not intended to contribute to this repository.
