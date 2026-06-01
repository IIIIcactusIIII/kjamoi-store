# Kjamoi Store (v2.0)

A lightweight, automated Linux package installation and system update manager built with Python and SQLite3. **Kjamoi Store** provides a streamlined, unified interface to install applications across multiple Linux package managers while actively verifying and logging success/failure histories into a local relational database.

---

## Key Features in v2.0

* **Unified Installation Interface:** Install packages seamlessly via `apt-get`, `snap`, `flatpak`, and `pip` using a single number-navigated CLI menu.
* **Stateful Database Tracking:** Automatically logs successful installations to an `install_history` table and failed attempts to an `install_failed` table using SQLite3.
* **Intelligent Path Verification:** Uses Python's native `shutil` library to safely verify if an application is active in the system `$PATH` post-installation.
* **Dynamic Environments (`sudo` protection):** Dynamically detects if `sudo` is available in the running shell environment before prepending root execution rights, optimizing runtime safety.
* **Safe System Maintenance:** Automates clean system updates (`update`, dependency dry-runs, and non-interactive upgrades) using stable `apt-get` system bindings.

---

##  How It Works under the Hood

The application follows a clean execution pipeline to guarantee system state syncs with your logs:

1. **User Choice:** User inputs a command via the numbered UI.
2. **Execution:** The script maps the chosen package store and calls a managed subprocess using `apt-get` optimization rules.
3. **Verification:** Rather than trusting terminal exit codes blindly, the tool directly queries the OS environment using `shutil.which()`.
4. **Data Persistence:** Relational logging saves the app name, package manager, and a clean ISO-formatted timestamp into `kjamoi.db`.

---

##  Getting Started

### Prerequisites
* Linux environment (Tested extensively on Linux Mint / Debian-based distros)
* Python 3.8+
* SQLite3 (Built into standard Python installations)

### Installation & Execution

1. Clone this repository to your local machine:
   ```bash
   git clone [https://github.com/IIIIcactusIIII/kjamoi-store.git](https://github.com/IIIIcactusIIII/kjamoi-store.git)
   cd ~/kjamoi-store
##    Credits: Ahmed Khalil
   this is a solo built open source app.
