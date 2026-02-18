import requests
from typing import List, Dict, Any


class ZabbixClint:
    def __init__(self, base_url: str, api_token: str, verify_lts: bool = True):
        self.base_url = base_url.rstrip("/") + "/api_jsonrpc.php"
        self.token = api_token
        self.verify_lts = verify_lts
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
        })

    def _call(self, method: str, params: Dict[str, Any] | None = None) -> Any:
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "auth": self.token,
            "id": 1,
        }
        response = self.session.post(
            self.base_url, json=payload, verify=self.verify_lts, timeout=20)
        response.raise_for_status()
        data = response.json()

        if "error" in data:
            raise RuntimeError(data["error"])

        return data["result"]

    def get_current_problems(self) -> List[Dict[str, Any]]:

        return self._call("problem.get", {
            "output": ["name", "severity", "clock", "eventid"],
            "recent": False,
            "sortfield": "eventid",
            "sortorder": "DESC",
        })

    def get_event_hosts(self, event_ids) -> List[Dict[str, Any]]:
        return self._call("event.get", {
            "eventids": event_ids,
            "output": ["eventid"],
            "selectHosts": ["hostid", "name"]
        })

    def get_host_ips(self,host_ids):
        hosts = self._call("host.get",{
            "hostids":host_ids,
            "output":["hostid"],
            "selectInterfaces": ["ip","main"]
        })

        ip_map = {}

        for host in hosts:
            interfaces = host.get("interfaces", [])

            ip = "N/A"

            for interface in interfaces:
                if interface.get("main") == "1":
                    ip = interface.get("ip")
                    break

            

            if ip == "N/A" and interfaces:
                ip = interfaces[0].get("ip","N/A")

            ip_map[host["hostid"]] = ip

        return ip_map
