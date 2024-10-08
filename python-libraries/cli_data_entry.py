from rich.console import Console
from rich.table import Table
import csv
import os
import io

console = Console()

table = Table(title='Logging Meals')
table.add_column("Date")
table.add_column("Time")
table.add_column("Description")
table.add_column("Calories")

def log_meals():
    while True:
        console.print("\n[bold green]Log a new meal[/bold green]")
        food_date = console.input("What day did you have this meal: ")
        food_time = console.input("What time did you have this meal: ")
        food_description = console.input("What did you have to eat: ")
        food_calories = console.input("How many calories was this meal: ")

        console.print("\n[bold yellow]Please confirm this was your entry")
        console.print(f"[bold]Date:[/bold] {food_date}")
        console.print(f"[bold]Time:[/bold] {food_time}")
        console.print(f"[bold]Description:[/bold] {food_description}")
        console.print(f"[bold]Calories:[/bold] {food_calories}")

        confirm = console.input("\nIs this the correct information (yes/no): ")
        if confirm == 'yes':
            return food_date, food_time, food_description, food_calories
            table.add_row(food_date, food_time, food_description, food_calories)
        else:
            console.print(["[bold red]Let's try this again then[/bold red]"])

def save_data(data, filename="food_log.csv"):
    file_exists = os.path.isfile(filename)
    output = io.StringIO()

    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Date', 'Time', 'Description', 'Calories'])
        writer.writerows(data)
        csv_content = output.getvalue()


    console.print(f"\n[cyan]Data has been saved to {os.path.abspath(filename)}[/cyan]")
    console.print(csv_content)

def display_data(filename="food_log.csv"):
    if os.path.isfile(filename):
        table = Table(title='Logged Meals')
        table.add_column("Date")
        table.add_column("Time")
        table.add_column("Description")
        table.add_column("Calories")

        with open(filename, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                table.add_row(*row)

        console.print(table)
    else:
        console.print("[bold red]No data found to display.[/bold red]")


food_log = []
while True:
    get_log = log_meals()
    food_log.append(get_log)

    add_log = console.input("Do you want to add another food (yes/no): ").lower()

    if add_log != 'yes':
        break

save_data(food_log)
console.print("\n[bold green]All entries have been saved![/bold green]")

display_data()

