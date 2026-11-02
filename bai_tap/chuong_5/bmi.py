import math

from flask import Flask, render_template, request

app = Flask(__name__)

height_accepted = [50, 250]
weight_accepted = [10, 300]


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
            result_class=None
        )

    # Lấy dữ liệu từ form
    height_value = request.form.get("height", "").strip()
    weight_value = request.form.get("weight", "").strip()

    height_error = None
    weight_error = None
    bmi = None
    category = None
    result_class = None

    height = None
    weight = None

    # Kiểm tra chiều cao
    if not height_value:
        height_error = "Vui lòng nhập chiều cao."
    else:
        try:
            height = float(height_value.replace(",", "."))

            if not math.isfinite(height):
                height_error = "Vui lòng nhập một số hợp lệ."
            elif height < height_accepted[0] or height > height_accepted[1]:
                height_error = (
                    f"Chiều cao phải từ {height_accepted[0]} "
                    f"đến {height_accepted[1]} cm."
                )
        except ValueError:
            height_error = "Vui lòng nhập một số."

    # Kiểm tra cân nặng
    if not weight_value:
        weight_error = "Vui lòng nhập cân nặng."
    else:
        try:
            weight = float(weight_value.replace(",", "."))

            if not math.isfinite(weight):
                weight_error = "Vui lòng nhập một số hợp lệ."
            elif weight < weight_accepted[0] or weight > weight_accepted[1]:
                weight_error = (
                    f"Cân nặng phải từ {weight_accepted[0]} "
                    f"đến {weight_accepted[1]} kg."
                )
        except ValueError:
            weight_error = "Vui lòng nhập một số."

    # Chỉ tính BMI khi cả hai dữ liệu hợp lệ
    if height_error is None and weight_error is None:
        height_m = height / 100
        bmi = round(weight / (height_m ** 2), 2)

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
        result_class=result_class
    )


if __name__ == "__main__":
    app.run(debug=True)
