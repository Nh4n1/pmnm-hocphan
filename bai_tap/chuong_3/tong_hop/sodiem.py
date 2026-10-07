import csv
import io

from flask import (
    Flask,
    abort,
    jsonify,
    make_response,
    redirect,
    request,
    url_for,
)
from markupsafe import escape

app = Flask(__name__)
app.json.ensure_ascii = False


STUDENTS = {
    "23T1020001": {
        "name": "Nguyễn Văn An",
        "lop": "K47A",
        "scores": {
            "PMMNM": 8.5,
            "CSDL": 7.0,
            "MMT": 9.0,
        },
    },
    "23T1020002": {
        "name": "Trần Thị Bình",
        "lop": "K47A",
        "scores": {
            "PMMNM": 6.0,
            "CSDL": 5.5,
            "MMT": 7.0,
        },
    },
    "23T1020003": {
        "name": "Lê Hoàng Cường",
        "lop": "K47B",
        "scores": {
            "PMMNM": 9.5,
            "CSDL": 9.0,
        },
    },
    "23T1020004": {
        "name": "Phạm Minh Dũng",
        "lop": "K47B",
        "scores": {
            "PMMNM": 4.0,
            "CSDL": 3.5,
            "MMT": 5.0,
        },
    },
    "23T1020005": {
        "name": "Hoàng Thu Hà",
        "lop": "K47A",
        "scores": {},
    },
    "23T1020006": {
        "name": "Võ Quốc Khánh",
        "lop": "K47C",
        "scores": {
            "PMMNM": 7.5,
            "MMT": 8.0,
        },
    },
}

def average(scores):
    if not scores:
        return None

    return round(
        sum(scores.values()) / len(scores),
        2,
    )

def rank(avg):
    if avg is None:
        return "Chưa có điểm"

    if avg >= 8.5:
        return "Giỏi"

    if avg >= 7:
        return "Khá"

    if avg >= 5:
        return "Trung bình"

    return "Yếu"

def student_summary(mssv):
    if mssv not in STUDENTS:
        abort(
            404,
            description=(
                f"Không có sinh viên với MSSV = {mssv}."
            ),
        )

    student = STUDENTS[mssv]
    avg = average(student["scores"])

    return {
        "mssv": mssv,
        "name": student["name"],
        "lop": student["lop"],
        "scores": student["scores"],
        "average": avg,
        "rank": rank(avg),
    }
    
def layout(title, body):
    return f"""<!doctype html>
<html lang="vi">
<head>
    <meta charset="utf-8">
    <title>{escape(title)} - Sổ điểm</title>
</head>
<body>
    <nav>
        <a href="{escape(url_for('home'))}">Trang chủ</a> |
        <a href="{escape(url_for('student_list'))}">Sinh viên</a> |
        <a href="{escape(url_for('search'))}">Tìm kiếm</a>
    </nav>

    <hr>

    {body}
</body>
</html>
"""

def student_table(items):
    if not items:
        return "<p>Không có sinh viên phù hợp.</p>"

    rows = ""

    for item in items:
        avg = item["average"]

        avg_text = (
            "—"
            if avg is None
            else f"{avg:.2f}"
        )

        href = url_for(
            "student_detail",
            mssv=item["mssv"],
        )

        rows += f"""
<tr>
    <td>
        <a href="{escape(href)}">
            {escape(item["mssv"])}
        </a>
    </td>
    <td>{escape(item["name"])}</td>
    <td>{escape(item["lop"])}</td>
    <td>{escape(avg_text)}</td>
    <td>{escape(item["rank"])}</td>
</tr>
"""

    return f"""
<table border="1" cellpadding="8">
    <thead>
        <tr>
            <th>MSSV</th>
            <th>Họ tên</th>
            <th>Lớp</th>
            <th>Điểm TB</th>
            <th>Xếp loại</th>
        </tr>
    </thead>
    <tbody>
        {rows}
    </tbody>
</table>
"""


@app.route("/")
def home():
    classes = {student["lop"] for student in STUDENTS.values()}
    body =f"""
<p>Tổng số sinh viên: {escape(len(STUDENTS))}</p>
<p>Số lớp: {escape(len(classes))}</p>

<p>
    <a href="{escape(url_for('student_list'))}">
        Xem danh sách sinh viên
    </a>
</p>

<p>
    <a href="{escape(url_for('api_student_list'))}">
        Xem API sinh viên
    </a>
</p>
"""

    return layout("Trang chủ", body)

@app.route("/students")
def student_list():
    lop = request.args.get("lop", "")

    classes = sorted({
        student["lop"]
        for student in STUDENTS.values()
    })

    items = [
        student_summary(mssv)
        for mssv, student in STUDENTS.items()
        if (
            not lop
            or student["lop"].casefold() == lop.casefold()
        )
    ]

    links = [
        (
            f'<a href="{escape(url_for("student_list"))}">'
            "Tất cả"
            "</a>"
        )
    ]

    for class_name in classes:
        href = url_for(
            "student_list",
            lop=class_name,
        )

        links.append(
            f'<a href="{escape(href)}">'
            f"{escape(class_name)}"
            "</a>"
        )

    body = "<h1>Danh sách sinh viên</h1>"
    body += "<p>" + " | ".join(links) + "</p>"
    body += student_table(items)

    return layout("Sinh viên", body)


