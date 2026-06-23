import io
import requests
from PIL import Image
import flet as ft

def main(page: ft.Page):
    # Configurações da tela para parecer um celular
    page.title = "Pokédex do Sheta"
    page.window_width = 380
    page.window_height = 680
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO
    page.theme_mode = ft.ThemeMode.DARK

    # Componentes Visuais (Frontend) - Atualizado com as cores novas
    titulo = ft.Text("Pokédex Pra Esse Celular de Pobre", size=28, weight=ft.FontWeight.BOLD, color="redaccent")
    
    entrada_nome = ft.TextField(
        label="Nome do Pokémon", 
        hint_text="Ex: pikachu, sua mãe e etc...", 
        width=300,
        border_radius=10
    )
    
    imagem_pokemon = ft.Image(src="https://pokeapi.co/static/sprite/xyz.png", width=180, height=180, visible=False)
    text_resultado = ft.Text("Digite o nome do Pokémon, sem parecer um analfabeto", size=14, text_align=ft.TextAlign.CENTER)

    def buscar_pokemon(e):
        nome = entrada_nome.value.strip().lower()
        if not nome:
            return
        
        text_resultado.value = "Buscando esse caraio, seu preguiçoso..."
        page.update()

        url = f"https://pokeapi.co/api/v2/pokemon/{nome}"
        resposta = requests.get(url)

        if resposta.status_code == 200:
            dados = resposta.json()
            peso = dados["weight"] / 10
            altura = dados["height"] / 10
            habilidades = [item["ability"]["name"].capitalize() for item in dados["abilities"]]

            # Atualiza o texto do app
            text_resultado.value = (
                f"ID do bostinha: #{dados['id']}\n"
                f"Nome desse lixo: {nome.upper()}\n\n"
                f"Altura pra saber se cabe numa gaiola: {altura:.2f} m\n"
                f"Peso desse monte de bosta: {peso:.1f} kg\n\n"
                f"Poderzin do idiota:\n" + ", ".join(habilidades)
            )
            
            # Atualiza a imagem direto pela URL da API
            url_img = dados["sprites"]["front_default"]
            if url_img:
                imagem_pokemon.src = url_img
                imagem_pokemon.visible = True
            else:
                imagem_pokemon.visible = False
        else:
            text_resultado.value = "❌ Pokémon não encontrado, seu burro! Escreve direito essa merda, por favor."
            imagem_pokemon.visible = False
            
        page.update()

    # Vincula o botão e o "Enter" do teclado à função de busca
    botao_buscar = ft.ElevatedButton(
        "Procurar Se Tem Essa Merda na Lista", 
        on_click=buscar_pokemon, 
        width=300, 
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
    )
    entrada_nome.on_submit = buscar_pokemon

    # Adiciona os elementos na tela do celular - Corrigido para "surfacevariant"
    page.add(
        ft.Container(height=20),
        titulo,
        ft.Container(height=10),
        entrada_nome,
        botao_buscar,
        ft.Container(height=20),
        imagem_pokemon,
        ft.Container(
            content=text_resultado,
            padding=20,
            bgcolor="surfacevariant",
            border_radius=15,
            width=320
        )
    )

import os

if __name__ == "__main__":
    porta = int(os.environ.get("PORT", 8080))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=porta)
