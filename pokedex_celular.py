import os
import requests
import streamlit as st

# Configurações da página (simula a largura/tema do celular no navegador)
st.set_page_config(page_title="Pokédex do Sheta", page_icon="📱", layout="centered")

# Título estilizado em vermelho (HTML embutido para manter o 'redaccent')
st.markdown("<h1 style='color: #ff5252; font-size: 28px; font-weight: bold;'>Pokédex Pra Esse Celular de Pobre</h1>", unsafe_allow_html=True)

# Entrada do usuário
entrada_nome = st.text_input(
    label="Nome do Pokémon", 
    placeholder="Ex: pikachu, sua mãe e etc...",
    help="Insira o nome exatamente como solicitado abaixo."
).strip().lower()

# Botão de busca
botao_buscar = st.button("Procurar Se Tem Essa Merda na Lista", use_container_width=True)

# Container do resultado (Inicia com o texto padrão caso não haja busca)
texto_padrao = "Digite o nome do Pokémon, sem parecer um analfabeto"

if botao_buscar and entrada_nome:
    url = f"https://pokeapi.co/api/v2/pokemon/{entrada_nome}"
    
    # Simula o texto de carregamento antes da requisição
    with st.spinner("Buscando esse caraio, seu preguiçoso..."):
        resposta = requests.get(url)

    if resposta.status_code == 200:
        dados = resposta.json()
        peso = dados["weight"] / 10
        altura = dados["height"] / 10
        habilidades = [item["ability"]["name"].capitalize() for item in dados["abilities"]]
        
        # Formatação exata das suas strings de saída
        texto_sucesso = (
            f"ID do bostinha: #{dados['id']}\n\n"
            f"Nome desse lixo: {entrada_nome.upper()}\n\n"
            f"Altura pra saber se cabe numa gaiola: {altura:.2f} m\n\n"
            f"Peso desse monte de bosta: {peso:.1f} kg\n\n"
            f"Poderzin do idiota:\n" + ", ".join(habilidades)
        )
        
        # Exibe a imagem caso exista
        url_img = dados["sprites"]["front_default"]
        if url_img:
            # Centraliza a imagem usando colunas do Streamlit
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image(url_img, width=180)
        
        # Caixa cinza estilizada imitando o 'surfacevariant' do Flet
        st.info(texto_sucesso)
        
    else:
        # Mensagem de erro idêntica à sua
        st.error("❌ Pokémon não encontrado, seu burro! Escreve direito essa merda, por favor.")
        
elif not entrada_nome:
    # Mostra o container padrão se o usuário não buscou nada ainda
    st.info(texto_padrao)
