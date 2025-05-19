import requests
import json
import time
from datetime import datetime
import random

class PlantinhaDoConhecimento:
    def __init__(self):
        self.api_key = ""  # Substitua pela sua API key real
        self.nivel_crescimento = 0
        self.ultima_alimentacao = None
        self.assuntos = {
            "Matemática": ["Álgebra", "Geometria", "Cálculo", "Estatística", "Trigonometria"],
            "Português": ["Gramática", "Literatura", "Redação", "Interpretação de Texto", "Ortografia"],
            "Ciências": ["Biologia", "Física", "Química", "Astronomia", "Ecologia"],
            "História": ["Brasil", "Mundial", "Antiga", "Contemporânea", "Cultura"],
            "Geografia": ["Física", "Humana", "Brasil", "Mundo", "Cartografia"]
        }
        self.plantas_estagios = [
            "🌱",  # Estágio 1
            "🌿",  # Estágio 2
            "🍀",  # Estágio 3
            "🌴",  # Estágio 4
            "🌳"   # Estágio 5 (completo)
        ]
    
    def consultar_gemini(self, assunto, topico):
        base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
        url = f"{base_url}?key={self.api_key}"
        
        prompt = f"Explique de forma simples e resumida (em 2-3 frases) sobre {topico} na disciplina de {assunto} para estudantes."
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }]
        }
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            resposta = response.json()
            
            if 'candidates' in resposta and resposta['candidates']:
                texto_resposta = resposta['candidates'][0]['content']['parts'][0]['text']
                return texto_resposta
            else:
                return "Não foi possível obter uma resposta do Gemini."
        
        except Exception as e:
            return f"Erro ao consultar a API: {str(e)}"
    
    def alimentar_plantinha(self):
        hoje = datetime.now().date()
        
        if self.ultima_alimentacao == hoje:
            print("\nVocê já alimentou sua plantinha hoje! Volte amanhã.")
            return
        
        # Escolhe um assunto e tópico aleatório
        assunto = random.choice(list(self.assuntos.keys()))
        topico = random.choice(self.assuntos[assunto])
        
        print(f"\nHoje vamos aprender sobre: {topico} em {assunto}!")
        input("Pressione Enter para buscar conhecimento...")
        
        # Consulta o Gemini
        conhecimento = self.consultar_gemini(assunto, topico)
        print("\n💡 Conhecimento adquirido:")
        print(conhecimento)
        
        # Atualiza a plantinha
        self.nivel_crescimento += 1
        self.ultima_alimentacao = hoje
        print(f"\nSua plantinha cresceu! Nível atual: {self.nivel_crescimento}/5")
        self.mostrar_planta()
    
    def mostrar_planta(self):
        estagio = min(self.nivel_crescimento, len(self.plantas_estagios)) - 1
        estagio = max(0, estagio)
        print(f"\nSua plantinha: {self.plantas_estagios[estagio]}")
        
        if self.nivel_crescimento >= 5:
            print("\n🎉 Parabéns! Sua plantinha está completamente crescida!")
            print("Você demonstrou compromisso diário com o aprendizado!")
    
    def status(self):
        print("\n=== Status da Plantinha do Conhecimento ===")
        self.mostrar_planta()
        if self.ultima_alimentacao:
            print(f"Última alimentação: {self.ultima_alimentacao}")
        else:
            print("Você ainda não alimentou sua plantinha hoje.")
        print(f"Dias consecutivos: {self.nivel_crescimento}")

def main():
    print("🌱 Bem-vindo à Plantinha do Conhecimento! 🌱")
    print("Alimente sua plantinha diariamente com conhecimento para vê-la crescer!")
    
    plantinha = PlantinhaDoConhecimento()
    
    while True:
        print("\nMenu:")
        print("1. Alimentar a plantinha (buscar conhecimento)")
        print("2. Ver status")
        print("3. Sair")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            plantinha.alimentar_plantinha()
        elif opcao == "2":
            plantinha.status()
        elif opcao == "3":
            print("Obrigado por cuidar da Plantinha do Conhecimento! Até mais!")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