@app.route("/students/<mssv>")
def student_detail(mssv):
    item = student_summary(mssv)

    avg = item["average"]

    avg_text = (
        "—"
        if avg is None
        else f"{avg:.2f}"
    )

    class_url = url_for(
        "student_list",
        lop=item["lop"],
    )

    export_url = url_for(
        "student_export",
        mssv=mssv,
    )

    short_url = url_for(
        "student_short",
        mssv=mssv,
    )

    rows = ""

    for course, score in item["scores"].items():
        rows += f"""
<tr>
    <td>{escape(course)}</td>
    <td>{escape(score)}</td>
</tr>
"""

    if not rows:
        rows = """
<tr>
    <td colspan="2">Chưa có điểm.</td>
</tr>
"""

    body = f"""
<h1>{escape(item["name"])}</h1>

<p>MSSV: {escape(mssv)}</p>

<p>
    Lớp:
    <a href="{escape(class_url)}">
        {escape(item["lop"])}
    </a>
</p>

<p>Điểm TB: {escape(avg_text)}</p>
<p>Xếp loại: {escape(item["rank"])}</p>

<table border="1" cellpadding="8">
    <tr>
        <th>Học phần</th>
        <th>Điểm</th>
    </tr>
    {rows}
</table>

<p>
    <a href="{escape(export_url)}">
        Tải bảng điểm (CSV)
    </a>
</p>

<p>
    Link rút gọn:
    <a href="{escape(short_url)}">
        {escape(short_url)}
    </a>
</p>
"""

    return layout("Chi tiết sinh viên", body)


@app.route("/sv/<mssv>")
def student_short(mssv):
    return redirect(
        url_for(
            "student_detail",
            mssv=mssv,
        ),
        code=301,
    )


@app.route("/students/<mssv>/export")
def student_export(mssv):
    item = student_summary(mssv)

    buffer = io.StringIO()
    writer = csv.writer(buffer)

    writer.writerow(["hoc_phan", "diem"])

    for course, score in item["scores"].items():
        writer.writerow([course, score])

    response = make_response(buffer.getvalue())

    response.headers["Content-Type"] = (
        "text/csv; charset=utf-8"
    )

    response.headers["Content-Disposition"] = (
        f"attachment; filename=diem_{mssv}.csv"
    )

    return response


@app.route("/search")
def search():
    q = request.args.get("q", "")
    keyword = q.casefold()

    results = [
        student_summary(mssv)
        for mssv, student in STUDENTS.items()
        if (
            keyword in student["name"].casefold()
            or keyword in mssv.casefold()
        )
    ]

    links = ""

    for item in results:
        href = url_for(
            "student_detail",
            mssv=item["mssv"],
        )

        links += f"""
<li>
    <a href="{escape(href)}">
        {escape(item["mssv"])} — {escape(item["name"])}
    </a>
</li>
"""

    body = f"""
<h1>Tìm kiếm sinh viên</h1>

<form method="get" action="{escape(url_for('search'))}">
    <input name="q" value="{escape(q)}">
    <button type="submit">Tìm kiếm</button>
</form>

<p>
    Tìm thấy {escape(len(results))} kết quả
    cho “{escape(q)}”.
</p>

<ul>
    {links}
</ul>
"""

    return layout("Tìm kiếm", body)

@app.route("/api/students")
def api_student_list():
    lop = request.args.get("lop", "")
    min_avg = None

    if "min_avg" in request.args:
        min_avg = request.args.get(
            "min_avg",
            type=float,
        )

        if min_avg is None:
            abort(
                400,
                description="min_avg phải là một số.",
            )

    results = [
        student_summary(mssv)
        for mssv, student in STUDENTS.items()
        if (
            not lop
            or student["lop"].casefold() == lop.casefold()
        )
    ]

    if min_avg is not None:
        results = [
            item
            for item in results
            if (
                item["average"] is not None
                and item["average"] >= min_avg
            )
        ]

    return jsonify(results)


@app.route("/api/students/<mssv>")
def api_student_detail(mssv):
    return jsonify(student_summary(mssv))

@app.route(
    "/api/students/<mssv>/scores/<course>",
    methods=["GET", "PUT", "DELETE"],
)
def student_score(mssv, course):
    item = student_summary(mssv)

    scores = item["scores"]
    course = course.upper()

    if request.method == "PUT":
        score = request.args.get(
            "score",
            type=float,
        )

        if score is None or not (0 <= score <= 10):
            abort(
                400,
                description="Điểm phải là số từ 0 đến 10.",
            )

        created = course not in scores
        scores[course] = score

        data = {
            "mssv": mssv,
            "course": course,
            "score": score,
            "average": average(scores),
        }

        if created:
            return jsonify(data), 201, {
                "Location": url_for(
                    "student_score",
                    mssv=mssv,
                    course=course,
                )
            }

        return jsonify(data), 200

    if course not in scores:
        abort(
            404,
            description=(
                f"Chưa có điểm học phần {course}."
            ),
        )

    if request.method == "DELETE":
        del scores[course]
        return "", 204

    return jsonify({
        "mssv": mssv,
        "course": course,
        "score": scores[course],
    })
    
@app.errorhandler(400)
@app.errorhandler(404)
@app.errorhandler(405)
def handle_error(error):
    titles = {
        400: "Dữ liệu không hợp lệ",
        404: "Không tìm thấy",
        405: "Phương thức không được hỗ trợ",
    }

    code = error.code
    title = titles[code]

    if request.path.startswith("/api/"):
        return jsonify({
            "error": title,
            "detail": error.description,
        }), code

    body = f"""
<h1>{escape(code)} — {escape(title)}</h1>
<p>{escape(error.description)}</p>
"""

    return layout(title, body), code

if __name__ == '__main__':
    app.run(debug=True)
    
    