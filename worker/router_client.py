from netmiko import ConnectHandler
import ntc_templates, os, json

def get_interfaces():

    os.environ["NET_TEXTFSM"] = os.path.join(
        os.path.dirname(ntc_templates.__file__), "templates"
    )

    device = {
        "device_type": "cisco_ios",
        "host": "10.0.29.101",
        "username": "admin",
        "password": "cisco",
    }

    with ConnectHandler(**device) as conn:
        conn.enable()
        result = conn.send_command("show ip int br", use_textfsm=True)
        conn.disconnect()

    print(json.dumps(result, indent=2))


if __name__=='__main__':
    get_interfaces()
