from app import create_app

# ✅ Gunicorn expects a callable function, not an instance
def app():
    return create_app()


# if __name__ == "__main__":
#     app.run(debug=True)
