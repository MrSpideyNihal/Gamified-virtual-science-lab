import json
import os

USER_DATA_FILE = "user_data.json"

def load_all_users():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as file:
            return json.load(file)
    else:
        return {}  

def save_all_users(users):
    with open(USER_DATA_FILE, "w") as file:
        json.dump(users, file, indent=4)

def get_user_data(name):
    users = load_all_users()
    return users.get(name, {"badges": []})  

def save_user_data(name, user_data):
    users = load_all_users()
    users[name] = user_data
    save_all_users(users)

def award_badge(name, badge_name):
    users = load_all_users()
    
    if name not in users:
        users[name] = {"badges": []}
    
    if badge_name not in users[name]["badges"]:
        users[name]["badges"].append(badge_name)
        save_all_users(users)
        print(f"🎉 Congratulations, {name}! You earned the '{badge_name}' badge!")
    else:
        print(f"✅ {name} already has the '{badge_name}' badge.")
