<h1>DMS</h1>

Remember to set a data-folder for the postgres volume to mount!

<i>More information coming..</i>

Run tests:
```
./test.sh $(pwd)
```
Run composed:
```
./rb.sh
```

Post curl example:
```
curl -X POST -H "Content-Type: text/plain" --data "<DATA>" -u <USERNAME>:<PASSWORD> <URL>/app/<APP_NAME>
```