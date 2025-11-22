

access database by shell
1. `docker exec -it docker-db-1 /bin/bash`
2. `psql -U postgres`
    - password: `difyai123456`
3. use database `\c dify`

reset admin password
1. `docker exec -it docker-api-1 /bin/bash`
2. `flask reset-password`, and type in your email of admin

