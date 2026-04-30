import sqlite3
import webbrowser
from threading import Timer
from flask import Flask, request, redirect

app = Flask(__name__)


def init_db():
    with sqlite3.connect("kanban.db") as con:
        con.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, txt TEXT, col INTEGER)")


init_db()


@app.route('/')
def index():
    with sqlite3.connect("kanban.db") as con:
        res = con.execute("SELECT * FROM tasks").fetchall()

    cols = {0: '', 1: '', 2: ''}
    for r in res:
        cols[r[2]] += f'''
            <div class="card" draggable="true" ondragstart="event.dataTransfer.setData('id', {r[0]})">
                {r[1]} 
                <a href="/del/{r[0]}" style="color:red; text-decoration:none; float:right; font-weight:bold;">×</a>
            </div>
        '''

    return f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>Канбан Доска</title>
        <style>
            body {{ font-family: 'Segoe UI', sans-serif; background: #f0f2f5; display: flex; flex-direction: column; align-items: center; padding: 20px; }}
            .board {{ display: flex; gap: 15px; width: 900px; }}
            .col {{ flex: 1; background: #ebedf0; border-radius: 10px; padding: 15px; min-height: 500px; box-shadow: inset 0 0 5px rgba(0,0,0,0.05); }}
            .card {{ background: white; padding: 15px; margin-bottom: 12px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); cursor: move; font-size: 14px; }}
            .card:hover {{ border: 1px solid #4a90e2; }}
            .header {{ margin-bottom: 30px; text-align: center; background: white; padding: 20px; border-radius: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }}
            input {{ padding: 10px; border-radius: 6px; border: 1px solid #ddd; width: 250px; outline: none; }}
            button {{ padding: 10px 20px; cursor: pointer; background: #4a90e2; color: white; border: none; border-radius: 6px; font-weight: bold; }}
            button:hover {{ background: #357abd; }}
            b {{ display: block; margin-bottom: 15px; color: #5f6c84; text-align: center; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h2 style="margin-top:0">Канбан доска</h2>
            <form action="/add" method="POST">
                <input name="txt" placeholder="Напиши задачу..." required>
                <button type="submit">Добавить</button>
            </form>
        </div>

        <div class="board">
            <div class="col" ondragover="event.preventDefault()" ondrop="location.href='/move/'+event.dataTransfer.getData('id')+'/0'">
                <b>НУЖНО</b>{cols[0]}
            </div>
            <div class="col" ondragover="event.preventDefault()" ondrop="location.href='/move/'+event.dataTransfer.getData('id')+'/1'">
                <b>В РАБОТЕ</b>{cols[1]}
            </div>
            <div class="col" ondragover="event.preventDefault()" ondrop="location.href='/move/'+event.dataTransfer.getData('id')+'/2'">
                <b>ГОТОВО</b>{cols[2]}
            </div>
        </div>
    </body>
    </html>
    """


@app.route('/add', methods=['POST'])
def add():
    txt = request.form.get('txt')
    with sqlite3.connect("kanban.db") as con:
        con.execute("INSERT INTO tasks (txt, col) VALUES (?, 0)", (txt,))
    return redirect('/')


@app.route('/move/<id>/<col>')
def move(id, col):
    with sqlite3.connect("kanban.db") as con:
        con.execute("UPDATE tasks SET col = ? WHERE id = ?", (col, id))
    return redirect('/')


@app.route('/del/<id>')
def delete(id):
    with sqlite3.connect("kanban.db") as con:
        con.execute("DELETE FROM tasks WHERE id = ?", (id,))
    return redirect('/')


def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")


if __name__ == '__main__':
    Timer(1.5, open_browser).start()
    app.run(port=5000)