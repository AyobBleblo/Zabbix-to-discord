from client import ZabbixClint
from config import ZABBIX_URL, ZABBIX_TOKEN
from datetime import datetime

def format_time(timestamp: str) -> str:
    return datetime.fromtimestamp(int(timestamp)).strftime("%Y-%m-%d %H:%M:%S")

def main():

    if not ZABBIX_URL or not ZABBIX_TOKEN:
        raise ValueError("ZABBIX_URL or ZABBIX_TOKEN is not set")

    client = ZabbixClint(ZABBIX_URL, ZABBIX_TOKEN)
    problems = client.get_current_problems()
    if not problems:
        print("No problems found")
        return
    print(f"{len(problems)} problems found")
    for problem in problems:
        
        # print(f"{format_time(problem['clock'])} {problem['name']} {problem['severity']}")

        # print(f"{problem["interfaces"][0]["ip"]}    {problem["host"]}")

        hosts = problem.get("hosts", [])
        interfaces = problem.get("interfaces", [])

        host_name = hosts[0]["host"] if hosts else "Unknown host"
        ip_address = interfaces[0]["ip"] if interfaces else "Unknown IP"
        
        print(f"{host_name} ({ip_address})")

    print(problem)

        


if __name__ == "__main__":
    main()