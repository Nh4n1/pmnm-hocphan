from flask import Flask, Response, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import  String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


TEXT = {"Content-Type": "text/plain; charset=utf-8"}

class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

app = Flask(__name__)

app.config["SECRET_KEY"] = "dev-chi-dung-khi-phat-trien-phan-mem"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///qlsv.db"

db.init_app(app)


class SinhVien(db.Model):
    __tablename__ = "sinh_vien"

    id: Mapped[int] = mapped_column(primary_key=True)
    mssv: Mapped[str] = mapped_column(String(10), unique=True)
    name: Mapped[str] = mapped_column(String(100))
    gpa: Mapped[float] = mapped_column(default=0.0)

    def __repr__(self):
        return f"<Student {self.mssv} - {self.name}>"


with app.app_context():
    db.create_all()


@app.get("/them-mau")
def app_sample():
    total = db.session.scalar(db.select(func.count(SinhVien.id)))
    if total > 0:
        return f"Da co du lieu {total} ban khong the them du lieu mau"
    an = SinhVien(mssv="23T102001", name="Nguyen Van An", gpa=3.5)
    before = an.id
    db.session.add(an)
    db.session.commit()
    db.session.add_all([
        SinhVien(mssv="23T102002", name="Tran Thi B", gpa=3.8),
        SinhVien(mssv="23T102003", name="Le Van C", gpa=2.9),
        SinhVien(mssv="23T102004", name="Pham Thi D", gpa=3.2),
        SinhVien(mssv="23T102005", name="Hoang Van E", gpa=3.0),
    ])
    db.session.commit()
    return (f"Da them 5 sinh vien, id cua An: "
            f"{before} - truoc commit, "
            f" - sau commit = {an.id}")
    
@app.route("/thu-truy-van")
def try_queries():
    if db.session.scalar(db.select(func.count(SinhVien.id))) == 0:
        return "Chua co du lieu, vui long truy cap /them-mau de them du lieu mau"
    lines =[]
    lines.append(f"1, get(3): {db.session.get(SinhVien, 3)}")
    lines.append(f"2, get(99): {db.session.get(SinhVien, 99)}")
    
    everyone = db.session.execute(db.select(SinhVien)).scalars().all()
    lines.append(f"3, select all: {everyone}")
    stmt=(db.select(SinhVien).where(SinhVien.gpa > 3.0).order_by(SinhVien.gpa.desc()))
    good_students = db.session.execute(stmt).scalars().all()
    lines.append(f"4, select where gpa > 3.0: {good_students}")
    binh=db.session.scalar(db.select(SinhVien).filter_by(mssv="23T102002"))    
    lines.append(f"5, filter by mssv='23T102002': {binh}")
    count = db.session.scalar(db.select(func.count(SinhVien.id)))
    avg= db.session.scalar(db.select(func.avg(SinhVien.gpa)))
    lines.append(f"6, So luong sinh vien: {count}, diem trung binh: {avg}")
    return "\n".join(lines), TEXT

@app.route("/thu-truy-van-moi")
def try_new_queries():
    if db.session.scalar(db.select(func.count(SinhVien.id))) == 0:
        return "Chua co du lieu, vui long truy cap /them-mau de them du lieu mau"

    lines = []

    lines.append(f"1, get(3): {db.session.get(SinhVien, 3)}")
    lines.append(f"2, get(99): {db.session.get(SinhVien, 99)}")

    everyone = db.session.execute(
        db.select(SinhVien)
    ).scalars().all()

    lines.append(f"3, select all: {everyone}")

    stmt = (
        db.select(SinhVien)
        .where(SinhVien.gpa > 3.0)
        .order_by(SinhVien.gpa.desc())
    )

    good_students = db.session.execute(stmt).scalars().all()
    lines.append(f"4, select where gpa > 3.0: {good_students}")

    binh = db.session.scalar(
        db.select(SinhVien).filter_by(mssv="23T102002")
    )

    lines.append(f"5, filter by mssv='23T102002': {binh}")

    count = db.session.scalar(db.select(func.count(SinhVien.id)))
    avg = db.session.scalar(db.select(func.avg(SinhVien.gpa)))

    lines.append(f"6, So luong sinh vien: {count}, diem trung binh: {avg}")
    

    return render_template("queries.html", lines=lines,everyone= everyone)


if __name__ == "__main__":
    app.run(debug=True)