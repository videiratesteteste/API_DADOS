from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Carregar os dados CSV
dados = pd.read_csv('30.09.csv', sep=';', encoding='latin1', dtype=str)

@app.route('/buscar_cliente', methods=['GET'])
def receber():
    # Receber o JSON da requisição
    data = request.get_json()

    # Garantir que o campo 'document' existe no JSON
    if not data or 'document' not in data:
        return jsonify({'status': 'error', 'message': 'Documento não fornecido'}), 400
    
    doc = str(data['document'])

    # Filtrar os dados pelo documento
    resultado = dados.query(f"DOCUMENTO == '{doc}'")

    if not resultado.empty:
        # Converter o resultado filtrado para JSON no formato adequado
        json_dados = resultado.to_json(orient='records')
        retorno = {
            'status': 'success',
            'find': True,
            "body": json_dados
        }
    else:
        retorno = {
            'status': 'success',
            'find': False,
            "body": []
        }
    print(retorno)
    return jsonify(retorno), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7070, debug=True, use_reloader=True)
