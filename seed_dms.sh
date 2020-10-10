curl -X POST -H "Content-Type: text/plain" --data '{"bob": 340, "fu":"bar"}' -u admin:Secret123 0.0.0.0:5000/app/my_app_json
sleep 1
curl -X POST -H "Content-Type: text/plain" --data '{"bob": 240, "fu":"bar"}' -u admin:Secret123 0.0.0.0:5000/app/my_app_json
sleep 1
curl -X POST -H "Content-Type: text/plain" --data '{"bob": 345, "fu":"bar"}' -u admin:Secret123 0.0.0.0:5000/app/my_app_json
sleep 1
curl -X POST -H "Content-Type: text/plain" --data '{"bob": 400, "fu":"bar"}' -u admin:Secret123 0.0.0.0:5000/app/my_app_json
sleep 1
curl -X POST -H "Content-Type: text/plain" --data '{"bob": 390, "fu":"bar"}' -u admin:Secret123 0.0.0.0:5000/app/my_app_json
sleep 1
curl -X POST -H "Content-Type: text/plain" --data '{"bob": 420, "fu":"bar"}' -u admin:Secret123 0.0.0.0:5000/app/my_app_json
sleep 1
curl -X POST -H "Content-Type: text/plain" --data '{"bob": 450, "fu":"bar"}' -u admin:Secret123 0.0.0.0:5000/app/my_app_json
sleep 1
curl -X POST -H "Content-Type: text/plain" --data '{"bob": 400, "fu":"bar"}' -u admin:Secret123 0.0.0.0:5000/app/my_app_json
sleep 1
curl -X POST -H "Content-Type: text/plain" --data '{"bob": 340, "fu":"bar"}' -u admin:Secret123 0.0.0.0:5000/app/my_app_json
sleep 1
curl -X POST -H "Content-Type: text/plain" --data '{"bob": 300, "fu":"bar"}' -u admin:Secret123 0.0.0.0:5000/app/my_app_json
sleep 1
curl -X POST -H "Content-Type: text/plain" --data '{"bob": 240, "fu":"bar"}' -u admin:Secret123 0.0.0.0:5000/app/my_app_json
sleep 1
curl -X POST -H "Content-Type: text/plain" --data '{"bob": 200, "fu":"bar"}' -u admin:Secret123 0.0.0.0:5000/app/my_app_json

curl -X POST -H "Content-Type: text/plain" --data 100 -u admin:Secret123 0.0.0.0:5000/app/my_app_simple
sleep 1
curl -X POST -H "Content-Type: text/plain" --data 150 -u admin:Secret123 0.0.0.0:5000/app/my_app_simple
sleep 1
curl -X POST -H "Content-Type: text/plain" --data 190 -u admin:Secret123 0.0.0.0:5000/app/my_app_simple
sleep 1
curl -X POST -H "Content-Type: text/plain" --data 200 -u admin:Secret123 0.0.0.0:5000/app/my_app_simple
sleep 1
curl -X POST -H "Content-Type: text/plain" --data 250 -u admin:Secret123 0.0.0.0:5000/app/my_app_simple
sleep 1
curl -X POST -H "Content-Type: text/plain" --data 195 -u admin:Secret123 0.0.0.0:5000/app/my_app_simple
sleep 1
curl -X POST -H "Content-Type: text/plain" --data 140 -u admin:Secret123 0.0.0.0:5000/app/my_app_simple
sleep 1
curl -X POST -H "Content-Type: text/plain" --data 100 -u admin:Secret123 0.0.0.0:5000/app/my_app_simple
sleep 1
curl -X POST -H "Content-Type: text/plain" --data 40 -u admin:Secret123 0.0.0.0:5000/app/my_app_simple
sleep 1
curl -X POST -H "Content-Type: text/plain" --data 80 -u admin:Secret123 0.0.0.0:5000/app/my_app_simple
sleep 1

curl -X POST -H "Content-Type: text/plain" --data '{"data_series_var": "bob"}' -u admin:Secret123 0.0.0.0:5000/app/my_app_json/config
