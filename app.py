from flask import Flask, render_template, request, redirect, url_for,g,jsonify
import sqlite3

app = Flask(__name__)

DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/search', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        word = request.form['word']
        return redirect(url_for('search', word=word))
    return render_template('index.html')

# @app.route('/create', methods=['GET', 'POST'])
# def create():
#     if request.method == 'POST':
#         sentence = request.form['sentence']
#         try:
#             with get_db() as con:
#                 cur = con.cursor()
#                 # 確保你的 SQL 語句是正確的
#                 cur.execute('INSERT INTO english (sentence) VALUES (?)', (sentence,))
#                 con.commit()

#             # AJAX 請求的成功響應
#             return jsonify({'status': 'success', 'message': 'Sentence added successfully!'})
#         except Exception as e:
#             # 錯誤處理
#             return jsonify({'status': 'error', 'message': str(e)}), 500

#     # GET 請求時返回頁面
#     return render_template('create.html')

@app.route('/search/<word>')
def search(word):
    with sqlite3.connect('database.db') as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        # 注意：這裡的 LIKE 語句是大小寫敏感的
        cur.execute("SELECT sentence FROM english WHERE sentence LIKE ?", ('%' + word + '%',))
        sentences = [row['sentence'].replace(word, f'<span class="highlight">{word}</span>') for row in cur.fetchall()]
    return render_template('search.html', sentences=sentences, word=word)


if __name__ == '__main__':
    app.run(debug=True)
