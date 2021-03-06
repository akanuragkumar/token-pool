# Token Pool API
This app can generate and assign random tokens within a pool and release them after some time.

## Approach
My initial appoach was to write a cron job that runs each second and updates expiry and refresh time of all the tokens in the pool. But soon realized that it is not a scalable approach.

Then I came up with this logic where we can actually limit the logic in API Layer itself and this making it more scalable approach.
Few things which I ccould add if time was not a constraint- 
1. Transaction lock so that raise conditions would not happen.
2. Write a cron job which runs every 1 hour or according to the scale which cleans up the tokens which have expired.

## Quickstart

To work in a sandboxed Python environment it is recommended to install the app in a Python [virtualenv](https://pypi.python.org/pypi/virtualenv).

1. Clone and install dependencies

    ```bash
    $ git clone https://github.com/akanuragkumar/token-pool.git
    $ cd token-pool
    $ pip install -r requirements.txt
    ```   
2. Running app

   ```bash
   $ manage.py makemigrations 
   $ python manage.py migrate
   $ python manage.py runserver
   ``` 
   
 3. Running unit test cases.
 The unit test cases are written in pool/tests.py

   ```bash
   $ python manage.py test
   ``` 
   
## API Documentation 

### `Endpoint to generate unique token in the pool` 

1. `POST /api/token_pool/` 


##### `response`

```json
{
   "token": "token uuid"
}   
```
### `Endpoint to delete the given token from the pool` 
2. `DELETE /api/token_pool/` 

```json
 application/json - {
   "token": "token uuid"
} 
```
##### `response`

```json
{
    "response": "Token deleted successfully"
}
    
```
### `Endpoint to block the available free token from the pool` 

3. `POST api/block_token/` 

##### `response`

```json
 application/json - {
    "blocked_token": "token_uuid"
}
```

### `Endpoint to extend expire time by 5 minutes or if it is blocked then. extend the refresh time by 60 seconds.` 

4. `POST /api/keep_alive/<uuid:token_uuid>` 

##### `response`

```json
{
    "response": "Token refreshed successfully"
} 
```
