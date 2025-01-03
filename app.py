import threading
import random
import time
import datetime

# 建立Lock
lock = threading.Lock()

# 肉類數量
meat_count = {"牛肉": 10, "豬肉": 7, "雞肉": 5}

# 處理時間
processing_time = {
    "牛肉": 1,
    "豬肉": 2,
    "雞肉": 3
}

# 員工列表
employees = ['A', 'B', 'C', 'D', 'E']

# 記錄每位員工處理的肉類數量
employee_logs = {employee: {"牛肉": 0, "豬肉": 0, "雞肉": 0} for employee in employees}

# 註冊事件
all_clear = threading.Event()

def get_meat(employee):
    global meat_count, employee_logs
    while not all_clear.is_set():
        with lock:
            # 檢查是否還有肉類可處理
            available_meats = [meat for meat, count in meat_count.items() if count > 0]
            if not available_meats:
                all_clear.set()
                break

            # 隨機選擇肉類
            meat = random.choice(available_meats)
            # 更新肉類數量
            meat_count[meat] -= 1
            # 紀錄員工處理數量
            employee_logs[employee][meat] += 1
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"{employee} 在 {now} 取得 {meat}，剩餘數量：{meat_count[meat]}")

        # 處理時間
        time.sleep(processing_time[meat])

        # 處理完成後的訊息
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{employee} 在 {now} 完成處理 {meat}")

# 創建執行緒
threads = []
for employee in employees:
    t = threading.Thread(target=get_meat, args=(employee,))
    threads.append(t)
    t.start()


# 等待所有執行緒結束
for t in threads:
    t.join()

print("所有員工已經處理完肉類。")
# print員工處理數量
for employee, log in employee_logs.items():
    meat_info = f"{employee} 處理了："
    for meat, count in log.items():
        meat_info += f"{meat} {count} 塊，"
    
    # 去掉最後多餘的逗號
    meat_info = meat_info.rstrip("，")
    
    print(meat_info)
