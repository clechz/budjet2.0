import pandas as pd
import csv
from datetime import datetime
from .data import *

class CSV:
    csv_file = "csv/finance_data.csv"
    columns = ["date", "amount", "category", "description", "balance", "session_key"]
    
    #opens a csv file with the desired categories if there is'nt one already
    @classmethod
    def init_csv(cls):

        try:
            pd.read_csv(cls.csv_file)

        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.columns)
            df.to_csv(cls.csv_file, index=False)

            CSV.add("10-10-1000", "0", "Income", "empty", 0)


    @classmethod
    def add(cls, date, amount, category, description, session_key):
       

        #creates dict to add into csv
        new_row = {
            "date": date,
            "amount": amount,
            "category": category,
            'description': description,
            'balance': 0,
            "session_key": session_key
        }
        
        if category == "Expense":
            new_row["balance"] = float(amount)*-1

        elif category == "Income":
            new_row["balance"] = float(amount)


        #opens csv file and writes the dict into it
        with open(cls.csv_file, "a+", newline="") as csvfile:
            # Move the file pointer to the beginning of the file
            csvfile.seek(0)

            reader = csv.DictReader(csvfile)
            rows = list(reader)
            print("ROWS: ", rows)
            sorted_rows = sorted(rows, key=lambda row: datetime.strptime(row['date'], DATEFORMAT), reverse=False)
            print("SORTED ROWS: ", sorted_rows)
            session_rows=[]
            for dictrow in sorted_rows:
                if dictrow["session_key"] == session_key:
                    session_rows.append(dictrow)

            sorted_rows=session_rows
            #loop inside csv for amounts and types and adds balance as a column
            for i, row in enumerate(sorted_rows, start=1):
                #represents the balance right before this trasaction
                print("\n \n\n\n\n ROW", row)
                prev_balance = float(row["balance"])
                if str(prev_balance) != "empty" and prev_balance:

                    print("prev balance: ", prev_balance, "\n Category", category)
                    if category == "Expense":
                        new_row["balance"] = prev_balance - float(amount)

                    elif category == "Income":
                        new_row["balance"] = prev_balance + float(amount)
                    else:
                        print("Internal error line 55")
                    
                    
            
            print("writing: \n", new_row)
            # Move the file pointer to the end of the file to append new content
            csvfile.seek(0, 2)
            writer = csv.DictWriter(csvfile, fieldnames=cls.columns)
            writer.writerow(new_row)
        print(" Entry added successfuly")

    @classmethod
    def read(cls, session):
        try:
            with open(cls.csv_file, "r") as csvfile:
                reader = csv.DictReader(csvfile)
                rows = list(reader)[1:]
                i=0
                sorted_rows = sorted(rows, key=lambda row: datetime.strptime(row['date'], DATEFORMAT), reverse=False)
                for dictrow in sorted_rows:
                    if sorted_rows[i]["session_key"] == session:
                        dictrow.pop("session_key")
                        sorted_rows[i]=dictrow.values()

                    else:
                        sorted_rows[i]=None

                    i+=1
                    print("sorted rows", sorted_rows)

                return reversed(sorted_rows)
        except FileNotFoundError:
            cls.init_csv(session)


def run():
    #ensures there is a dict already
    CSV.init_csv()
    #different columns prompts
    date = get_date("Enter the date of the transaction (dd-mm-yyyy) or enter for todays date: ", allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    #opens csv file and writes the dict into it
    CSV.add(date, amount, category, description)
    
