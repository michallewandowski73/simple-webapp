from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session

app = Flask(__name__)

# --- Database setup (SQLite file) ---
DATABASE_URL = "sqlite:///notes.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base = declarative_base()
SessionLocal = scoped_session(sessionmaker(bind=engine))


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=True)


Base.metadata.create_all(bind=engine)


# --- Routes ---
@app.route("/", methods=["GET"])
def index():
    session = SessionLocal()
    notes = session.query(Note).order_by(Note.id.desc()).all()
    session.close()
    return render_template("index.html", notes=notes)


@app.route("/add", methods=["POST"])
def add_note():
    title = request.form.get("title", "").strip()
    content = request.form.get("content", "").strip()

    if title:
        session = SessionLocal()
        note = Note(title=title, content=content)
        session.add(note)
        session.commit()
        session.close()

    return redirect(url_for("index"))


@app.route("/delete/<int:note_id>", methods=["POST"])
def delete_note(note_id):
    session = SessionLocal()
    note = session.query(Note).filter(Note.id == note_id).first()
    if note:
        session.delete(note)
        session.commit()
    session.close()
    return redirect(url_for("index"))


if __name__ == "__main__":
    # Local dev
    print("App started successfully!")
    app.run(debug=True)
