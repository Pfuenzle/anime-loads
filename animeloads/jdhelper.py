import myjdapi
import requests
import json

from Cryptodome.Cipher import AES
from binascii import unhexlify
import base64

@staticmethod
def decode_cnl(k, crypted):
#        k_list = list(k)
#        tmp = k_list[15]
#        k_list[15] = k_list[16]
#        k_list[16] = tmp
#        k = "".join(k_list)

    key = unhexlify(k)
    data = base64.standard_b64decode(crypted)
    obj = AES.new(key, AES.MODE_CBC, key)
    d = obj.decrypt(data)
    d = map(lambda x: x.strip(b'\r\x00'), d.split(b'\n'))
    d = list(d)
    return d

@staticmethod
def add_to_jd(host, passwords, source, crypted, jk):
    data = {
        "passwords": str(passwords),
        "source": str(source),
        "jk": str(jk),
        "crypted": str(crypted)
    }
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0 Waterfox/78.7.0"
    }
    try:
        req = requests.post("http://" + host + ":9666/flash/addcrypted2", data=data, headers=headers, timeout=30)
    except Exception:
        return False
    retdata = req.text
    if(retdata == "failed"):
        return False
    else:
        return True

@staticmethod
def add_to_jd_deprecated(host, port, passwords, links, pkg_name, destination_folder=""):
    data = {
           "params":[
              {
                 "packageName": pkg_name,
                 "autoExtract": True,
                 "autostart": True,
                 "destinationFolder": destination_folder,
                 "extractPassword": passwords,
                 "links": links,
                 "overwritePackagizerRules": True,
                 "priority": "DEFAULT"
              }
           ]
        }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0 Waterfox/78.7.0",
        "Content-type": "application/json"
    }
    try:
        req = requests.post(f'http://{host}:{port}/linkgrabberv2/addLinks', data=json.dumps(data), headers=headers)
    except Exception as e:
        print(f'Fehler beim senden des requests zum JDownloader: {e}')
    retdata = json.loads(req.text)
    if ("type" in retdata):
        print(f'Senden zum JD fehlgeschlagen: {retdata["type"]}')
        return False
    elif ("data" in retdata):
        print(f'Folge wurde zu JDownloader hinzugefügt. JobID: {retdata["data"]["id"]}')
        return True

@staticmethod
def add_to_myjd(myjd_user, myjd_pass, myjd_device, links, pkg_name, pwd, destination_folder=None):
    jd=myjdapi.Myjdapi()
    jd.set_app_key("animeloads")
    jd.connect(myjd_user, myjd_pass)
    jd.update_devices()
    device=jd.get_device(myjd_device)
    dl = device.linkgrabber

    return dl.add_links([{
                          "autostart": True,
                          "links": links,
                          "packageName": pkg_name,
                          "extractPassword": pwd,
                          "priority": "DEFAULT",
                          "downloadPassword": None,
                          "destinationFolder": destination_folder,
                          "overwritePackagizerRules": False
                      }])