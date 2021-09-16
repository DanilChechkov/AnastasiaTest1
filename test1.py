import os
import hashlib
import shutil
from flask import Flask, request, send_from_directory, render_template
from flask.helpers import url_for
from werkzeug.utils import redirect
workDir = os.path.dirname((os.path.abspath(__file__)))      #Корневая дирректория
app = Flask(__name__,template_folder='template')

def hashname(file):                                     #Функция хэширования SHA256
    return hashlib(file.read()).hexdigest()


@app.route('/',methods=['POST','GET'])                            #Получаем запрос на загрузку файла с главной
def upload():
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            file.save(os.path.join(workDir,'tmp'))
            fname = file.filename
            with open(os.path.join(workDir,'tmp'),'rb') as f:
                fname = hashname(f)                         #Хэшируем файл и создаем дирректорию при необходимости
                if not os.path.exists(os.path.join(workDir,'store')):
                    os.mkdir(os.path.join(workDir,'store'))                 
                if not os.path.exists(os.path.join(workDir,'store',fname[:2])):
                    os.mkdir(os.path.join(workDir,'store',fname[:2]))
            shutil.move(os.path.join(workDir,'tmp'),os.path.join(workDir,'store',fname[:2],fname))    #Наконец сохраняем файл на сервер
            return fname, {'Content-Type': 'text/html'}                                        #Возвращаем пользователю хэшированное имя файла
        elif 'name' in request.values:
            print(request.values)
            return redirect(url_for('download', name=request.values['name']))
        elif 'delete' in request.values:
            try:
                os.remove(os.path.join(workDir,'store',request.values['delete'][:2],request.values['delete']))
                return 'FILE REMOVED'
            except:
                return 'NO SUCH FILE'
        else:
            return render_template('index.html')
    else:
        return render_template('index.html')

@app.get('/<name>')                                         #Запрос на загрузку файла
def download(name):
    try:
        return send_from_directory(os.path.join(workDir,'store',name[:2]),name,as_attachment=True)
    except:
        return "NO SUCH FILE"                              #Если файла нет, то возращаем сообщения что такого файла нет

@app.delete('/<name>')                                      #Удаление файла с сервера
def delete(name):
    try:
        os.remove(os.path.join(workDir,'store',name[:2],name))
        return 'FILE REMOVED'
    except:
        return 'NO SUCH FILE'