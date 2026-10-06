from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# ==========================================
# FURAYAASHA SIRTA AH
# ==========================================
# Kani waa Token-kii ka muuqday sawirka aad ila wadaagtay
WHATSAPP_TOKEN = "EAAZAz1uUSg3MBStux3OOUhHzZUgx" 

# Nambarkaaga ID-ga ee aan ka qaaday sawiradii hore
PHONE_NUMBER_ID = "1407873482402133" 

VERIFY_TOKEN = "dalab_ai_sir_123" 

# ==========================================
# WEBHOOK & QABASHADA FARRIIMAHA
# ==========================================
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if mode and token:
            if mode == 'subscribe' and token == VERIFY_TOKEN:
                print("Webhook waa la xaqiijiyay!")
                return challenge, 200
            else:
                return 'Xaqiijintu way fashilantay', 403

    elif request.method == 'POST':
        body = request.get_json()

        if body.get('object'):
            if body.get('entry') and body['entry'][0].get('changes') and body['entry'][0]['changes'][0].get('value').get('messages'):
                message = body['entry'][0]['changes'][0]['value']['messages'][0]
                phone_number = message['from']
                
                # ---------------------------------------------------------
                # NIDAAMKA LACAG BIXINTA (MASTERCARD KALIYA)
                # ---------------------------------------------------------
                jawaab = (
                    "Ku soo dhawow Dalab AI!\n\n"
                    "Si aad u sii isticmaasho adeeggan, fadlan iska bixi "
                    "rukunka (subscription) adigoo isticmaalaya Mastercard-kaaga.\n\n"
                    "Guji link-gan si aad lacagta u bixiso: [Link-ga Mastercard ayaa halkan iman doona]"
                )
                
                send_whatsapp_message(phone_number, jawaab)

            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"status": "error"}), 404

# ==========================================
# DIRISTA FARRIIMAHA
# ==========================================
def send_whatsapp_message(to, message):
    url = f"https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": message}
    }
    requests.post(url, headers=headers, json=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
