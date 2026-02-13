import sqlite3
import time
from rich.console import Console
from rich.table import Table
from prompt_toolkit import prompt

DB_FILE = "law_db.sqlite"
console = Console()

TABLES = ["clients", "lawyers", "cases"]

def get_table_data(table_name):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table_name}")
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    conn.close()
    return columns, rows

def show_table(table_name):
    console.clear()
    console.rule(f"[bold yellow]{table_name.upper()} TABLE[/bold yellow]")
    columns, rows = get_table_data(table_name)
    table = Table(show_lines=True)
    for col in columns:
        table.add_column(col, style="cyan", justify="center")

    for row in rows:
        table.add_row(*[str(x) if x is not None else "" for x in row])

    console.print(table)
    console.print("\n[green]Commands: edit | delete | next | prev | refresh | switch <table> | exit[/green]")

def edit_record(table_name):
    columns, _ = get_table_data(table_name)
    record_id = prompt("Enter ID of record to edit: ").strip()
    console.print(f"Available columns: {', '.join(columns[1:])}")
    column = prompt("Enter column to edit: ").strip()
    new_value = prompt("Enter new value: ").strip()

    if column not in columns:
        console.print("[red]Invalid column name![/red]")
        return

    id_col = columns[0]
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(f"UPDATE {table_name} SET {column} = ? WHERE {id_col} = ?", (new_value, record_id))
    conn.commit()
    conn.close()
    console.print(f"[green]{table_name} record {record_id} updated![/green]")

def delete_record(table_name):
    columns, _ = get_table_data(table_name)
    record_id = prompt("Enter ID of record to delete: ").strip()
    id_col = columns[0]
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(f"DELETE FROM {table_name} WHERE {id_col} = ?", (record_id,))
    conn.commit()
    conn.close()
    console.print(f"[red]{table_name} record {record_id} deleted![/red]")

def main():
    current_index = 0
    table_name = TABLES[current_index]
    last_refresh = 0

    while True:
        now = time.time()
        if now - last_refresh > 5:
            show_table(table_name)
            last_refresh = now

        cmd = prompt("\n> ").strip().lower()

        if cmd == "exit":
            console.print("[bold red]Exiting backend...[/bold red]")
            break
        elif cmd == "refresh":
            show_table(table_name)
        elif cmd == "next":
            current_index = (current_index + 1) % len(TABLES)
            table_name = TABLES[current_index]
            show_table(table_name)
        elif cmd == "prev":
            current_index = (current_index - 1) % len(TABLES)
            table_name = TABLES[current_index]
            show_table(table_name)
        elif cmd.startswith("switch"):
            try:
                _, name = cmd.split()
                if name in TABLES:
                    table_name = name
                    show_table(table_name)
                else:
                    console.print("[red]Invalid table name![/red]")
            except ValueError:
                console.print("[red]Usage: switch <table>[/red]")
        elif cmd == "edit":
            edit_record(table_name)
            show_table(table_name)
        elif cmd == "delete":
            delete_record(table_name)
            show_table(table_name)
        else:
            console.print("[red]Unknown command. Try 'help' or 'refresh'.[/red]")

if __name__ == "__main__":
    main()
