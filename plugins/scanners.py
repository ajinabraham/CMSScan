import json
from subprocess import check_output, CalledProcessError, STDOUT
import requests
from fake_useragent import UserAgent


def find_cms(url):
    try:
        ua = UserAgent()
        headers = {'User-Agent': ua.random}
        res = requests.get(url, headers=headers)
    except:
        return "unknown"
    if "wp-content/themes/" in res.text:
        return "wordpress"
    elif "Drupal.settings" in res.text:
        return "drupal"
    return "unknown"


def cmd_runner(cmd):
    try:
        result = check_output(cmd, stderr=STDOUT, universal_newlines=True)
        return result
    except CalledProcessError as exc:
        print("[ERROR]", exc.returncode, exc.output)
        return json.dumps(json.loads(exc.output.strip()))


def droopescan(url):
    print(f"[INFO] droopescan scanning URL: {url}")
    if not url.endswith("/"):
        url += "/"
    wp_scan = ['droopescan', 'scan', 'drupal', '-u',
               url, '-t', '8', '-o', 'json', '-e', 'a',
               '--hide-progressbar']
    return cmd_runner(wp_scan)


def update_wpscan():
    print("[INFO] Updating WPScan")
    cmd_runner(['wpscan', '--update'])


def wpscan(url):
    print(f"[INFO] wpscan scanning URL: {url}")
    if not url.endswith("/"):
        url += "/"
    wp_scan = ['wpscan', '--url', url, '--no-banner', '-f', 'json',
               '--force', '--wp-content-dir', url + 'wp-content/',
               '-e', 'vp,vt', '--plugins-detection', 'mixed', '--rua']
    return cmd_runner(wp_scan)
