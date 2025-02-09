from flask import Flask, render_template, request, redirect, url_for, session
from word_database import get_quiz

app = Flask(__name__)
app.secret_key = "supersecretkey"  # 用于存储会话数据

@app.route("/")
def index():
    # 生成题目并存入 session
    session["quiz"] = get_quiz()
    session["score"] = 0
    session["current_question"] = 0
    return render_template("index.html", question=session["quiz"][0], question_number=1)

@app.route("/next", methods=["POST"])
def next_question():
    user_answer = request.form.get("answer")
    current_question = session["current_question"]
    
    # 检查用户答案
    if user_answer == session["quiz"][current_question]["correct_answer"]:
        session["score"] += 1

    session["current_question"] += 1

    # 如果题目完成，跳转到结果页
    if session["current_question"] >= len(session["quiz"]):
        return redirect(url_for("result"))

    # 否则，继续下一题
    return render_template("index.html", 
                           question=session["quiz"][session["current_question"]], 
                           question_number=session["current_question"] + 1)

@app.route("/result")
def result():
    return render_template("result.html", score=session["score"], total=len(session["quiz"]))

if __name__ == "__main__":
    app.run(debug=True)
