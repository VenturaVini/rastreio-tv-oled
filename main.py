import time
import requests
from bs4 import BeautifulSoup
from services.telegram import enviar_mensagem

def coletar_ultimo_evento():
    url = "http://vvlog.uxdelivery.com.br/tracking/rastrear"
    data = {"tipoBusca": "D", "nroBusca": "70386432406"}
    response = requests.post(url, data=data)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        blocos_data = soup.find_all("div", class_="tracking-header")

        for bloco_data in blocos_data:
            data_evento = bloco_data.get_text(strip=True)
            for sibling in bloco_data.find_next_siblings():
                if "tracking-header" in sibling.get("class", []):
                    break
                if "tracking-detalhe" in sibling.get("class", []):
                    hora = sibling.find("span").get_text(strip=True)
                    descricao = sibling.find_all("div")[1].get_text(" ", strip=True)
                    requisicao = {
                        "data": data_evento,
                        "hora": hora,
                        "descricao": descricao
                    }

                    texto_formatado = f"📦 Último evento:\n🗓 Data: {data_evento}\n⏰ Hora: {hora}\n📝 Descrição: {descricao}"

                    return requisicao, texto_formatado

    else:
        print("Erro ao coletar dados:", response.status_code)
        return None, None


# evento_json, evento_texto = coletar_ultimo_evento()

# print("JSON:", evento_json)
# print("Texto formatado:\n", evento_texto)

# # Enviar pelo Telegram, se quiser
# enviar_mensagem(evento_texto)


def monitorar_evento(intervalo_minutos=5, hora_esperada="08:11"):
    while True:
        evento_json, evento_texto = coletar_ultimo_evento()

        if evento_json:
            hora_evento = evento_json.get("hora", "")
            if hora_evento != hora_esperada:
                enviar_mensagem(evento_texto)
                print("Mensagem enviada:", evento_texto)
            else:
                print(f"Nenhuma alteração. Evento com hora esperada: {hora_evento}")
        else:
            print("Nenhum evento encontrado.")

        time.sleep(intervalo_minutos * 60)  # Aguarda X minutos antes da próxima verificação
if __name__ == "__main__":
    # Defina o intervalo de monitoramento em minutos
    intervalo_minutos = 5
    # Defina a hora esperada para o evento
    hora_esperada = "08:11"
    # Inicia o monitoramento
    monitorar_evento(intervalo_minutos, hora_esperada)