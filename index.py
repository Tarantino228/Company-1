from flask import Flask, Response, redirect, url_for, request
import mysql.connector

app = Flask(__name__)

# Конфигурация базы данных
db_config = {
    'host': '127.0.1.28',
    'user': 'root',
    'password': '',
    'database': 'furniture_manufacturing'
}

# Главная страница
@app.route('/')
def index():
    html = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8" />
        <title>Мебельная Компания</title>
        <style>
            body {{
                margin: 0;
                font-family: 'Candara', sans-serif;
                background-color: #FFFFFF;
                color: #000;
            }}
            .header {{
                display: flex;
                align-items: center;
                padding: 20px;
                background-color: #FFFFFF;
            }}
            .logo {{
                height: 60px;
                width: auto;
            }}
            h1 {{
                margin-left: 20px;
                font-size: 2em;
            }}
            .buttons-container {{
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: calc(100vh - 100px);
                background-color: #D2DFFF;
            }}
            .button {{
                padding: 15px 30px;
                margin: 15px;
                font-size: 1.2em;
                background-color: #355CBD;
                color: #fff;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                width: 350px;
                text-align: center;
                text-decoration: none;
            }}
            .button:hover {{
                background-color: #2E4FAF;
                transform: scale(1.05);
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <img src="{url_for('static', filename='logo.png')}" alt="Логотип" class="logo" />
            <h1>Мебельная Компания</h1>
        </div>
        <div class="buttons-container">
            <a href="{url_for('show_products')}" class="button">Просмотр списка продукции</a>
            <a href="{url_for('add_product')}" class="button">Добавить новую продукцию</a>
            <a href="{url_for('show_workshops')}" class="button">Просмотр списка цехов для производства продукции</a>
            <a href="{url_for('calculate_time')}" class="button">Расчет времени изготовления</a>
        </div>
    </body>
    </html>
    """
    return Response(html, content_type='text/html')

# Остальной код остается без изменений...

# Страница отображения списка продукции
@app.route('/products')
def show_products():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Produkts")
    products = cursor.fetchall()
    cursor.close()
    conn.close()

    items_html = ""
    for product in products:
        items_html += f"""
        <div class="product-box">
            <h3>№ {product['id']}</h3>
            <p><strong>Тип продукции:</strong> {product['Tip_produkciji']}</p>
            <p><strong>Название:</strong> {product['Naimenovanie_produkciji']}</p>
            <p><strong>Арт:</strong> {product['Artikyl']}</p>
            <p><strong>Минимальная стоимость:</strong> {product['Minimalnaya_stoimost']}</p>
            <p><strong>Основной материал:</strong> {product['Osnovnoy_material']}</p>
            <a href="{url_for('edit_product', product_id=product['id'])}">Редактировать</a>
        </div>
        """

    html = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8" />
        <title>Список продукции</title>
        <style>
            body {{
                margin: 0;
                font-family: 'Candara', sans-serif;
                background-color: #f0f0f0;
                padding: 20px;
            }}
            h1 {{
                text-align: center;
                margin-bottom: 20px;
            }}
            .products-container {{
                display: flex;
                flex-wrap: wrap;
                gap: 20px;
                justify-content: center;
            }}
            .product-box {{
                background-color: #fff;
                border-radius: 10px;
                padding: 15px;
                width: 250px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                transition: transform 0.2s, box-shadow 0.2s;
            }}
            .product-box:hover {{
                transform: translateY(-5px);
                box-shadow: 0 8px 16px rgba(0,0,0,0.2);
            }}
            h3 {{
                margin-top: 0;
                text-align: center;
            }}
            p {{
                margin: 8px 0;
                font-size: 0.95em;
            }}
            a.back-link {{
                display: inline-block;
                margin-top: 20px;
                text-decoration: none;
                color: #355CBD;
                font-weight: bold;
            }}
            a.back-link:hover {{
                text-decoration: underline;
            }}
        </style>
    </head>
    <body>
        <h1>Список продукции</h1>
        <div class="products-container">
            {items_html}
        </div>
        <div style="text-align:center;">
            <a href="{url_for('index')}" class="back-link">Вернуться на главную</a>
        </div>
    </body>
    </html>
    """
    return Response(html, content_type='text/html')

# Страница редактирования продукта
@app.route('/edit/<int:product_id>', methods=['GET'])
def edit_product(product_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Produkts WHERE id = %s", (product_id,))
    product = cursor.fetchone()
    cursor.close()
    conn.close()

    if not product:
        return "Продукт не найден", 404

    html = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8" />
        <title>Редактировать продукт № {product['id']}</title>
        <style>
            body {{
                font-family: 'Candara', sans-serif;
                background-color: #f9f9f9;
                padding: 20px;
            }}
            form {{
                max-width: 600px;
                margin: auto;
                background: #fff;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }}
            label {{
                display: block;
                margin-top: 10px;
                font-weight: bold;
            }}
            input[type="text"], input[type="number"] {{
                width: 100%;
                padding: 8px;
                margin-top: 5px;
                border-radius: 4px;
                border: 1px solid #ccc;
            }}
            button {{
                margin-top: 20px;
                padding: 10px 20px;
                background-color: #355CBD;
                color: #fff;
                border: none;
                border-radius: 8px;
                cursor: pointer;
            }}
            button:hover {{
                background-color: #2E4FAF;
            }}
            a.back-link {{
                display: inline-block;
                margin-top: 20px;
                text-decoration: none;
                color: #555;
            }}
            a.back-link:hover {{
                text-decoration: underline;
            }}
        </style>
    </head>
    <body>
        <h2>Редактировать продукт № {product['id']}</h2>
        <form method="POST" action="{url_for('save_product')}">
            <input type="hidden" name="id" value="{product['id']}"/>
            <label>Тип продукции:</label>
            <input type="text" name="Tip_produkciji" value="{product['Tip_produkciji']}"/>

            <label>Название:</label>
            <input type="text" name="Naimenovanie_produkciji" value="{product['Naimenovanie_produkciji']}"/>

            <label>Арт:</label>
            <input type="text" name="Artikyl" value="{product['Artikyl']}"/>

            <label>Минимальная стоимость:</label>
            <input type="number" name="Minimalnaya_stoimost" value="{product['Minimalnaya_stoimost']}"/>

            <label>Основной материал:</label>
            <input type="text" name="Osnovnoy_material" value="{product['Osnovnoy_material']}"/>

            <button type="submit">Сохранить</button>
        </form>
        <a href="{url_for('show_products')}" class="back-link">Вернуться к списку продукции</a>
    </body>
    </html>
    """
    return Response(html, content_type='text/html')

# Обработчик сохранения изменений
@app.route('/save', methods=['POST'])
def save_product():
    product_id = int(request.form['id'])
    Tip_produkciji = request.form['Tip_produkciji']
    Naimenovanie_produkciji = request.form['Naimenovanie_produkciji']
    Artikyl = request.form['Artikyl']
    Minimalnaya_stoimost = request.form['Minimalnaya_stoimost']
    Osnovnoy_material = request.form['Osnovnoy_material']

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Produkts SET
            Tip_produkciji = %s,
            Naimenovanie_produkciji = %s,
            Artikyl = %s,
            Minimalnaya_stoimost = %s,
            Osnovnoy_material = %s
        WHERE id = %s
    """, (Tip_produkciji, Naimenovanie_produkciji, Artikyl, Minimalnaya_stoimost, Osnovnoy_material, product_id))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('show_products'))

# Страница добавления новой продукции
@app.route('/add', methods=['GET'])
def add_product():
    html = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8" />
        <title>Добавить новую продукцию</title>
        <style>
            body {{
                font-family: 'Candara', sans-serif;
                background-color: #f9f9f9;
                padding: 20px;
            }}
            form {{
                max-width: 600px;
                margin: auto;
                background: #fff;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }}
            label {{
                display: block;
                margin-top: 10px;
                font-weight: bold;
            }}
            input[type="text"], input[type="number"] {{
                width: 100%;
                padding: 8px;
                margin-top: 5px;
                border-radius: 4px;
                border: 1px solid #ccc;
            }}
            button {{
                margin-top: 20px;
                padding: 10px 20px;
                background-color: #355CBD;
                color: #fff;
                border: none;
                border-radius: 8px;
                cursor: pointer;
            }}
            button:hover {{
                background-color: #2E4FAF;
            }}
            a.back-link {{
                display: inline-block;
                margin-top: 20px;
                text-decoration: none;
                color: #555;
            }}
            a.back-link:hover {{
                text-decoration: underline;
            }}
        </style>
    </head>
    <body>
        <h2>Добавить новую продукцию</h2>
        <form method="POST" action="{url_for('insert_product')}">
            <label>Тип продукции:</label>
            <input type="text" name="Tip_produkciji" required/>

            <label>Название:</label>
            <input type="text" name="Naimenovanie_produkciji" required/>

            <label>Арт:</label>
            <input type="text" name="Artikyl" required/>

            <label>Минимальная стоимость:</label>
            <input type="number" name="Minimalnaya_stoimost" required/>

            <label>Основной материал:</label>
            <input type="text" name="Osnovnoy_material" required/>

            <button type="submit">Добавить</button>
        </form>
        <a href="{url_for('show_products')}" class="back-link">Вернуться к списку продукции</a>
    </body>
    </html>
    """
    return Response(html, content_type='text/html')

# Обработчик вставки новой продукции
@app.route('/insert', methods=['POST'])
def insert_product():
    Tip_produkciji = request.form['Tip_produkciji']
    Naimenovanie_produkciji = request.form['Naimenovanie_produkciji']
    Artikyl = request.form['Artikyl']
    Minimalnaya_stoimost = request.form['Minimalnaya_stoimost']
    Osnovnoy_material = request.form['Osnovnoy_material']

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Produkts (Tip_produkciji, Naimenovanie_produkciji, Artikyl, Minimalnaya_stoimost, Osnovnoy_material)
        VALUES (%s, %s, %s, %s, %s)
    """, (Tip_produkciji, Naimenovanie_produkciji, Artikyl, Minimalnaya_stoimost, Osnovnoy_material))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('show_products'))

# Страница отображения цехов
@app.route('/workshops')
def show_workshops():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM workshops")
    workshops = cursor.fetchall()
    cursor.close()
    conn.close()

    items_html = ""
    for workshop in workshops:
        items_html += f"""
        <div class="workshop-box">
            <h3>Цех: {workshop['Shop_name']}</h3>
            <p><strong>Тип цеха:</strong> {workshop['Shop_type']}</p>
            <p><strong>Количество сотрудников:</strong> {workshop['Number_of_people']}</p>
        </div>
        """

    html = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8" />
        <title>Цеха производства</title>
        <style>
            body {{
                margin: 0;
                font-family: 'Candara', sans-serif;
                background-color: #f0f0f0;
                padding: 20px;
            }}
            h1 {{
                text-align: center;
                margin-bottom: 20px;
            }}
            .workshops-container {{
                display: flex;
                flex-wrap: wrap;
                gap: 20px;
                justify-content: center;
            }}
            .workshop-box {{
                background-color: #fff;
                border-radius: 10px;
                padding: 15px;
                width: 300px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                transition: transform 0.2s, box-shadow 0.2s;
            }}
            .workshop-box:hover {{
                transform: translateY(-5px);
                box-shadow: 0 8px 16px rgba(0,0,0,0.2);
            }}
            h3 {{
                margin-top: 0;
                text-align: center;
            }}
            p {{
                margin: 8px 0;
                font-size: 0.95em;
            }}
            a.back-link {{
                display: inline-block;
                margin-top: 20px;
                text-decoration: none;
                color: #355CBD;
                font-weight: bold;
            }}
            a.back-link:hover {{
                text-decoration: underline;
            }}
        </style>
    </head>
    <body>
        <h1>Цеха производства</h1>
        <div class="workshops-container">
            {items_html}
        </div>
        <div style="text-align:center;">
            <a href="{url_for('index')}" class="back-link">Вернуться на главную</a>
        </div>
    </body>
    </html>
    """
    return Response(html, content_type='text/html')

# --- Новая часть: расчет времени изготовления продукции ---

@app.route('/calculate_time', methods=['GET', 'POST'])
def calculate_time():
    if request.method == 'GET':
        # форма выбора продукта
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT Product_Name FROM Product")
        products = cursor.fetchall()
        cursor.close()
        conn.close()

        options_html = ""
        for p in products:
            options_html += f'<option value="{p["Product_Name"]}">{p["Product_Name"]}</option>'

        html_form = f"""
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8" />
            <title>Расчет времени изготовления продукции</title>
            <style>
                body {{
                    font-family: 'Candara', sans-serif;
                    background-color: #f9f9f9;
                    padding: 20px;
                }}
                form {{
                    max-width: 500px;
                    margin: auto;
                    background: #fff;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                }}
                label {{
                    display: block;
                    margin-top: 10px;
                    font-weight: bold;
                }}
                select, input[type="number"] {{
                    width: 100%;
                    padding: 8px;
                    margin-top: 5px;
                    border-radius: 4px;
                    border: 1px solid #ccc;
                }}
                button {{
                    margin-top: 20px;
                    padding: 10px 20px;
                    background-color: #355CBD;
                    color: #fff;
                    border: none;
                    border-radius: 8px;
                    cursor: pointer;
                }}
                button:hover {{
                    background-color: #2E4FAF;
                }}
            </style>
        </head>
        <body>
            <h2>Расчет времени изготовления продукции</h2>
            <form method="POST" action="{url_for('calculate_time')}">
                <label>Выберите продукт:</label>
                <select name="product_name" required>
                    {options_html}
                </select>
                <label>Количество единиц:</label>
                <input type="number" name="quantity" min="1" value="1" required />
                <button type="submit">Рассчитать</button>
            </form>
            <div style="text-align:center; margin-top:20px;">
                <a href="{url_for('index')}">Вернуться на главную</a>
            </div>
        </body>
        </html>
        """
        return Response(html_form, content_type='text/html')
    else:
        # обработка POST-запроса
        product_name = request.form['product_name']
        quantity = int(request.form['quantity'])

        # Получить сумму Preparation_Time_h по всем цехам для выбранного продукта
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT SUM(Preparation_Time_h) AS total_time FROM `Product` WHERE Product_Name = %s",
            (product_name,)
        )
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        # Время на один продукт
        single_product_time = result['total_time'] if result['total_time'] else 0
        # Общее время, округленное до целого и неотрицательное
        total_hours = max(0, int(round(single_product_time * quantity)))

        # вывод результата
        html_result = f"""
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8" />
            <title>Результат расчета</title>
            <style>
                body {{
                    font-family: 'Candara', sans-serif;
                    background-color: #f9f9f9;
                    padding: 20px;
                }}
                .result-box {{
                    max-width: 600px;
                    margin: auto;
                    background: #fff;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                    text-align: center;
                }}
                h2 {{
                    margin-top: 0;
                }}
                a {{
                    display: inline-block;
                    margin-top: 20px;
                    text-decoration: none;
                    color: #355CBD;
                }}
                a:hover {{
                    text-decoration: underline;
                }}
            </style>
        </head>
        <body>
            <div class="result-box">
                <h2>Общее время изготовления</h2>
                <p>Для {quantity} единиц(ы): <strong>{total_hours} часов</strong></p>
                <a href="{url_for('calculate_time')}">Рассчитать еще раз</a><br>
                <a href="{url_for('index')}">На главную</a>
            </div>
        </body>
        </html>
        """
        return Response(html_result, content_type='text/html')

if __name__ == '__main__':
    app.run(debug=True)