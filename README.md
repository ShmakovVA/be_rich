# BeRich

```
Simple money exchange web-service
```

# How to up it?

```
>> make build-init

During building up you'll be asked about superuser credentials
 - please, provide a username which equal to valid email there 
   to be able to log in as system account via GUI.
   (like email=root@g.com and username=root@g.com)

urls for access:
- http://127.0.0.1:8082 - is service GUI 
- http://127.0.0.1:8082/admin/ - is Django admin 
```

# What I have been used:

0. PyCharm IDE

    ```
   It brings us a lot of features and integration-wise things, which
   makes the development more comfortable.
   ``` 

1. Django as a basic framework for implementing backend with REST API

   ```
   Because it most friendly and powerful framework I worked ever.
   It might be a bit overkill for that prototype, but it makes sense 
   in case of service growing.
   ``` 

2. ReactJS for providing frontend GUI using REST API

   ```
   Nowadays, I'm very interested in that library and that direction of 
   frontend development at all. 
   I've just started to learn it, so sorry for frontend implementation :)
   ```

3. Docker-compose + webpack + Makefile for 
building/debugging/running the project inside a Docker container

   ```
   In all my current projects we use it. Kinda 'Must have'.
   Especially I'm excited about Docker <-> PyCharm integration. 
   Makefile saves a lot of time for debugging and other stuff 
   and all it via one entry point
   ```

4. Git as VCS

   ```
   No comments
   ```

5. Prettier and flakes for keeping code clean
    
   ```
   No comments
   ```

6. PostgreSQL DB for storing data

   ```
   It overkill for prototype too.
   But I use it because It's the best choice 
   for high-load and growing web-services.
   ```
   
# What I did not, but I do always.

1. Using multiple branchs like 'epik-...' -> 'dev' -> 'master'
   
   ``` 
   No reason to use it for writing a prototype in several commits.
   ```
    
2. Documentation and docstrings

   ```
   I've saved my time on it :)
   Ofc there are should be two docs: for REST API and rest stuff
   ```
    
3. Unit tests
    
   ```
   The same reason as above 
   (But usually I do strong test coverage for almost each 'pull request') 
   ```
   
4. Configurating for production
    
   ```
   No reason to do it for a test prototype. Many DevOps activities there.
   In my teams, we have DevOps guys for it :) 
   ```
   
5. Sentry, Kibana, New Relic ...

   ```
   Kinda `Must have`-services, but It's too much, again... 
   ```
