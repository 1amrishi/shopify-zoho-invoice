{\rtf1\ansi\ansicpg1252\cocoartf2818
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 from flask import Flask, request, jsonify\
import requests\
import os\
\
app = Flask(__name__)\
\
# Get Zoho API Credentials from Railway Environment Variables\
CLIENT_ID = os.getenv("ZOHO_CLIENT_ID")\
CLIENT_SECRET = os.getenv("ZOHO_CLIENT_SECRET")\
REFRESH_TOKEN = os.getenv("ZOHO_REFRESH_TOKEN")\
ORGANIZATION_ID = os.getenv("ZOHO_ORGANIZATION_ID")\
\
def get_new_access_token():\
    """Fetches a new access token using the refresh token"""\
    url = "https://accounts.zoho.com/oauth/v2/token"\
    payload = \{\
        "refresh_token": REFRESH_TOKEN,\
        "client_id": CLIENT_ID,\
        "client_secret": CLIENT_SECRET,\
        "grant_type": "refresh_token"\
    \}\
    response = requests.post(url, data=payload)\
    return response.json()["access_token"]\
\
@app.route("/webhook", methods=["POST"])\
def create_invoice():\
    """Receives Shopify Webhook and creates an invoice in Zoho Books"""\
    data = request.json  # Shopify order data\
    access_token = get_new_access_token()\
\
    customer_name = f"\{data['customer']['first_name']\} \{data['customer']['last_name']\}"\
    customer_email = data["customer"]["email"]\
    line_items = data["line_items"]\
\
    items = [\{"item_name": item["name"], "rate": item["price"], "quantity": item["quantity"]\} for item in line_items]\
\
    invoice_data = \{\
        "customer_name": customer_name,\
        "customer_email": customer_email,\
        "line_items": items\
    \}\
\
    headers = \{"Authorization": f"Zoho-oauthtoken \{access_token\}", "Content-Type": "application/json"\}\
    response = requests.post(\
        f"https://books.zoho.com/api/v3/invoices?organization_id=\{ORGANIZATION_ID\}",\
        json=invoice_data,\
        headers=headers\
    )\
\
    return jsonify(response.json()), response.status_code\
\
if __name__ == "__main__":\
    app.run(port=5000, debug=True)\
}