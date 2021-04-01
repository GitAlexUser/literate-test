import json
import psycopg2

white_list = ["Port-channel",
              "TenGigabitEthernet",
              "GigabitEthernet"]
intf_lst = []# interface list

def reader():
    with open('configClear_v2.json') as json_data:
        data = json.load(json_data)
        adress = data["frinx-uniconfig-topology:configuration"]["Cisco-IOS-XE-native:native"]["interface"]

    for i in adress:#full list
        if i in white_list:#clining
            for j in adress[i]:
                name = str(i) + str(j["name"])
                t = {}
                t['name'] = str(name)
                if "mtu" in j:
                    t["max_frame_size"] = int(j['mtu'])
                if "description" in j:
                    t["description"] = str(j["description"])
                if "Cisco-IOS-XE-ethernet:channel-group" in j:
                    t["port_channel_id"] = int(j["Cisco-IOS-XE-ethernet:channel-group"]["number"])
                t["config"] = json.dumps(j)

                intf_lst.append(t)

def loader():
    con = psycopg2.connect(user="postgres",
                               password="1234",
                               host="127.0.0.1",
                               port="5432",
                               database="postgres_db")
    cursor = con.cursor()

    for j in intf_lst:
        keys = j.keys()
        columns = ','.join(keys)
        values = ','.join(['%({})s'.format(k) for k in keys])
        insert = 'insert into connections ({0}) values ({1})'.format(columns, values)
        cursor.execute(insert, j)

    con.commit()
    con.close()

reader()
loader()