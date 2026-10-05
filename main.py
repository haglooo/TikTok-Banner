import os
import requests
import SignerPy

HOSTS = [
    "api16-normal-c-alisg.tiktokv.com",
    "api22-normal-c-alisg.tiktokv.com",
    "api16-normal-no1a.tiktokv.eu",
    "api16-normal-useast5.tiktokv.us",
]


def find_host(session_id):
    for host in HOSTS:
        try:
            response = requests.get(
                f"https://{host}/passport/web/account/info/",
                headers={
                    "Cookie": f"sessionid={session_id}",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                },
                timeout=10
            )
            try:
                data = response.json()
            except ValueError:
                continue
            if response.status_code == 200:
                account = data.get("data", {})
                if account.get("user_id_str"):
                    return host
            if response.status_code == 404 and data.get("status_code") == 0:
                user = data.get("data", {}).get("user", {})
                if user.get("id"):
                    return host
        except requests.RequestException:
            continue
    return None


def upload_banner_image(session, host, file_path):
    url = f"https://{host}/aweme/v1/upload/image/"

    params = {
      "_rticket": "1791016703379",
      "ab_version": "47.0.3",
      "ac": "wifi",
      "ac2": "wifi",
      "aid": "473824",
      "app_language": "en",
      "app_name": "lite",
      "app_package": "com.ss.android.ugc.tiktok.pro",
      "app_package_type": "pro_eu",
      "app_type": "normal",
      "build_number": "47.0.3",
      "channel": "googleplay",
      "current_region": "DE",
      "device_brand": "ROG",
      "device_id": "7680482516813628950",
      "device_platform": "android",
      "device_type": "ASUS_AI2401_A",
      "dpi": "480",
      "host_abi": "arm64-v8a",
      "iid": "7692357050986907406",
      "is_flip": "1",
      "is_pad": "0",
      "language": "en",
      "last_install_time": "1791016493",
      "locale": "en",
      "manifest_version_code": "470003",
      "mcc_mnc": "26201",
      "op_region": "DE",
      "os": "android",
      "os_api": "34",
      "os_version": "14",
      "region": "US",
      "residence": "DE",
      "resolution": "1080*1920",
      "ssmix": "a",
      "sys_region": "US",
      "timezone_name": "Europe/Amsterdam",
      "timezone_offset": "3600",
      "ts": "1791016703",
      "uoo": "0",
      "update_version_code": "470003",
      "version_code": "470003",
      "version_name": "47.0.3"
    }

    payload = {
        "source": "0",
    }

    if not os.path.isfile(file_path):
        raise FileNotFoundError("File not found")

    with open(file_path, "rb") as image_file:
        files = [
            (
                "file",
                (
                    os.path.basename(file_path),
                    image_file,
                    "application/octet-stream",
                ),
            )
        ]

        m = SignerPy.sign(
            params=params,
            payload=payload,
            aid=473824,
            version=8404,
        )

        headers = {
            "User-Agent": "com.zhiliaoapp.musically/2024604030 (Linux; U; Android 12; tr_TR; M2102J20SG; Build/SKQ1.211006.001; Cronet/TTNetVersion:45466851 2026-07-20 QuicVersion:c3b23989 2026-06-25)",
            "x-tt-ttnet-origin-host": host,
            "x-ss-dp": "473824",
            "Cookie": f"sessionid={session}",
        }

        headers.update(m)

        response = requests.post(
            url,
            params=params,
            data=payload,
            files=files,
            headers=headers,
        )

    try:
        return response.json()["data"]["uri"]
    except Exception as e:
        raise RuntimeError(f"Banner image upload failed: {e}\nResponse: {response.text}")


def change_banner(session, host, uri):
    url = f"https://{host}/aweme/v1/commit/user/"

    params = {
      "_rticket": "1791016703379",
      "ab_version": "47.0.3",
      "ac": "wifi",
      "ac2": "wifi",
      "aid": "473824",
      "app_language": "en",
      "app_name": "lite",
      "app_package": "com.ss.android.ugc.tiktok.pro",
      "app_package_type": "pro_eu",
      "app_type": "normal",
      "build_number": "47.0.3",
      "channel": "googleplay",
      "current_region": "DE",
      "device_brand": "ROG",
      "device_id": "7680482516813628950",
      "device_platform": "android",
      "device_type": "ASUS_AI2401_A",
      "dpi": "480",
      "host_abi": "arm64-v8a",
      "iid": "7692357050986907406",
      "is_flip": "1",
      "is_pad": "0",
      "language": "en",
      "last_install_time": "1791016493",
      "locale": "en",
      "manifest_version_code": "470003",
      "mcc_mnc": "26201",
      "op_region": "DE",
      "os": "android",
      "os_api": "34",
      "os_version": "14",
      "region": "US",
      "residence": "DE",
      "resolution": "1080*1920",
      "ssmix": "a",
      "sys_region": "US",
      "timezone_name": "Europe/Amsterdam",
      "timezone_offset": "3600",
      "ts": "1791016703",
      "uoo": "0",
      "update_version_code": "470003",
      "version_code": "470003",
      "version_name": "47.0.3"
    }

    payload = f'profile_bg_type=1&image_uri={uri}'

    m = SignerPy.sign(
        params=params,
        payload=payload,
        aid=473824,
        version=8404,
    )

    headers = {
        "User-Agent": "com.zhiliaoapp.musically/2024604030 (Linux; U; Android 12; tr_TR; M2102J20SG; Build/SKQ1.211006.001; Cronet/TTNetVersion:45466851 2026-07-20 QuicVersion:c3b23989 2026-06-25)",
        "x-tt-ttnet-origin-host": host,
        "x-ss-dp": "473824",
        "Cookie": f"sessionid={session}",
    }

    headers.update(m)

    response = requests.post(
        url,
        params=params,
        data=payload,
        headers=headers,
    )

    return response.json()


def set_banner(session, file_path):
    host = find_host(session)
    if not host:
        raise RuntimeError("Invalid session.")
    uri = upload_banner_image(session, host, file_path)
    result = change_banner(session, host, uri)
    return result.get("status_code") == 0, result

ssid = input("sessionid: ")
file_path = input("image path: ")
set_banner(ssid, file_path)


# t.me/drumkit
