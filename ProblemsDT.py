
import requests
import pandas as pd
import io
from datetime import datetime

DYNATRACE_URL = "https://bom85898.live.dynatrace.com"
API_TOKEN = "dt0c01.MLCDC5UUMCEFRCCSJ3XKFMS3.VEYSFCORQYMCJFMP4QOJNM5QVS6NTZLMM6RUF2H542DDWSY7K4MWZMQSJ3MK6WXA"
HEADERS = {
    "Authorization": f"Api-Token {API_TOKEN}"
}

def get_host_ip(host_id):
    url = f"{DYNATRACE_URL}/api/v2/entities/{host_id}"
    res = requests.get(url, headers=HEADERS)
    if res.ok:
        return res.json().get("properties", {}).get("ipAddress")
    return None

def main():
    url = f"{DYNATRACE_URL}/api/v2/problems"
    params = {
        "pageSize": 10,
        "from": "now-1d",
        "to": "now",
        "problemSelector": 'status("open")'
    }

    res = requests.get(url, headers=HEADERS, params=params)
    if not res.ok:
        return pd.DataFrame()

    problems = res.json().get("problems", [])
    
    rows = []
    for p in problems:
        for e in p.get("affectedEntities", []):
            if e.get("entityId", {}).get("type") == "HOST":
                host_id = e["entityId"]["id"]
                ip = get_host_ip(host_id)
                if isinstance(ip, list):
                    ip_str = ip[0] if ip else "N/A"
                else:
                    ip_str = ip if ip else "N/A"
                
                rows.append([
                    p.get("displayId"),
                    p.get("title"),
                    p.get("status"),
                    p.get("severityLevel"),
                    datetime.fromtimestamp(p.get("startTime") / 1000).strftime('%Y-%m-%d %H:%M:%S'),
                    host_id,
                    ip_str
                ])

    df = pd.DataFrame(rows, columns=[
        "Problem ID", "Title", "Status", "Severity", "Start Time", "Host ID", "IP Address"
    ])
    df.to_csv("dynatrace_problems.csv", index=False)
    print(f"Data saved total rows {len(df)} rows")
    
    return df

if __name__ == '__main__':
    df = main()
