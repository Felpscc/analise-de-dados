from flask import Flask, render_template, jsonify
import requests
import pandas as pd
import matplotlib.pyplot as plt
from data_analysis import analyze_sales

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analises-venda')
def analises_venda():
    vendas = get_vendas()
    sales_summary = analyze_sales(vendas)
    create_sales_chart(sales_summary)
    return render_template('analises_venda.html', vendas=vendas, sales_summary=sales_summary)

@app.route('/mensagens')
def mensagens():
    return render_template('mensagens.html')

@app.route('/devolucoes')
def devolucoes():
    return render_template('devolucoes.html')

@app.route('/reclamacoes')
def reclamacoes():
    return render_template('reclamacoes.html')

@app.route('/api/vendas')
def api_vendas():
    vendas = get_vendas()
    return jsonify(vendas)




def get_vendas():
    url = "https://api.mercadolibre.com/sites/MLB/search?q=notebook"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        vendas = [{"produto": item["title"], "quantidade": item["available_quantity"], "valor": item["price"]}
                  for item in data["results"]]
        return vendas
    else:
        return {"error": "Failed to fetch data"}

def create_sales_chart(data):
    plt.figure(figsize=(10, 6))
    plt.bar(data['produto'], data['valor'])
    plt.xlabel('Produto')
    plt.ylabel('Valor de Vendas')
    plt.title('Vendas por Produto')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout(pad=3.0)  # Ajustar padding para garantir que o texto não seja cortado
    plt.savefig('static/sales_chart.png')
    plt.close()

if __name__ == '__main__':
    app.run(debug=True)
