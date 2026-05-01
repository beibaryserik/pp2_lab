import psycopg2
import json
import csv

conn = psycopg2.connect(
    dbname="phonebook",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
)

cur = conn.cursor()


# -------------------------
# ADD CONTACT
# -------------------------
def add_contact():
    try:
        name = input("Name: ")
        email = input("Email: ")
        birthday = input("Birthday (YYYY-MM-DD): ")
        group = input("Group: ")

        # FIX
        birthday = None if birthday in ("None", "", None) else birthday
        email = None if email in ("None", "", None) else email
        group = None if group in ("None", "", None) else group

        # group
        if group:
            cur.execute("""
                INSERT INTO groups(name)
                VALUES (%s)
                ON CONFLICT (name) DO NOTHING
            """, (group,))

            cur.execute("SELECT id FROM groups WHERE name=%s", (group,))
            group_id = cur.fetchone()[0]
        else:
            group_id = None

        # contact
        cur.execute("""
            INSERT INTO contacts(name, email, birthday, group_id)
            VALUES (%s, %s, %s, %s)
        """, (name, email, birthday, group_id))

        conn.commit()
        print("✅ Contact added")

    except Exception as e:
        conn.rollback()
        print("❌ Error:", e)


# -------------------------
# ADD PHONE
# -------------------------
def add_phone():
    try:
        name = input("Contact name: ")
        phone = input("Phone: ")
        ptype = input("Type (home/work/mobile): ")

        cur.execute("CALL add_phone(%s,%s,%s)", (name, phone, ptype))

        conn.commit()
        print("✅ Phone added")

    except Exception as e:
        conn.rollback()
        print("❌ Error:", e)


# -------------------------
# MOVE GROUP
# -------------------------
def move_group():
    try:
        name = input("Contact name: ")
        group = input("New group: ")

        cur.execute("CALL move_to_group(%s,%s)", (name, group))

        conn.commit()
        print("✅ Group updated")

    except Exception as e:
        conn.rollback()
        print("❌ Error:", e)


# -------------------------
# SEARCH
# -------------------------
def search():
    try:
        query = input("Search: ")

        cur.execute("SELECT * FROM search_contacts(%s)", (query,))
        rows = cur.fetchall()

        if not rows:
            print("❌ Nothing found")
            return

        for r in rows:
            print(r)

    except Exception as e:
        print("❌ Error:", e)


# -------------------------
# FILTER BY GROUP
# -------------------------
def filter_group():
    try:
        group = input("Group: ")

        cur.execute("""
            SELECT c.name, c.email
            FROM contacts c
            JOIN groups g ON c.group_id = g.id
            WHERE g.name = %s
        """, (group,))

        rows = cur.fetchall()

        if not rows:
            print("❌ No contacts")
            return

        for row in rows:
            print(row)

    except Exception as e:
        print("❌ Error:", e)


# -------------------------
# EXPORT JSON
# -------------------------
def export_json():
    try:
        cur.execute("""
            SELECT c.name, c.email, c.birthday, g.name,
                   p.phone, p.type
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones p ON c.id = p.contact_id
        """)

        data = {}

        for name, email, birthday, group, phone, ptype in cur.fetchall():
            if name not in data:
                data[name] = {
                    "name": name,
                    "email": email,
                    "birthday": str(birthday),
                    "group": group,
                    "phones": []
                }

            if phone:
                data[name]["phones"].append({
                    "number": phone,
                    "type": ptype
                })

        with open("contacts.json", "w") as f:
            json.dump(list(data.values()), f, indent=4)

        print("✅ Exported")

    except Exception as e:
        print("❌ Error:", e)


# -------------------------
# IMPORT JSON
# -------------------------
def import_json():
    try:
        with open("contacts.json") as f:
            data = json.load(f)

        for c in data:
            name = c.get("name")
            email = c.get("email")
            birthday = c.get("birthday")
            group = c.get("group")

            # FIX
            birthday = None if birthday in ("None", "", None) else birthday
            email = None if email in ("None", "", None) else email
            group = None if group in ("None", "", None) else group

            # duplicate check
            cur.execute("SELECT id FROM contacts WHERE name=%s", (name,))
            exists = cur.fetchone()

            if exists:
                choice = input(f"{name} exists. skip/overwrite: ")
                if choice == "skip":
                    continue
                else:
                    cur.execute("DELETE FROM contacts WHERE name=%s", (name,))

            # group
            if group:
                cur.execute("""
                    INSERT INTO groups(name)
                    VALUES (%s)
                    ON CONFLICT (name) DO NOTHING
                """, (group,))

                cur.execute("SELECT id FROM groups WHERE name=%s", (group,))
                group_id = cur.fetchone()[0]
            else:
                group_id = None

            # contact
            cur.execute("""
                INSERT INTO contacts(name,email,birthday,group_id)
                VALUES (%s,%s,%s,%s)
            """, (name, email, birthday, group_id))

            # phones
            for p in c.get("phones", []):
                cur.execute("CALL add_phone(%s,%s,%s)",
                            (name, p["number"], p["type"]))

        conn.commit()
        print("✅ Imported")

    except Exception as e:
        conn.rollback()
        print("❌ Error:", e)


# -------------------------
# IMPORT CSV
# -------------------------
def import_csv():
    try:
        with open("contacts.csv", newline='') as f:
            reader = csv.DictReader(f)

            for row in reader:
                name = row["name"]
                email = row["email"]
                birthday = row["birthday"]
                group = row["group"]
                phone = row["phone"]
                ptype = row["type"]

                # FIX
                birthday = None if birthday in ("None", "", None) else birthday
                email = None if email in ("None", "", None) else email
                group = group if group else None

                # group
                if group:
                    cur.execute("""
                        INSERT INTO groups(name)
                        VALUES (%s)
                        ON CONFLICT (name) DO NOTHING
                    """, (group,))

                    cur.execute("SELECT id FROM groups WHERE name=%s", (group,))
                    group_id = cur.fetchone()[0]
                else:
                    group_id = None

                # contact
                cur.execute("""
                    INSERT INTO contacts(name,email,birthday,group_id)
                    VALUES (%s,%s,%s,%s)
                    ON CONFLICT DO NOTHING
                """, (name, email, birthday, group_id))

                # phone
                cur.execute("CALL add_phone(%s,%s,%s)",
                            (name, phone, ptype))

        conn.commit()
        print("✅ CSV Imported")

    except Exception as e:
        conn.rollback()
        print("❌ Error:", e)


# -------------------------
# MENU
# -------------------------
def menu():
    while True:
        print("""
1. Add contact
2. Add phone
3. Move group
4. Search
5. Filter by group
6. Export JSON
7. Import JSON
8. Import CSV
0. Exit
        """)

        choice = input("Choose: ")

        if choice == "1":
            add_contact()
        elif choice == "2":
            add_phone()
        elif choice == "3":
            move_group()
        elif choice == "4":
            search()
        elif choice == "5":
            filter_group()
        elif choice == "6":
            export_json()
        elif choice == "7":
            import_json()
        elif choice == "8":
            import_csv()
        elif choice == "0":
            break


menu()

cur.close()
conn.close()