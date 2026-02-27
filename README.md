 Overview

A real-time SSH brute force detection tool built in Python.
It monitors Ubuntu authentication logs, detects repeated failed login attempts from the same IP address, and simulates automated blocking with auto-unban functionality.

Designed for **cybersecurity labs, SOC practice, and defensive security learning**.

---

##  Features

*  Real-time log monitoring (`tail -f` style)
*  Detects multiple failed SSH login attempts
*  Configurable threshold
*  Simulated IP blocking
*  Auto-unban after defined time
*  Whitelist support
*  Incident logging
*  Persistent blocked IP storage
-*  No external dependencies

---

##  Project Structure

```
ssh-bruteforce-detector/
│
├── main.py
├── config.json
├── blocked_ips.json
├── requirements.txt
├── README.md
└── logs/
    └── incidents.log
```

---

##  Configuration

Edit `config.json`:

```json
{
  "log_file": "/var/log/auth.log",
  "threshold": 5,
  "ban_time_seconds": 600,
  "whitelist": ["127.0.0.1"]
}
```

| Option             | Description                             |
| ------------------ | --------------------------------------- |
| `log_file`         | Path to SSH authentication log          |
| `threshold`        | Failed attempts before triggering block |
| `ban_time_seconds` | Duration of simulated block             |
| `whitelist`        | IPs excluded from blocking              |

---

##  Installation

### 1️. Clone repository

```bash
git clone https://github.com/yourusername/ssh-bruteforce-detector.git
cd ssh-bruteforce-detector
```

### 2️. Run tool (requires sudo to read auth logs)

```bash
sudo python3 main.py
```

---

##  How to Test (Lab Environment)

Test only in a controlled lab environment.

From another machine (e.g., Kali Linux):

```bash
ssh wronguser@UBUNTU_IP
```

Enter incorrect passwords multiple times to trigger detection.

---

##  How It Works

1. Reads `/var/log/auth.log`
2. Searches for `Failed password` entries
3. Extracts attacker IP
4. Counts attempts per IP
5. If threshold exceeded:

   * Logs incident
   * Simulates block
   * Starts auto-unban timer

---

##  Example Alert Output

```
[DEBUG] 192.168.1.50 failed attempt 6
[ALERT] Blocking IP: 192.168.1.50
```

---

##  Future Improvements

* Real firewall integration (`iptables`)
* Email alerts
* REST API dashboard
* Docker containerization
* Systemd service integration
* Risk scoring system

---

##  Use Case

This project demonstrates:

* Log analysis
* Detection engineering
* Incident response simulation
* Defensive automation
* SOC workflow fundamentals

---

##  Disclaimer

This project is for **educational and defensive security purposes only**.
Use strictly in authorized lab environments.

---

##  Author

Developed as part of cybersecurity practice and SOC skill development.
