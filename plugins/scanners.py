import json
from subprocess import check_output, CalledProcessError, STDOUT
import requests
from fake_useragent import UserAgent

# Toggle to use tools installed in the system path instead of using from plugins
USE_PREINSTALLED_TOOLS = False

def find_cms(url):
    try:
        ua = UserAgent()
        headers = {'User-Agent': ua.random}
        res = requests.get(url, headers=headers)
    except:
        return "unknown"
    if "wp-content/themes/" in res.text or "powered by WordPress" in res.text:
        return "wordpress"
    elif "Drupal.settings" in res.text:
        return "drupal"
    elif "window.vBulletin" in res.text or "vBulletin_" in res.text:
        return "vbulletin"
    elif "Joomla!" in res.text or "joomla-script-" in res.text:
        return "joomla"
    return "unknown"


def cmd_runner(cmd, jsono=True):
    try:
        result = check_output(cmd, stderr=STDOUT, universal_newlines=True)
        return result
    except CalledProcessError as exc:
        print("[ERROR]", exc.returncode, exc.output)
        if jsono:
            return json.dumps(json.loads(exc.output.strip()))
        return exc.output.strip()


def droopescan(url):
    print(f"[INFO] droopescan scanning URL: {url}")
    if not url.endswith("/"):
        url += "/"
    droope_scan = ['droopescan', 'scan', 'drupal', '-u',
               url, '-t', '8', '-o', 'json', '-e', 'a',
               '--hide-progressbar']
    return cmd_runner(droope_scan)


def update_wpscan():
    print("[INFO] Updating WPScan")
    cmd_runner(['wpscan', '--update'], False)


def wpscan(url):
    print(f"[INFO] wpscan scanning URL: {url}")
    if not url.endswith("/"):
        url += "/"
    wp_scan = ['wpscan', '--url', url, '--no-banner', '-f', 'json',
               '--force', '-e', 'vp,vt', '--plugins-detection',
               'mixed', '--rua']
    return cmd_runner(wp_scan)


def vbscan(url):
    print(f"[INFO] vbscan scanning URL: {url}")
    if not url.endswith("/"):
        url += "/"
    if USE_PREINSTALLED_TOOLS:
        vb_scan = ['vbscan', url]
    else:
        vb_scan = ['perl', 'plugins/vbscan/vbscan.pl', url]
    return cmd_runner(vb_scan)


def joomscan(url):
    print(f"[INFO] joomscan scanning URL: {url}")
    if not url.endswith("/"):
        url += "/"
    if USE_PREINSTALLED_TOOLS:
        jm_scan = ['joomscan', '--url', url, '-ec']
    else:
        jm_scan = ['perl', 'plugins/joomscan/joomscan.pl', '--url', url, '-ec']
    return cmd_runner(jm_scan)
