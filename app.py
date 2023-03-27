from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('books.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    conn = get_db_connection()
    books = conn.execute('SELECT * FROM books').fetchall()
    conn.close()
    return render_template('index.html', books=books)


@app.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        read = request.form.get('read') == 'on'
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO books (book_title, book_author, already_read) VALUES (?, ?, ?)', (title, author, read))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/edit', methods=('GET', 'POST'))
def edit():
    conn = get_db_connection()
    if request.method == 'POST':
        id = request.form['id']
        title = request.form['title']
        author = request.form['author']
        read = request.form.get('read') == 'on'
        conn.execute(
            'UPDATE books SET book_title = ?, book_author = ?, already_read = ? WHERE id = ?', (title, author, read, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    books = conn.execute('SELECT * FROM books').fetchall()
    conn.close()
    return render_template('edit.html', books=books)


@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM books WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


@app.route('/borrowed', methods=('GET', 'POST'))
def borrowed():
    conn = get_db_connection()
    if request.method == 'POST':
        id = request.form['id']
        borrowed = request.form.get('borrowed') == 'on'
        conn.execute(
            'UPDATE borrowed_books SET borrowed = ? WHERE id = ?', (borrowed, id))
        conn.commit()
    books = conn.execute('SELECT * FROM books').fetchall()
    borrowed_books = conn.execute('SELECT * FROM borrowed_books').fetchall()
    conn.close()
    return render_template('borrowed.html', books=books, borrowed_books=borrowed_books)


if __name__ == '__main__':
    app.run()
