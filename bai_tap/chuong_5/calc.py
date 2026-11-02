
import math

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/calculator", methods=["GET", "POST"])
def calculator():
    if request.method == "GET":
        return render_template(
            "calculator.html",
            a="",
            b="",
            operation="add",
            result=None,
            error=None
        )

    a_input = request.form.get("a", "").strip()
    b_input = request.form.get("b", "").strip()
    operation = request.form.get("operation", "").strip()

    a = None
    b = None
    result = None
    error = None

    valid_operations = ["add", "subtract", "multiply", "divide"]

    if operation not in valid_operations:
        error = "Lỗi: phép toán không hợp lệ."
    elif not a_input and not b_input:
        error = "Lỗi cả hai ô: vui lòng nhập lại."
    else:
        if not a_input:
            error = "Lỗi ô a: vui lòng nhập lại."
        else:
            try:
                a = float(a_input.replace(",", "."))
                if not math.isfinite(a):
                    error = "Lỗi ô a: vui lòng nhập lại."
            except ValueError:
                error = "Lỗi ô a: vui lòng nhập lại."

        if error is None:
            if not b_input:
                error = "Lỗi ô b: vui lòng nhập lại."
            else:
                try:
                    b = float(b_input.replace(",", "."))
                    if not math.isfinite(b):
                        error = "Lỗi ô b: vui lòng nhập lại."
                except ValueError:
                    error = "Lỗi ô b: vui lòng nhập lại."

    if error is None and operation == "divide" and b == 0:
        error = "Lỗi ô b: không thể chia cho không."

    if error is None:
        if operation == "add":
            result = a + b
        elif operation == "subtract":
            result = a - b
        elif operation == "multiply":
            result = a * b
        elif operation == "divide":
            result = a / b

    return render_template(
        "calculator.html",
        a=a_input,
        b=b_input,
        operation=operation,
        result=result,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)
