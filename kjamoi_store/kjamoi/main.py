#libraries needed
import subprocess #used to run commands in the terminal
import sys #used to make simpler and cleaner exist (i am adding this becouse i forget why i added libiraries sometimes)
import os #the primary os library, i am not sure if we need it or not
import sqlite3 #python's data base
import time #to save the date
import datetime #to save the date too
import shutil #to fix the sudo problem

def data_check(app_name, store, cursor, connection):
    """Checks if app is installed and logs result to the database."""
    timestamp = str(datetime.datetime.now())
    if is_app_installed(app_name):
        print(f"{app_name} is installed.")
        cursor.execute(
            "INSERT INTO install_history (app_name, store, date) VALUES (?, ?, ?)",
            (app_name, store, timestamp)
        )
    else:
        print(f"{app_name} is not installed.")
        cursor.execute(
            "INSERT INTO install_failed (app_name, store, date) VALUES (?, ?, ?)",
            (app_name, store, timestamp)
        )
    connection.commit()

#stores list 
stores = ['apt', 'snap', 'flatpak', 'pip']

#function that checks if the app is installed
def is_app_installed(check_app_name):
    """Returns True if the executable is found in the system PATH."""
    return shutil.which(check_app_name) is not None


#the main functiion
def main():
    #connect the database
    connection = sqlite3.connect('kjamoi.db')
    cursor = connection.cursor()
    #create a table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS install_history (
            app_name TEXT NOT NULL,
            store TEXT NOT NULL,
            date text NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS install_failed (
            app_name TEXT NOT NULL,
            store TEXT NOT NULL,
            date text NOT NULL
        )
    """)

    global using_program
    print(r'''
      _  __   _   _    __  __  ___ ___   ____ _____ ___  ____  _____ 
     | |/ /  | | / \  |  \/  |/ _ \_ _| / ___|_   _/ _ \|  _ \| ____|
     | ' /_  | |/ _ \ | |\/| | | | | |  \___ \ | || | | | |_) |  _|  
     | . \ |_| / ___ \| |  | | |_| | |   ___) || || |_| |  _ <| |___ 
     |_|\_\___/_/   \_\_|  |_|\___/___| |____/ |_| \___/|_| \_\_____|
                                                                      V2.0''')
    choice = input('choose if you want to update or install an app or exit(1.update \n2.install \n3.exit\n4.install stores\n5.view succesful install history\n6.view failed install attempts\n): ')
    try:
        #the acual app
        sudo_prefix = ['sudo'] if shutil.which('sudo') else []

        if choice == '2':
            app_name=input('please input ur app name:')
            store= input('what store do you want to use eg. flatpak, apt, snap:')
            if store in stores:
                if store == 'apt':
                    subprocess.run(sudo_prefix + ['apt-get', 'install', app_name], check=True)
                    data_check(app_name, store, cursor, connection)
                else:
                    subprocess.run(sudo_prefix + [store.lower(), 'install', app_name], check=True)
                    data_check(app_name, store, cursor, connection)
            else:
                input('please select a supported store, press inter to continue')
            
        elif choice == '1':
            print('updating the following packeges')
            subprocess.run(sudo_prefix + ['apt-get', 'update'], check=True)
            subprocess.run(sudo_prefix + ['apt-get', '-s', 'upgrade'], check=True)
            subprocess.run(sudo_prefix + ['apt-get', 'upgrade', '-y'], check=True)
        elif choice == '4':
            subprocess.run(sudo_prefix + ['apt-get', 'install', 'apt-utils'], check=True)
            subprocess.run(sudo_prefix + ['apt-get', 'install', 'snap'], check=True)
            subprocess.run(sudo_prefix + ['apt-get', 'install', 'flatpak'], check=True)
        elif choice == '3':
            using_program = False
            sys.exit(0)
        elif choice == '5':
            cursor.execute("SELECT * FROM install_history")
            rows = cursor.fetchall()
            for row in rows:
                print(row)
        elif choice == '6':
            cursor.execute("SELECT * FROM install_failed")
            rows = cursor.fetchall()
            print('apps failed to install')
            for row in rows:
                
                print(f'App: {row[0]}, \nStore: {row[1]}, \nDate: {row[2]}')
        else:
            print('please select a valid option (1-6)')
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        if isinstance(e, FileNotFoundError):
            print(f"Error: The command '{e.filename}' was not found. If you are running this inside a Flatpak (like VSCodium), it may not have access to system package managers.")
            return
        print(f"An error occurred: {e}")
        print("This usually means another process is using apt (Lock error) or the package name is invalid.")
    finally:
        connection.close()

if __name__ == '__main__':
    using_program = True
    while using_program:
        main()