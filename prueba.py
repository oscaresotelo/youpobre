from youtube_search import YoutubeSearch

def buscar_videos(query, cantidad=20):
    resultados = YoutubeSearch(query, max_results=cantidad).to_dict()

    for i, video in enumerate(resultados, start=1):
        print(f"{i}. {video['title']}")
        print(f"   URL: https://www.youtube.com/watch?v={video['id']}")
        print(f"   Duración: {video['duration']}")
        print("-" * 60)

buscar_videos("tutorial streamlit", cantidad=10)
