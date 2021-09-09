import os
import hashlib
from flask import Flask, request, send_from_directory
workDir = os.path.dirname((os.path.abspath(__file__)))      #Корневая дирректория
app = Flask(__name__)


def hashname(filename):                                     #Функция хэширования SHA256
    return hashlib.sha256(filename.encode()).hexdigest()

@app.route('/',methods=['POST'])                            #Получаем запрос на загрузку файла с главной
def upload():
    if request.method == 'POST':
        file = request.files['file']
        fname = hashname(file.filename)                     #Хэшируем имя файла и создаем дирректорию при необходимости
        if not os.path.exists(os.path.join(workDir,'store')):
            os.mkdir(os.path.join(workDir,'store'))                 
        if not os.path.exists(os.path.join(workDir,'store',fname[:2])):
            os.mkdir(os.path.join(workDir,'store',fname[:2]))
        file.save(os.path.join(workDir,'store',fname[:2],fname))    #Наконец сохраняем файл на сервер
        return fname                                        #Возвращаем пользователю хэшированное имя файла
    return 'That should not happen...'

@app.get('/<name>')                                         #Запрос на загрузку файла
def dowloand(name):
    try:
        return send_from_directory(os.path.join(workDir,'store',name[:2]),name,as_attachment=True)
    except:
        return "NO SUCH FILE"                               #Если файла нет, то возращаем сообщения что такого файла нет

@app.delete('/<name>')                                      #Удаление файла с сервера
def delete(name):
    try:
        os.remove(os.path.join(workDir,'store',name[:2],name))
        return 'FILE REMOVED'
    except:
        return 'NO SUCH FILE'