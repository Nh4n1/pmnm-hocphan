import datetime
from math import ceil

from flask import Flask, abort, render_template, request

app = Flask(__name__)


SHOP={
    "name": "Cà phê Trung Nguyên",
    "address": "Số 1, đường ABC, quận XYZ, TP.HCM",
    "open": 7,
    "close": 22
}

PROMOTIONS=[
    "Giảm 10% cho khách hàng thân thiết",
    "Mua 2 tặng 1 vào thứ hai"
]
# PROMOTIONS=[]

@app.route('/home')
def home():
    gio=request.args.get('gio', default=9, type=int)
    if gio is None:
        gio=datetime.now().hour
    
    is_open = SHOP['open'] <= gio < SHOP['close']
    return render_template('home.html',shop=SHOP, promotions=PROMOTIONS, is_open=is_open)



MENU = [
    {"name": "cà phê sữa", "price": 20000, "available": True},
    {"name": "cà phê đen", "price": 15000, "available": True},
    {"name": "bạc xỉu", "price": 25000, "available": False},
    {"name": "trà sữa", "price": 30000, "available": True},
    {"name": "nước cam", "price": 20000, "available": True},
]


@app.template_filter("vnd")
def vnd(value):
    return f"{value:,.0f}".replace(",", ".") + " đ"


@app.route("/menu")
def menu():
    per_page = 3

    page_value = request.args.get("page", "1")

    try:
        page = int(page_value)
    except ValueError:
        abort(404)

    total_dishes = len(MENU)
    pages = ceil(total_dishes / per_page)

    if page < 1 or page > pages:
        abort(404)

    start = (page - 1) * per_page
    end = start + per_page

    current_menu = MENU[start:end]

    average_price = (
        sum(item["price"] for item in MENU) / total_dishes
        if total_dishes > 0
        else 0
    )

    available_count = sum(
        1 for item in MENU if item["available"]
    )

    return render_template(
        "menu.html",
        menu=current_menu,
        page=page,
        pages=pages,
        total_dishes=total_dishes,
        average_price=average_price,
        available_count=available_count
    )

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

if __name__ == '__main__':
    app.run(debug=True)