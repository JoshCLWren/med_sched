import os
import shutil

import arrow


def create_backup():
    """Create a backup of the database"""
    print("Creating backup...")
    print("Checking for backups directory...")
    if not os.path.exists("backups"):
        print("Backups directory not found, creating...")
        os.mkdir("backups")
    print("Creating new backup...")
    try:
        shutil.copyfile("data.db", f"backups/{arrow.now().format('YYYY-MM-DD')}.db")
        print("Backup created!")
    except Exception as e:
        print("Error creating backup!")
        print(e)


def restore_backup():
    """Restore from a backup"""
    breakpoint()
    print("Restoring from backup...")
    print("Checking for backups directory...")
    if not os.path.exists("backups"):
        print("Backups directory not found...")

        print("Sorry, no backups found.")
        return
    else:
        print("Backups directory found...")
    print("Checking for backups in backups directory...")
    if backups := os.listdir("backups"):
        print("Backups found, getting latest backup...")
        latest_backup = backups
        latest_backup.sort()
        latest_backup = latest_backup[-1]
        print(f"Latest backup found: {latest_backup}")
        print("Copying latest backup to database...")
        try:
            shutil.copyfile(
                f"backups/{arrow.get(latest_backup).format('YYYY-MM-DD')}.db",
                "database.db",
            )
            print("Backup restored!")
        except Exception as e:
            print("Error restoring backup!")
            print(e)
            return
    else:
        print("No backups found...")
        print("Sorry, no backups found.")
        return

    print("Backup restored!")
