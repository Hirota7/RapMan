from flask import Flask, render_template, request, redirect, url_for
from app.models import db, Memo 
from dotenv import load_dotenv
import os
from uuid import UUID
from datetime import datetime

# .envファイルを読み込む
load_dotenv()

# 環境変数からデータベース接続情報を取得
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')

app = Flask(__name__)

# SQLAlchemy設定
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.before_request
def create_tables():
    db.create_all()

# メモ一覧を表示
@app.route('/')
def index():
    memos = Memo.query.order_by(Memo.created_at.desc()).all()
    return render_template('index.html', memos=memos)


# メモの詳細を表示
@app.route('/memo/<uuid:memo_id>')
def view_memo(memo_id):
    memo = Memo.query.get_or_404(str(memo_id))
    return render_template('view_memo.html', memo=memo)



# 新しいメモの作成フォームを表示
@app.route('/create', methods=['GET'])
def show_create_memo():
    return render_template('create_memo.html')

# 新しいメモを作成
@app.route('/create', methods=['GET', 'POST'])
def create_memo():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        priority = request.form['priority']
        
        
        # デバッグ用: 送信されたpriorityを確認
        print(f"Priority: {priority}")
        
        new_memo = Memo(title=title, content=content, priority=priority)
        db.session.add(new_memo)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('create_memo.html')







# メモを削除
# ===============================
# エンドポイント /memo/(メモのID)/delete
# メソッド　　POST
# 返すもの　index.html (リダイレクト)
# ===============================
@app.route('/memo/<uuid:memo_id>/delete', methods=['POST'])
def delete_memo(memo_id):
    memo = Memo.query.get_or_404(str(memo_id))
    db.session.delete(memo)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
