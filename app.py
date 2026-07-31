from flask import Flask, render_template, request, redirect
from datetime import datetime
from dateutil.relativedelta import relativedelta
from db import get_db_connection
import os

app = Flask(__name__)

try:
    from db import init_db
    init_db()
except Exception as e:
    print(e)

# ==========================
# データベース接続
# ==========================



# ==========================
# 共通処理
# ==========================

def calculate_days(start_date, end_date):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    return (end - start).days + 1


def create_transportation_data(row):

    item = dict(row)

    days = calculate_days(
        item["start_date"],
        item["end_date"]
    )

    item["days"] = days
    item["total"] = days * item["fare"]

    return item


# ==========================
# 一覧
# ==========================

@app.route("/")
def index():

    name = request.args.get("name", "")
    month = request.args.get("month", "")

    # 過去12か月分のプルダウン
    today = datetime.today()
    months = []

    for i in range(12):
        d = today - relativedelta(months=i)

        months.append({
            "value": d.strftime("%Y-%m"),
            "label": d.strftime("%Y年%-m月")
        })

    with get_db_connection() as conn:

        if name and month:

            rows = conn.execute("""

                SELECT *

                FROM transportation

                WHERE name=%s
                AND month=%s

                ORDER BY start_date DESC,id DESC

            """, (name, month)).fetchall()

        else:

            rows = []

    transportation_list = [
        create_transportation_data(row)
        for row in rows
    ]

    total_amount = sum(item["total"] for item in transportation_list)
    total_days = sum(item["days"] for item in transportation_list)
    total_count = len(transportation_list)

    return render_template(

        "index.html",

        transportation_list=transportation_list,

        total_amount=total_amount,
        total_days=total_days,
        total_count=total_count,

        name=name,
        month=month,
        months=months

    )


# ==========================
# 登録
# ==========================

@app.route("/add", methods=["POST"])
def add():

    updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    name = request.form["name"]
    month = request.form["month"]

    with get_db_connection() as conn:

        conn.execute("""

            INSERT INTO transportation(

                name,
                month,
                start_date,
                end_date,
                departure,
                destination,
                transport,
                trip_type,
                fare,
                updated_at

            )

            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)

        """, (

            name,
            month,
            request.form["start_date"],
            request.form["end_date"],
            request.form["departure"],
            request.form["destination"],
            request.form["transport"],
            request.form["trip_type"],
            request.form["fare"],
            updated_at

        ))

        conn.commit()

    return redirect(f"/?name={name}&month={month}")

# ==========================
# 編集画面
# ==========================

@app.route("/edit/<int:id>")
def edit(id):

    with get_db_connection() as conn:

        transportation = conn.execute("""

            SELECT *

            FROM transportation

            WHERE id=%s

        """, (id,)).fetchone()

    return render_template(
        "edit.html",
        transportation=transportation
    )


# ==========================
# 更新
# ==========================

@app.route("/update/<int:id>", methods=["POST"])
def update(id):

    updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    name = request.form["name"]
    month = request.form["month"]

    with get_db_connection() as conn:

        conn.execute("""

            UPDATE transportation

            SET
              start_date=%s,
              end_date=%s,
              departure=%s,
              destination=%s,
              transport=%s,
              trip_type=%s,
              fare=%s,
              updated_at=%s

            WHERE id=%s

        """, (

            request.form["start_date"],
            request.form["end_date"],
            request.form["departure"],
            request.form["destination"],
            request.form["transport"],
            request.form["trip_type"],
            request.form["fare"],
            updated_at,
            id

        ))

        conn.commit()

    return redirect(f"/?name={name}&month={month}")


# ==========================
# 削除
# ==========================

@app.route("/delete/<int:id>")
def delete(id):

    with get_db_connection() as conn:

        transportation = conn.execute("""

            SELECT
                name,
                month

            FROM transportation

            WHERE id=%s

        """, (id,)).fetchone()

        conn.execute("""

            DELETE FROM transportation

            WHERE id=%s

        """, (id,))

        conn.commit()

    return redirect(
        f"/?name={transportation['name']}&month={transportation['month']}"
    )


# ==========================
# 提出
# ==========================

@app.route("/submit", methods=["POST"])
def submit():

    name = request.form["name"]
    month = request.form["month"]

    submitted_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with get_db_connection() as conn:

        conn.execute("""

            INSERT INTO submissions (
    name,
    month,
    submitted_at
)
VALUES (%s, %s, %s)

ON CONFLICT(name, month)
DO UPDATE SET
submitted_at = EXCLUDED.submitted_at

        """, (

            name,
            month,
            submitted_at

        ))

        conn.commit()

    return redirect(f"/?name={name}&month={month}")

# ==========================
# 管理画面
# ==========================

@app.route("/admin")
def admin():

    month = request.args.get("month", "")

    # 対象月プルダウン
    today = datetime.today()
    months = []

    for i in range(12):
        d = today - relativedelta(months=i)

        months.append({
            "value": d.strftime("%Y-%m"),
            "label": d.strftime("%Y年%-m月")
        })

    with get_db_connection() as conn:

        if month:

            rows = conn.execute("""

                SELECT

                    s.name,
                    s.month,
                    s.submitted_at,

                    MAX(t.updated_at) AS updated_at

                FROM submissions s

                LEFT JOIN transportation t

                    ON s.name=t.name
                    AND s.month=t.month

                WHERE s.month=%s

                GROUP BY

                    s.name,
                    s.month,
                    s.submitted_at

                ORDER BY

                    s.name

            """, (month,)).fetchall()

        else:

            rows = conn.execute("""

                SELECT

                    s.name,
                    s.month,
                    s.submitted_at,

                    MAX(t.updated_at) AS updated_at

                FROM submissions s

                LEFT JOIN transportation t

                    ON s.name=t.name
                    AND s.month=t.month

                GROUP BY

                    s.name,
                    s.month,
                    s.submitted_at

                ORDER BY

                    s.month DESC,
                    s.name

            """).fetchall()

    return render_template(

        "admin.html",

        rows=rows,
        month=month,
        months=months

    )

# ==========================
# 提出内容詳細
# ==========================

@app.route("/detail/<name>/<month>")
def detail(name, month):

    with get_db_connection() as conn:

        rows = conn.execute("""

            SELECT *

            FROM transportation

            WHERE
                name=%s
            AND
                month=%s

            ORDER BY start_date

        """, (name, month)).fetchall()

    transportation_list = [
        create_transportation_data(row)
        for row in rows
    ]

    total_amount = sum(item["total"] for item in transportation_list)

    return render_template(

        "detail.html",

        name=name,
        month=month,

        transportation_list=transportation_list,

        total_amount=total_amount

    )

# ==========================
# 起動
# ==========================

from db import get_db_connection, init_db

if __name__ == "__main__":

    init_db()

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )