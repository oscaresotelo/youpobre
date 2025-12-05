import streamlit as st
from youtube_search import YoutubeSearch
import streamlit.components.v1 as components

# =========================================================
#          🎨 ESTILO SPOTIFY — DISEÑO PREMIUM
# =========================================================
ui_css = """
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800;900&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background-color: #121212 !important;
    color: white !important;
    font-family: "Inter", sans-serif !important;
}

/* BARRA SUPERIOR */
h1 {
    font-weight: 900 !important;
    font-size: 42px !important;
    letter-spacing: -1px !important;
    color: white !important;
}

/* INPUT */
.stTextInput>div>div>input {
    background: #1E1E1E !important;
    border-radius: 14px !important;
    border: 1px solid #333 !important;
    padding: 12px 16px !important;
    color: white !important;
    font-size: 16px !important;
}

/* BOTÓN PLAY */
.stButton > button {
    background-color: #1DB954 !important;
    color: black !important;
    border-radius: 999px !important;
    padding: 10px 28px !important;
    font-weight: 700 !important;
    border: none !important;
    font-size: 17px !important;
    transition: 0.2s ease-in-out;
}
.stButton > button:hover {
    background-color: #1ED760 !important;
    transform: scale(1.06);
}

/* GRID */
.video-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 22px;
    margin-top: 30px;
}

/* TARJETAS */
.video-card {
    background: #181818;
    padding: 16px;
    border-radius: 20px;
    border: 1px solid #282828;
    transition: 0.25s;
    cursor: pointer;
    position: relative;
}

.video-card:hover {
    background: #202020;
    border-color: #1DB954;
    transform: translateY(-6px);
    box-shadow: 0px 6px 25px rgba(0,0,0,0.4);
}

/* MINIATURA */
.thumb {
    width: 100%;
    border-radius: 16px;
    margin-bottom: 12px;
    transition: 0.25s ease;
}

/* TÍTULO */
.video-title {
    font-size: 17px;
    font-weight: 700;
    margin-bottom: 6px;
}

/* INFORMACIÓN */
.video-info {
    font-size: 14px;
    opacity: 0.75;
}

/* BOTÓN PLAY SOBRE MINIATURA */
.play-btn {
    position: absolute;
    right: 22px;
    bottom: 90px;
    background: #1DB954;
    width: 54px;
    height: 54px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 28px;
    opacity: 0;
    transition: 0.25s;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.6);
}

.video-card:hover .play-btn {
    opacity: 1;
    transform: translateY(-4px);
}

.card-anim {
    animation: fadeUp 0.6s ease;
}
@keyframes fadeUp {
    0% { opacity: 0; transform: translateY(25px); }
    100% { opacity: 1; transform: translateY(0); }
}

</style>
"""

st.markdown(ui_css, unsafe_allow_html=True)

# =========================================================
#                FUNCION DE BUSQUEDA
# =========================================================
def buscar_videos(q, max_results):
    try:
        data = YoutubeSearch(q, max_results=max_results).to_dict()

        videos = []
        for item in data:
            videos.append({
                "id": item["id"],
                "title": item["title"],
                "channel": item.get("channel"),
                "duration": item.get("duration", "N/D"),
                "views": item.get("views", "N/D"),
                "thumb": item["thumbnails"][0],
            })
        return videos
    except Exception as e:
        st.error(f"Error: {e}")
        return []


# =========================================================
#                INTERFAZ PRINCIPAL
# =========================================================
st.title("🎵 Pobrefy — Tu Mini Spotify")

st.markdown("### Buscá cualquier canción 🎶")

query = st.text_input("🔍 Buscar en YouTube...")

MAX_RESULTS = 8

if st.button("Buscar"):
    if not query.strip():
        st.warning("Ingresá algo para buscar.")
    else:
        with st.spinner("Buscando..."):
            videos = buscar_videos(query, MAX_RESULTS)

        if videos:
            st.success(f"Encontrados {len(videos)} resultados.")

            html_items = """<div class='video-grid'>"""

            for idx, v in enumerate(videos):
                html_items += f"""
                <div class="video-card card-anim" style="animation-delay:{idx*0.13}s;">
                    <img src="{v['thumb']}" class="thumb"/>
                    <div class="play-btn">▶</div>

                    <div class="video-title">{v['title']}</div>
                    <div class="video-info">
                        🎤 {v['channel']}<br>
                        ⏱ {v['duration']} — 👁 {v['views']}
                    </div>

                    <iframe style="margin-top:12px; border-radius:16px;"
                        width="100%" height="240"
                        src="https://www.youtube.com/embed/{v['id']}?autoplay=0"
                        frameborder="0"
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                        allowfullscreen>
                    </iframe>
                </div>
                """

            html_items += "</div>"

            # RENDER HTML REAL, SIN QUE STREAMLIT ESCAPE TEXTO
            components.html(html_items, height=2000, scrolling=True)
