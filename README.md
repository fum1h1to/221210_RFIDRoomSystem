# RFIDRoomSystem

# How To
## server側の起動
1. サーバのディレクトリへ移動<br>
    ```
    cd server
    ```

2. 仮想環境の構築<br>
    ```
    $ python -m venv venv
    $ venv ./venv/Scripts/activate
    ```

2. モジュールのインストール<br>
    ```
    pip install -r requirements.txt
    ```

3. データベースの準備<br>
    ※データベースがinstance配下にすでにある場合は対応不可
    ```
    $ python
    >>> from server import app
    >>> from server import db
    >>> with app.app_context():
    ...    db.create_all()
    >>> exit()

    ```
4. サーバの起動<br>
    ```
    python server.py
    ```

# Note
ファイル構成
```
RFIDRoomSystem<br>
├─m5stack： M5Stack関連のソースコードを格納
└─server： Webサーバ関連のソースコードを格納
    └─instance
        └─db.sqlite3： 取得したログやタグの情報を保持
```