import csv
import json
import sys

########################## File convert CSV to JSON ############################
def csv_to_json(csv_file):
   clients = []
   with open(csv_file, mode='r') as file:
       csv_reader = csv.DictReader(file)
       for row in csv_reader:
           client_id = int(row['Client ID'])
           client = next((c for c in clients if c['id'] == client_id), None)
           if client is None:
               client = {
                   'id': client_id,
                   'name': row['Client Name'],
                   'email': row['Client Email'],
                   'phone': row['Client Phone'],
                   'accounts': []
               }
               clients.append(client)
           account_id = int(row['Account ID'])
           account = next((a for a in client['accounts'] if a['id'] == account_id), None)
           if account is None:
               account = {
                   'id': account_id,
                   'type': row['Account Type'],
                   'balance': float(row['Account Balance']),
                   'cards': []
               }
               client['accounts'].append(account)
           card_id = int(row['Card ID'])
           card = {
               'id': card_id,
               'type': row['Card Type'],
               'expiry_date': row['Card Expiry Date'],
               'credit_limit': float(row['Card Credit Limit'])
           }
           account['cards'].append(card)
   return json.dumps(clients, indent=4)


########################## File convert JSON to CSV ############################
def json_to_csv(json_file):
   clients = json.load(open(json_file, 'r'))
   with open('output.csv', mode='w', newline='') as file:
       writer = csv.writer(file)
       writer.writerow(['Client ID', 'Client Name', 'Client Email', 'Client Phone', 'Account ID', 'Account Type', 'Account Balance', 'Card ID', 'Card Type', 'Card Expiry Date', 'Card Credit Limit'])
       for client in clients:
           for account in client['accounts']:
               for card in account['cards']:
                   writer.writerow([client['id'], client['name'], client['email'], client['phone'], account['id'], account['type'], account['balance'], card['id'], card['type'], card['expiry_date'], card['credit_limit']])

########################## Get File ############################
if len(sys.argv) < 3: 
   print("Usage: python convert.py input.csv output.json")
   sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

if input_file.endswith('.csv'):
   json_data = csv_to_json(input_file)
   with open(output_file, 'w') as file:
       file.write(json_data)
   print(f"CSV to JSON conversion completed. Output file: {output_file}")
elif input_file.endswith('.json'):
   json_to_csv(input_file)
   print(f"JSON to CSV conversion completed. Output file: {output_file}")
else:
   print("Unsupported input file format. Please provide a CSV or JSON file.")


