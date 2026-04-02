import subprocess
import os
#the main functiion
def main():
    global using_program
    print('''
      _  __   _   _    __  __  ___ ___   ____ _____ ___  ____  _____ 
     | |/ /  | | / \  |  \/  |/ _ \_ _| / ___|_   _/ _ \|  _ \| ____|
     | ' /_  | |/ _ \ | |\/| | | | | |  \___ \ | || | | | |_) |  _|  
     | . \ |_| / ___ \| |  | | |_| | |   ___) || || |_| |  _ <| |___ 
     |_|\_\___/_/   \_\_|  |_|\___/___| |____/ |_| \___/|_| \_\_____|
                                                                  ''')
    choice=input('choose if you want to update or install an app or exit(update/install/exit/install stores)')
    try:
        #the acual app

        if choice.lower() == 'install':
            app_name=input('please input ur app name:')
            store= input('what store do you want to use eg. flatpak, apt, snap:')
            if store == 'apt':
                subprocess.run(['sudo', 'apt-get', 'install', app_name], check=True)
            elif store == 'snap':
                subprocess.run(['sudo', 'snap', 'install', app_name], check=True)
            elif store == 'flatpak':
                subprocess.run(['sudo', 'flatpak', 'install', app_name], check=True)
            elif store == 'pip':
                subprocess.run(['pip', 'install', app_name], check=True)
            else:
                input('please select a supported store, press inter to continue')
        elif choice.lower() == 'update':
            print('updating the following packeges')
            subprocess.run(['sudo', 'apt-get', 'update'], check=True)
            subprocess.run(['sudo', 'apt-get', '-s', 'upgrade'], check=True)
            subprocess.run(['sudo', 'apt-get', 'upgrade', '-y'], check=True)
        elif choice.lower() == 'install stores':
            subprocess.run(['sudo', 'apt-get', 'install', 'apt-utils'], check=True)
            subprocess.run(['sudo', 'apt-get', 'install', 'snap'], check=True)
            subprocess.run(['sudo', 'apt-get', 'install', 'flatpak'], check=True)
        elif choice == 'exit':
            using_program = False
        else:
            print('please use update or install or exit')
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        print("This usually means another process is using apt (Lock error) or the package name is invalid.")
if __name__ == '__main__':
    using_program = True
    while using_program:
        main()