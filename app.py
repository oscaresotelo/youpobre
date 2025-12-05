import streamlit as st
from youtubesearchpython import SearchVideos
import json

# =========================================================
#                🎨 ESTILO SPOTIFY AJUSTADO
# =========================================================
spotify_css = """
<style>

/* ------- BACKGROUND GENERAL ------- */
[data-testid="stAppViewContainer"] {
    background-color: #121212 !important;
    color: #FFFFFF !important;
    font-family: "Helvetica Neue", Arial, sans-serif;
}

/* ------- TITULO PRINCIPAL ------- */
h1 {
    font-weight: 800 !important;
    letter-spacing: -1px !important;
    color: white !important;
}

/* ------- INPUT ------- */
.stTextInput>div>div>input {
    background-color: #181818 !important;
    color: #FFFFFF !important;
    border-radius: 8px !important;
    border: 1px solid #282828 !important;
    padding: 12px !important;
}

/* ------- BOTÓN VERDE SPOTIFY ------- */
.stButton > button {
    background-color: #1DB954 !important;
    color: #000000 !important;
    border-radius: 30px !important;
    padding: 10px 25px !important;
    font-weight: bold !important;
    border: none !important;
    font-size: 16px !important;
    transition: 0.2s;
}
.stButton > button:hover {
    background-color: #1ED760 !important;
    transform: scale(1.03);
}

/* ------- TARJETAS DE VIDEO ------- */
.video-card {
    background-color: #181818;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #282828;
    margin-bottom: 25px;
    transition: all 0.20s ease-in-out;
}

.video-card:hover {
    background-color: #1E1E1E;
    transform: scale(1.01);
    border: 1px solid #1DB954;
}

</style>
"""
st.markdown(spotify_css, unsafe_allow_html=True)

# =========================================================
#                      APLICACIÓN
# =========================================================
MAX_RESULTS = 5

def youtube_search_no_api(q, max_results):
    try:
        search = SearchVideos(q, offset=1, mode="json", max_results=max_results)
        data = json.loads(search.result())

        videos = []
        for item in data.get('search_result', []):
            videos.append({
                "title": item.get('title'),
                "duration": item.get('duration'),
                "views": item.get('views'),
                "channel": item.get('channel'),
                "url": item.get('link')
            })
        return videos

    except Exception as e:
        st.error(f"Ocurrió un error: {e}")
        return []

# =========================================================
#                    INTERFAZ PRINCIPAL
# =========================================================
st.title("🎵 Pobrefy")
st.markdown("---")

search_query = st.text_input("🔍 ¿Qué querés escuchar?")

if st.button(f"Buscar {MAX_RESULTS} Videos"):
    if search_query:
        with st.spinner(f"Buscando '{search_query}'..."):
            results = youtube_search_no_api(search_query, MAX_RESULTS)

            if results:
                st.success(f"{len(results)} videos encontrados.")
                st.markdown("---")

                for video in results:
                    st.markdown("<div class='video-card'>", unsafe_allow_html=True)

                    st.subheader(video["title"])
                    st.caption(
                        f"🎤 {video['channel']} — ⏱ {video['duration']} — 👁 {video['views']}"
                    )

                    # === REPRODUCTOR SIN MENSAJE DE "VIDEO NO DISPONIBLE" ===
                    try:
                        youtube_id = video["url"].split("v=")[-1].split("&")[0]

                        embed_code = f"""
                        <iframe 
                            width="100%" 
                            height="320" 
                            src="https://www.youtube.com/embed/{youtube_id}?autoplay=0"
                            frameborder="0"
                            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                            allowfullscreen>
                        </iframe>
                        """

                        st.markdown(embed_code, unsafe_allow_html=True)

                    except:
                        st.write("⚠️ No se pudo cargar el reproductor.")

                    #st.write(f"[Abrir en YouTube]({video['url']})")

                    st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.warning("No se encontraron resultados.")
    else:
        st.info("Ingresá algo para buscar.")
