# At the very end of your main.py file, change this:
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# To this:
# This allows Vercel to import the app directly
app = app