
import math

from flask import Flask, render_template, request

app = Flask(__name__)


def convert_point_to_letter(point):
    if point >= 8.5:
        return "A"
    elif point >= 7.0:
        return "B"
    elif point >= 5.5:
        return "C"
    elif point >= 4.0:
        return "D"
    else:
        return "F"


def calc_point(cc, gk, ck):
    return round(cc * 0.1 + gk * 0.3 + ck * 0.6, 1)


@app.route("/tinh-diem-hoc-phan", methods=["GET", "POST"])
def tinh_diem_hoc_phan():
    if request.method == "GET":
        return render_template(
            "diem_hoc_phan.html",
            diem_chu=None,
            diem_so=None,
            error=None
        )

    cc_input = request.form.get("cc", "").strip()
    gk_input = request.form.get("gk", "").strip()
    ck_input = request.form.get("ck", "").strip()

    if not cc_input or not gk_input or not ck_input:
        error = "Lỗi: vui lòng nhập đầy đủ điểm."
        return render_template(
            "diem_hoc_phan.html",
            diem_chu=None,
            diem_so=None,
            error=error
        )

    try:
        cc = float(cc_input.replace(",", "."))
        gk = float(gk_input.replace(",", "."))
        ck = float(ck_input.replace(",", "."))
    except ValueError:
        error = "Lỗi: vui lòng nhập điểm hợp lệ."
        return render_template(
            "diem_hoc_phan.html",
            diem_chu=None,
            diem_so=None,
            error=error
        )

    if not all(math.isfinite(x) for x in (cc, gk, ck)):
        error = "Lỗi: vui lòng nhập điểm hợp lệ."
        return render_template(
            "diem_hoc_phan.html",
            diem_chu=None,
            diem_so=None,
            error=error
        )

    if cc < 0 or cc > 10 or gk < 0 or gk > 10 or ck < 0 or ck > 10:
        error = "Lỗi: vui lòng nhập điểm từ 0 đến 10."
        return render_template(
            "diem_hoc_phan.html",
            diem_chu=None,
            diem_so=None,
            error=error
        )

    diem_so = calc_point(cc, gk, ck)
    diem_chu = convert_point_to_letter(diem_so)

    return render_template(
        "diem_hoc_phan.html",
        diem_chu=diem_chu,
        diem_so=diem_so,
        error=None
    )


if __name__ == "__main__":
    app.run(debug=True)
