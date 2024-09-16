# Product management

This is a small application for managing products.

## Requirements

- Python 3.12
- Docker

## Endpoints and Authentication

There is a Postman collection in the repository root so you can explore all the endpoints available.

It uses OAuth 2.0 for handling user authentication and basic endpoint security.

Grant type used: **Authorization Code Flow with Proof Key for Code Exchange (PKCE)**. This is the grant type recommended
for a scenario with a `user <-> frontend app <-> backend app` schema.

- `/api/products` endpoints **require user authentication only**.
- `/api/users` endpoints **require user authentication plus admin role**.
    - admin status is handled by setting `is_staff` field.
- `/o/authorize` and `/o/token/` endpoints allow handling of user authentication.

## Get started

In the following guide, we assume that we are working in the default local environment (http://127.0.0.1:8000).

1. Create a virtual environment: `python3.12 -m venv .venv`
2. Activate it: `source .venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Run migrations: `python manage.py migrate`
5. Create superuser: `python manage.py createsuperuser`
    - username: admin
    - email address: admin@example.com
    - password: 1234
6. Run server: `python manage.py runserver`
7. Configure Client App
    1. Go to http://127.0.0.1:8000/admin/ and login as superuser
    2. Django OAuth Toolkit -> Applications -> ADD APPLICATION
    3. Save `Client id` for later.
    4. Save `Client secret` for later.
    5. Set `Redirect uris` to `http://127.0.0.1:8000/` and save it for later.
    6. Set `Client type` to `Public`
    7. Set `Authorization grant type` to `Authorization code`
    8. Check `Skip authorization`
    9. Save
8. Authenticate ourselves into the API.
    1. Since we do not have a frontend app and to simplify the process, we need to be logged in
       at http://127.0.0.1:8000/admin/.
    2. Generate a Code Verifier and a Code Challenge at https://tonyxu-io.github.io/pkce-generator/ and save them for
       later.
    3. In the same browser where you logged in at http://127.0.0.1:8000/admin/, go to
       `http://127.0.0.1:8000/o/authorize?client_id=EYlpjccPGkcSrpxJWuMWsRAhEDAiqEHAJHklznEz&response_type=code&redirect_uri=http://127.0.0.1:8000/&scope=read write&code_challenge=J4NzDMb_PMmc2Vu25zsGcbv-Ezmun5qXxbwI9JztYVU&code_challenge_method=S256`
       with the following values:
       1. client_id=\[YOUR CLIENT ID\] 
       2. response_type=code 
       3. redirect_url=\[YOUR REDIRECT URI\] 
       4. scope=read write 
       5. code_challenge=\[YOUR CODE CHALLENGE\] 
       6. code_challenge_method=S256
    4. You will be redirected to http://127.0.0.1:8000. Copy the value of the query string `code` that is shown in the URL and save it for next step.
    5. Invoke the endpoint `http://127.0.0.1:8000/o/token/` in the Postman collection replacing the values saved in previous steps.
       (client_id, code, redirect_uri, code_verifier, scope).
    6. You will get a response with this form:
       1. ```json
          {
            "access_token": "lzosRF6uh60gu75bdH7BngBPr192qV",
            "expires_in": 3600,
            "token_type": "Bearer",
            "scope": "read write",
            "refresh_token": "6eQmI6r7Lwc1Qs6PNxKWvglTUn9phR"
          }
          ```
       2. Save the previous response.
       3. Go to the Postman collection settings -> tab `Variables` -> set the `access_token` to `lzosRF6uh60gu75bdH7BngBPr192qV` (only for this example).
9. Now you can play with the remaining endpoints.
10. You can use the postman refresh token request when needed.

## Containerization

File `Dockerfile` contains the Docker image definition of the app.

## Continuous deployment

The file `.github/workflows/on-push-to-main.yaml` deploys a new Dockerized App version on Render on every push to main branch.

The app is deployed at https://product-management-latest.onrender.com (it may take a few minutes to start after first request)

## Pending things

- Cover functionality with tests.
- Remove dev mode to be fully ready for production
- Replace sqlite connection by same type as production (e.g. Postrgres)
