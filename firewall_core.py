import threading
import pydivert
import json
import time

RULES_FILE = "rules.json"
LOG_FILE = "logs.txt"

firewall_running = False
firewall_thread = None

rules = {
    "mode": "block",    
    "ips": []
}

# ----------------------------- RULES MANAGEMENT -----------------------------

def load_rules():
    global rules
    try:
        with open(RULES_FILE, "r", encoding="utf-8") as f:
            rules = json.load(f)
    except:
        save_rules()
    return rules


def save_rules():
    with open(RULES_FILE, "w", encoding="utf-8") as f:
        json.dump(rules, f, indent=4)


def add_ip(ip):
    if ip not in rules["ips"]:
        rules["ips"].append(ip)
        save_rules()
        log_event(f"Rule Added: {ip}")
        return True
    return False


def remove_ip(ip):
    if ip in rules["ips"]:
        rules["ips"].remove(ip)
        save_rules()
        log_event(f"Rule Removed: {ip}")
        return True
    return False


def set_mode(mode):
    rules["mode"] = mode
    save_rules()
    log_event(f"Mode changed to: {mode.upper()}")


# --------------------------------- LOGGING ---------------------------------

def log_event(text):
    """Always write logs in UTF-8, avoid Windows cp1252 crashes."""
    try:
        timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]")
        safe_text = text.encode("utf-8", errors="ignore").decode("utf-8")
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"{timestamp} {safe_text}\n")
    except Exception as e:
        print("Log Write Error:", e)


# ------------------------------ FIREWALL ENGINE -----------------------------

def start_firewall():
    global firewall_running, firewall_thread

    if firewall_running:
        return

    firewall_running = True
    load_rules()

    firewall_thread = threading.Thread(target=firewall_loop, daemon=True)
    firewall_thread.start()


def stop_firewall():
    global firewall_running
    firewall_running = False
    log_event("Firewall Stopped")


def firewall_loop():
    log_event("Firewall Started")
    print("🔥 Firewall Engine Running...")

    try:
        with pydivert.WinDivert("true") as w:  # capture all packets
            for packet in w:

                if not firewall_running:
                    break

                src = packet.src_addr
                dst = packet.dst_addr

                mode = rules["mode"]
                ip_list = rules["ips"]

                # ------------------ ALLOW MODE (Whitelist) ------------------
                if mode == "allow":
                    if src not in ip_list and dst not in ip_list:
                        log_event(f"BLOCKED (Not allowed): {src} -> {dst}")
                        continue

                # ------------------ BLOCK MODE ------------------------------
                elif mode == "block":
                    if src in ip_list or dst in ip_list:
                        log_event(f"BLOCKED (Rule match): {src} -> {dst}")
                        continue

                # Reinjection
                try:
                    w.send(packet)
                except Exception:
                    log_event("Packet reinject failed")

    except Exception as e:
        log_event(f"WinDivert crashed: {e}")
        print("WinDivert crashed:", e)

def get_status():
    return firewall_running
