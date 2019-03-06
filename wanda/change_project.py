import json
import requests

saas_ip = ""
saas_pass = ""
target_project_id = ""


def get_token_and_tenant_uuid():  # 获取token和admin租户uuid
    endpoint = 'http://%s:35357/v3/auth/tokens' % (saas_ip)
    payload = {
        "auth": {
            "identity": {
                "methods": ["password"],
                "password": {
                    "user": {
                        "name": "admin",
                        "domain": {
                            "name": "Default"
                        },
                        "password": ""
                    }
                }
            }
        }
    }
    payload["auth"]["identity"]["password"]["user"]["password"] = saas_pass
    headers = {'Content-type': 'application/json'}
    req = requests.post(endpoint, data=json.dumps(payload), headers=headers)
    token = req.headers['x-subject-token']
    tenant_uuid = req.json()['token']['user']['domain']['id']
    list_tau = [token, tenant_uuid]

    return list_tau


# 通过内网ip,查找虚拟机名
def get_instance_name(token, tenant_uuid, instance_fixed_ip):
    endpoint = 'http://%s:8774/v2.1/%s/os-fixed-ips/%s' % (
        saas_ip, tenant_uuid, instance_fixed_ip)
    headers = {'X-Auth-Token': token}
    req = requests.get(endpoint, headers=headers)
    res = req.json()
    instance_name = res["fixed_ip"]["hostname"]
    return instance_name


# 通过instance_name查找instance_uuid
def get_instance_uuid(token, tenant_uuid, instance_name):
    endpoint = 'http://%s:8774/v2.1/%s/servers/' % (saas_ip, tenant_uuid)
    headers = {'X-Auth-Token': token}
    req = requests.get(endpoint, headers=headers)
    res = req.json()
    instance_details = res["servers"]
    instance_uuid = ""
    for instance_info in instance_details:
        if instance_info["name"] == instance_name:
            instance_uuid == instance_info["id"]
    return instance_uuid


def get_flavor_name(token, tenant_uuid, instance_uuid):  # 获取flavor的name
    # endpoint = 'http://%s:8774/v2.1/%s/flavors/detail' % (saas_ip,
    #                                                             tenant_uuid)
    # headers = {'X-Auth-Token': token}
    # req = requests.get(endpoint, headers=headers)
    # res = req.json()
    # flavors_list = res['flavors']
    # for flavor_detail in flavors_list:
    #     if flavor_detail['ram'] == 2048 and flavor_detail['vcpus'] == 2:
    #         flavor_uuid = flavor_detail['id']
    #         return flavor_uuid
    endpoint = 'http://%s:8774/v2.1/%s/servers/%s' % (saas_ip, tenant_uuid,
                                                      instance_uuid)
    headers = {'X-Auth-Token': token}
    req = requests.get(endpoint, headers=headers)
    res = req.json()
    flavors_name = res["server"]["flavor"]["original_name"]
    return flavors_name


def get_volume_id(token, tenant_uuid, instance_uuid):
    endpoint = 'http://%s:8774/v2.1/%s/servers/%s/os-volume_attachments' % (
        saas_ip, tenant_uuid, instance_uuid)
    headers = {'X-Auth-Token': token}
    req = requests.get(endpoint, headers=headers)
    res = req.json()
    volume_attachments = res["volumeAttachments"]
    instance_volume_ids = []
    for i in range(len(volume_attachments)):
        instance_volume_ids.append(
            volume_attachments["volumeAttachments"][i]["id"])
    return instance_volume_ids


def get_instance_net_info(token, tenant_uuid, instance_uuid):
    endpoint = 'http://%s:8774/v2.1/%s/servers/%s/os-interface' % (
        saas_ip, tenant_uuid, instance_uuid)

    headers = {'X-Auth-Token': token}
    req = requests.get(endpoint, headers=headers)
    res = req.json()
    instance_fixed_ip = res["interfaceAttachments"][0]["fixed_ips"][0][
        "ip_address"]
    instance_port_mac = res["interfaceAttachments"][0]["mac_addr"]
    instance_port_id = res["interfaceAttachments"][0]["port_id"]
    instance_net_id = res["interfaceAttachments"][0]["net_id"]
    instance_subnet_id = res["interfaceAttachments"][0]["fixed_ips"][0][
        "subnet_id"]
    return instance_fixed_ip, instance_port_mac, instance_port_id, instance_net_id, instance_subnet_id


