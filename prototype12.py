import webbrowser
import os
import psutil

# Define the URLs for the web apps
urls = {
    "youtube": "https://www.youtube.com",
    "gmail": "https://mail.google.com"
}

# Function to open a web app
def open_web_app(app_name):
    if app_name.lower() in urls:
        webbrowser.open(urls[app_name.lower()])
        print(f"{app_name.capitalize()} is now open.")
    else:
        print(f"No URL found for {app_name}.")

# Function to close a web app (browser)
def close_web_app(browser_name="chrome"):
    browser_name = browser_name.lower()
    browser_processes = {
        "chrome": ["chrome", "chromium"],
        "firefox": ["firefox"],
        "safari": ["safari"],
        "edge": ["msedge"]
    }

    if browser_name not in browser_processes:
        print(f"No known processes for browser: {browser_name}")
        return

    for proc in psutil.process_iter(['name']):
        try:
            proc_name = proc.info['name'].lower()
            if proc_name in browser_processes[browser_name]:
                proc.kill()
                print(f"{proc_name} has been closed.")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

# Example usage
if __name__ == "__main__":
    # Open YouTube
    open_web_app("youtube")

    # Open Gmail
    open_web_app("gmail")

    # Close Chrome browser
    close_web_app("chrome")
