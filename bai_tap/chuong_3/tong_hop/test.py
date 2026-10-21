from flask import Flask, request

app = Flask(__name__)

@app.route('/search')
def search():
    # URL: /search?q=python
    query = request.args.get('q')

    # Đặt giá trị mặc định nếu không truyền tham số (URL: /search)
    page = request.args.get('page', default=1)

    # Ép kiểu dữ liệu (tự động chuyển sang int, nếu lỗi sẽ dùng default)
    limit = request.args.get('limit', default=10, type=int)

    return f"Query: {query}, Page: {page}, Limit: {limit}"


if __name__ == '__main__':
    app.run(debug=True)