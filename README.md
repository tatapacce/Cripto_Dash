Estrutura do projeto;
 - main.py
    Arquivo principal que executa o dashboard com Streamlit. Controla a interface, carrega dados via API e renderiza os gráficos de preços.

 - layout.py
    Contém funções separadas para organização do layout visual, estilo personalizado e componentes reutilizáveis (como seleção de moedas, gráficos e cards de preço).

 - data (ou função de coleta de dados)
    Função dentro de main.py responsável por buscar o histórico de preços das criptomoedas via API do CoinGecko. Utiliza cache e controle de tentativa para evitar bloqueios por excesso de requisições.