def create_volume_snapshot(token, tenant_uuid, instance_volume_ids):
    endpoint = 'http://%s:8776/v2/%s/snapshots' % (saas_ip, tenant_uuid)
    payload = {
        "snapshot": {
            "name": "",
            "description": "",
            "volume_id": "",
            "force": "true"
        }
    }
    snapshot_ids = []
    for i in range(len(instance_volume_ids)):
        payload["snapshot"]["name"] = instance_volume_ids[i] + "_snapshot"
        payload["snapshot"]["volume_id"] = instance_volume_ids[i]
        payload["snapshot"][
            "description"] = instance_volume_ids[i] + "_snapshot"
        headers = {'Content-type': 'application/json'}
        req = requests.post(
            endpoint, data=json.dumps(payload), headers=headers)
        snapshot_ids.append(req.json()["snapshots"][i]["id"])
    return snapshot_ids


#
def create_volume(token, tenant_uuid, snapshot_ids, instance_name):
    endpoint = 'http://%s:8776/v2/%s/volumes' % (saas_ip, tenant_uuid)
    payload = {"volume": {"snapshot_id": "", "name": ""}}
    headers = {'X-Auth-Token': token}
    mid_volume_ids = []
    for i in range(len(snapshot_ids)):
        payload["volume"]["snapshot_id"] = snapshot_ids[i]
        payload["volume"]["name"] = instance_name + "_" + i
        req = requests.post(
            endpoint, data=json.dumps(payload), headers=headers)
        volume_id = req.json()["volume"]["id"]
        mid_volume_ids.append(volume_id)
    return mid_volume_ids


def create_volume_transfer(token, tenant_uuid, from_snapshot_volume_id):
    endpoint = 'http://%s:8776/v2/%s/os-volume-transfer' % (saas_ip,
                                                            tenant_uuid)
    payload = {"transfer": {"volume_id": "", "name": ""}}
    transfer_dict = {}
    for volumeid in from_snapshot_volume_id:
        payload["transfer"]["volume_id"] = from_snapshot_volume_id[volumeid]
        payload["transfer"][
            "name"] = from_snapshot_volume_id[volumeid] + "_transfer"
        headers = {'Content-type': 'application/json'}
        req = requests.post(
            endpoint, data=json.dumps(payload), headers=headers)
        res = req.json()
        transfer_id = res["transfer"]["id"]
        transfer_auth_key = res["transfer"]["auth_key"]
        transfer_dict[transfer_id] = transfer_auth_key
    return transfer_dict


def accept_volume_transfer(token, tenant_uuid, transfer_dict):
    headers = {'Content-type': 'application/json'}
    new_volume_ids = []
    for transfer_id in transfer_dict.keys():
        endpoint = 'http://%s:8776/v2/%s/os-volume-transfer/%s/accept' % (
            saas_ip, tenant_uuid, transfer_id)
        payload = {
            "accept": {
                "auth_key": "",
                "transfer_id": "",
                "project_id": ""
            }
        }
        payload["accept"]["auth_key"] = transfer_dict[transfer_id]
        payload["accept"]["transfer_id"] = transfer_id
        payload["accept"]["project_id"] = target_project_id
        req = requests.post(
            endpoint, data=json.dumps(payload), headers=headers)
        res = req.json()
        new_volume_id = res["transfer"]["volume_id"]
        new_volume_ids.append(new_volume_id)


# 删除源port
def delete_port(token, instance_port_id):
    endpoint = 'http://%s:9696/v2.0/ports/%s' % (saas_ip, instance_port_id)
    headers = {'X-Auth-Token': token}
    requests.delete(endpoint, headers=headers)


# 源虚拟机卸载port
def delete_server_port(token, tenant_uuid, instance_uuid, instance_port_id):
    endpoint = 'http://%s:8774/v2.1/%s/servers/%s/os-interface/%s' % (
        saas_ip, tenant_uuid, instance_uuid, instance_port_id)
    headers = {'X-Auth-Token': token}
    requests.delete(endpoint, headers=headers)
