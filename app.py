import urllib.request, json
import streamlit as st

st.title("EDH OCTGN Deck Exporter")

texto = st.text_area("Paste your deck list here", height=300)

if st.button("Generate .o8d"):
    linhas = texto.strip().split("\n")
    if len(linhas) < 1:
        st.error("Please enter at least one card.")
    else:
        xml_inicio = """<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<deck game="a6c8d2e8-7cd8-11dd-8f94-e62b56d89593">
  <section name="Main" shared="False">"""
        xml_meio = ""
        xml_fim1 = """  </section>
  <section name="Sideboard" shared="False" />
  <section name="Command Zone" shared="False">"""
        xml_commander = ""
        xml_fim2 = """
  </section>
  <section name="Planes/Schemes" shared="False" />
  <notes><![CDATA[]]></notes>
</deck>"""

        for linha in linhas[:-1]:
            if not linha.strip():
                continue
            partes = linha.strip().split()
            quantidade = partes[0]
            nome = " ".join(partes[1:])
            processedname = nome.replace(" ", "%20")

            try:
                with urllib.request.urlopen(f"https://api.scryfall.com/cards/named?fuzzy={processedname}") as url:
                    data = json.load(url)
                    card_id = data["id"]
                    xml_meio += f'\n    <card qty="{quantidade}" id="{card_id}">{nome}</card>'
            except:
                st.error(f"Erro ao buscar: {nome}")

        ultima = linhas[-1].strip()
        partes = ultima.split()
        quantidade = partes[0]
        nome = " ".join(partes[1:])
        processedname = nome.replace(" ", "%20")

        try:
            with urllib.request.urlopen(f"https://api.scryfall.com/cards/named?fuzzy={processedname}") as url:
                data = json.load(url)
                card_id = data["id"]
                xml_commander = f'\n    <card qty="{quantidade}" id="{card_id}">{nome}</card>'
        except:
            st.error(f"Erro ao buscar comandante: {nome}")

        output = xml_inicio + xml_meio + "\n" + xml_fim1 + xml_commander + xml_fim2
        st.download_button("Download deck", output, file_name="deck.o8d")
