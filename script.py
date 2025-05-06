from zabbix_utils import ZabbixAPI
import pandas as pd

ZABBIX_SERVER = "127.0.0.1/zabbix"
ZABBIX_API_TOKEN = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

zapi = ZabbixAPI(url=ZABBIX_SERVER, token=ZABBIX_API_TOKEN)
print("Connected to Zabbix API")

hosts = zapi.host.get(
            output=['host', 'hostid']
        )

result = []

for host in hosts:
    triggers = zapi.trigger.get(output=['triggerid', 'description'],
                            hostids = host['hostid'],
                            selectTags="extend"
    )
    for trig in triggers:
        tag_interface = None
        tag_scope = None
        for tag in trig.get('tags', []):
            if tag["tag"] == "interface":
                tag_interface = tag['value']
            elif tag["tag"] == "scope":
                tag_scope = tag['value']
            
        result.append({
            "host": host['host'],
            "triggerid": trig['triggerid'],
            "description": trig['description'],
            "interface": tag_interface,
            "scope": tag_scope
        })
    
df = pd.DataFrame(result)

file_path = 'A/B/C/D/Triggers.xlsx'
df.to_excel(file_path, sheet_name='triggers', index=False)

print(f"Data written in '{file_path}'") 
