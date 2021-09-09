Так же проект размещен на Python Anywhere, так что можно потестировать его на сервере =)

http://danilchechkov.pythonanywhere.com/

Для выгрузки файла на сервер:

curl -F "file=@test.txt" http://127.0.0.1:5000/

curl -F "file=@test.txt" http://danilchechkov.pythonanywhere.com/


Для скачивания файла:

curl -X GET http://127.0.0.1:5000/{YOUR HASH}

Или перейти по ссылке http://127.0.0.1:5000/{YOUR HASH}

curl -X GET http://danilchechkov.pythonanywhere.com/{YOUR HASH}

Или перейти по ссылке http://danilchechkov.pythonanywhere.com/{YOUR HASH}


Для удаления файла

curl -X DELETE http://127.0.0.1:5000/{YOUR HASH}

curl -X DELETE http://danilchechkov.pythonanywhere.com/{YOUR HASH}

Для запуска устанавливаем venv


pip install flask

export FLASK_APP=test1.py

export FLASK_ENV=development

flask run