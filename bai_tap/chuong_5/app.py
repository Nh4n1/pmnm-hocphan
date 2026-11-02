import math

from flask import Flask, render_template, request

app = Flask(__name__)

HEIGHT_RANGE_CM = (50, 250)
WEIGHT_RANGE_KG = (10, 300)


def convert_point_to_letter(point):
    if point >= 8.5:
        return "A"
    if point >= 7.0:
        return "B"
    if point >= 5.5:
        return "C"
    if point >= 4.0:
        return "D"
    return "F"


def calculate_course_score(attendance, midterm, final):
    return round(attendance * 0.1 + midterm * 0.3 + final * 0.6, 1)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/calculator", methods=["GET", "POST"])
def calculator():
    if request.method == "GET":
        return render_template(
            "calculator.html",
            a="",
            b="",
            operation="add",
            result=None,
            error=None,
        )

    a_input = request.form.get("a", "").strip()
    b_input = request.form.get("b", "").strip()
    operation = request.form.get("operation", "").strip()

    a = None
    b = None
    result = None
    error = None
    valid_operations = {"add", "subtract", "multiply", "divide"}

    if operation not in valid_operations:
        error = "Lỗi: phép toán không hợp lệ."
    elif not a_input and not b_input:
        error = "Lỗi cả hai ô: vui lòng nhập lại."
    else:
        if not a_input:
            error = "Lỗi ô thứ nhất: vui lòng nhập lại."
        else:
            try:
                a = float(a_input.replace(",", "."))
                if not math.isfinite(a):
                    error = "Lỗi ô thứ nhất: vui lòng nhập lại."
            except ValueError:
                error = "Lỗi ô thứ nhất: vui lòng nhập lại."

        if error is None:
            if not b_input:
                error = "Lỗi ô thứ hai: vui lòng nhập lại."
            else:
                try:
                    b = float(b_input.replace(",", "."))
                    if not math.isfinite(b):
                        error = "Lỗi ô thứ hai: vui lòng nhập lại."
                except ValueError:
                    error = "Lỗi ô thứ hai: vui lòng nhập lại."

    if error is None and operation == "divide" and b == 0:
        error = "Lỗi ô thứ hai: không thể chia cho không."

    if error is None:
        if operation == "add":
            result = a + b
        elif operation == "subtract":
            result = a - b
        elif operation == "multiply":
            result = a * b
        else:
            result = a / b

    return render_template(
        "calculator.html",
        a=a_input,
        b=b_input,
        operation=operation,
        result=result,
        error=error,
    )


@app.route("/tinh-diem-hoc-phan", methods=["GET", "POST"])
def tinh_diem_hoc_phan():
    if request.method == "GET":
        return render_template(
            "diem_hoc_phan.html",
            diem_chu=None,
            diem_so=None,
            error=None,
        )

    score_inputs = {
        "cc": request.form.get("cc", "").strip(),
        "gk": request.form.get("gk", "").strip(),
        "ck": request.form.get("ck", "").strip(),
    }

    if any(not value for value in score_inputs.values()):
        error = "Lỗi: vui lòng nhập đầy đủ điểm."
        return render_template(
            "diem_hoc_phan.html",
            diem_chu=None,
            diem_so=None,
            error=error,
        )

    try:
        attendance, midterm, final = (
            float(value.replace(",", ".")) for value in score_inputs.values()
        )
    except ValueError:
        error = "Lỗi: vui lòng nhập điểm hợp lệ."
        return render_template(
            "diem_hoc_phan.html",
            diem_chu=None,
            diem_so=None,
            error=error,
        )

    scores = (attendance, midterm, final)
    if not all(math.isfinite(score) for score in scores):
        error = "Lỗi: vui lòng nhập điểm hợp lệ."
        return render_template(
            "diem_hoc_phan.html",
            diem_chu=None,
            diem_so=None,
            error=error,
        )

    if any(score < 0 or score > 10 for score in scores):
        error = "Lỗi: vui lòng nhập điểm từ 0 đến 10."
        return render_template(
            "diem_hoc_phan.html",
            diem_chu=None,
            diem_so=None,
            error=error,
        )

    diem_so = calculate_course_score(*scores)
    diem_chu = convert_point_to_letter(diem_so)

    return render_template(
        "diem_hoc_phan.html",
        diem_chu=diem_chu,
        diem_so=diem_so,
        error=None,
    )


@app.route("/bmi-calculator", methods=["GET", "POST"])
def bmi_calculator_route():
    if request.method == "GET":
        return render_template(
            "bmi_calculator.html",
            height_value="",
            weight_value="",
            height_error=None,
            weight_error=None,
            bmi=None,
            category=None,
            result_class=None,
        )

    height_value = request.form.get("height", "").strip()
    weight_value = request.form.get("weight", "").strip()

    height_error = None
    weight_error = None
    height = None
    weight = None
    bmi = None
    category = None
    result_class = None

    if not height_value:
        height_error = "Vui lòng nhập chiều cao."
    else:
        try:
            height = float(height_value.replace(",", "."))
            if not math.isfinite(height):
                height_error = "Vui lòng nhập một số hợp lệ."
            elif not HEIGHT_RANGE_CM[0] <= height <= HEIGHT_RANGE_CM[1]:
                height_error = (
                    f"Chiều cao phải từ {HEIGHT_RANGE_CM[0]} "
                    f"đến {HEIGHT_RANGE_CM[1]} cm."
                )
        except ValueError:
            height_error = "Vui lòng nhập một số."

    if not weight_value:
        weight_error = "Vui lòng nhập cân nặng."
    else:
        try:
            weight = float(weight_value.replace(",", "."))
            if not math.isfinite(weight):
                weight_error = "Vui lòng nhập một số hợp lệ."
            elif not WEIGHT_RANGE_KG[0] <= weight <= WEIGHT_RANGE_KG[1]:
                weight_error = (
                    f"Cân nặng phải từ {WEIGHT_RANGE_KG[0]} "
                    f"đến {WEIGHT_RANGE_KG[1]} kg."
                )
        except ValueError:
            weight_error = "Vui lòng nhập một số."

    if height_error is None and weight_error is None:
        height_m = height / 100
        bmi = round(weight / height_m**2, 2)

        if bmi < 18.5:
            category = "Thiếu cân"
            result_class = "warning"
        elif bmi < 23:
            category = "Bình thường"
            result_class = "success"
        elif bmi < 25:
            category = "Thừa cân"
            result_class = "warning"
        else:
            category = "Béo phì"
            result_class = "danger"

    return render_template(
        "bmi_calculator.html",
        height_value=height_value,
        weight_value=weight_value,
        height_error=height_error,
        weight_error=weight_error,
        bmi=bmi,
        category=category,
        result_class=result_class,
    )


if __name__ == "__main__":
    app.run(debug=True)
