from flask import Flask, render_template, request, redirect
from supabase import create_client
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Connect to Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

app = Flask(__name__)


# Home page
@app.route("/", methods=["GET", "POST"])
def home():

    # Add a new task
    if request.method == "POST":

        task = request.form["task"]

        supabase.table("tasks").insert({
            "task": task,
            "completed": False
        }).execute()

        return redirect("/")

    # Get all tasks
    response = supabase.table("tasks").select("*").order(
        "created_at", desc=True
    ).execute()

    tasks = response.data

    return render_template("index.html", tasks=tasks)


# Complete / uncomplete a task
@app.route("/complete/<int:task_id>", methods=["POST"])
def complete_task(task_id):

    # Get the current task
    response = supabase.table("tasks").select(
        "completed"
    ).eq("id", task_id).single().execute()

    current_status = response.data["completed"]

    # Change true → false or false → true
    supabase.table("tasks").update({
        "completed": not current_status
    }).eq("id", task_id).execute()

    return redirect("/")


# Delete a task
@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):

    supabase.table("tasks").delete().eq(
        "id", task_id
    ).execute()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)