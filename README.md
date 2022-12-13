# RFIDRoomSystem

# how to
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
    ```
    $ python
    >>> from app import app
    >>> from app import db
    >>> with app.app_context():
    ...    db.create_all()
    >>> exit()

    ```
4. サーバの起動<br>
    ```
    python server.py
    ```