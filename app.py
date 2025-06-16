from flask import Flask, request, render_template, redirect, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'journal_user'
app.config['MYSQL_PASSWORD'] = 'Prasvi'
app.config['MYSQL_DB'] = 'journal_db'

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        content = request.form['content']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO entries (content) VALUES (%s)', (content,))

        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('index'))
    else:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM entries ORDER BY created_at DESC')
        entries = cursor.fetchall()
        cursor.close()
        return render_template('index.html',entries=entries)
        
if __name__ == '__main__':
    app.run(debug=True)
