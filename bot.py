import requests
import json
from web3 import Web3
import os
import time
from colorama import init, Fore, Style

init()

BASE_URL = "https://baishi-api.arenavs.com/api/v1"

HEADERS = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "ja,en-US;q=0.9,en;q=0.8",
    "content-type": "application/json",
    "origin": "https://baishi.arenavs.com",
    "priority": "u=1, i",
    "referer": "https://baishi.arenavs.com/",
    "sec-ch-ua": '"Chromium";v="136", "Microsoft Edge";v="136", "Not.A/Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0"
}

def generate_ethereum_account():
    w3 = Web3()
    account = w3.eth.account.create()
    address = account.address
    private_key = account.key.hex()
    return address, private_key

def save_to_json(address, private_key, filename="address.json"):
    data = {
        "address": address,
        "private_key": private_key
    }
    try:
        with open(filename, "a") as f:
            json.dump(data, f, indent=4)
            f.write("\n")
    except Exception as e:
        print(f"{Fore.RED}ファイル {filename} に保存できませんでした：{e}{Style.RESET_ALL}")

def register_user(wallet_address, referral_code):
    url = f"{BASE_URL}/users/initialize"
    payload = {
        "walletAddress": wallet_address,
        "referralCode": referral_code
    }
    try:
        response = requests.post(url, headers=HEADERS, json=payload)
        response.raise_for_status()
        response_data = response.json()
        token = response_data.get("token")
        if not token:
            raise ValueError("トークンを取得できませんでした")
        print(f"{Fore.GREEN}登録が成功しました{Style.RESET_ALL}")
        return token
    except requests.RequestException as e:
        print(f"{Fore.RED}登録に失敗しました：{e}{Style.RESET_ALL}")
        return None
    except ValueError as e:
        print(f"{Fore.RED}トークンを取得できませんでした：{e}{Style.RESET_ALL}")
        return None

def clear_task(token, task_id):
    url = f"{BASE_URL}/tasks/{task_id}/complete/13044"
    headers = HEADERS.copy()
    headers["authorization"] = f"Bearer {token}"
    payload = {}
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        print(f"{Fore.RED}タスク {task_id} に失敗しました：{e}{Style.RESET_ALL}")
        return False

def countdown(seconds):
    for i in range(seconds, -1, -1):
        print(f"{Fore.YELLOW}タスクを処理しています、{i}秒待っています...{Style.RESET_ALL}", end="\r")
        time.sleep(1)
    print(" " * 50, end="\r")

def main():
    print(f"{Fore.YELLOW}╔══════════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}║       🌟 Baishi Bot - Automated Tasks        ║{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}║   Otomatisasi tugas akun Baishi ArenaVS      ║{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}║  Developed by: https://t.me/sentineldiscus   ║{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}╚══════════════════════════════════════════════╝{Style.RESET_ALL}")
    
    referral_code = input("リファラルコードを入力してください：").strip()
    while True:
        try:
            num_requests = int(input("リファラルの数を入力してください："))
            if num_requests <= 0:
                print(f"{Fore.RED}リファラルの数は0より大きくしてください{Style.RESET_ALL}")
                continue
            break
        except ValueError:
            print(f"{Fore.RED}有効な数字を入力してください{Style.RESET_ALL}")
    
    for request_num in range(1, num_requests + 1):
        print(f"{Fore.YELLOW}リファラル {request_num} / {num_requests} を開始します{Style.RESET_ALL}")
        
        wallet_address, private_key = generate_ethereum_account()
        print(f"{Fore.GREEN}新しいアドレスを作成しました{Style.RESET_ALL}")
        
        save_to_json(wallet_address, private_key)
        
        token = register_user(wallet_address, referral_code)
        if not token:
            print(f"{Fore.RED}リファラル {request_num} を中止しました：トークンを取得できませんでした{Style.RESET_ALL}")
            continue
        
        countdown(30)
        task_list = [1, 6, 12, 13, 14, 15, 16]
        for task_id in task_list:
            clear_task(token, task_id)
        
        print(f"{Fore.GREEN}リファラル {request_num} / {num_requests} が完了しました{Style.RESET_ALL}")

if __name__ == "__main__":
    main()