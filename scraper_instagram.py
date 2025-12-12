import instaloader
import pandas as pd
from datetime import datetime

# Lista de cuentas a analizar
ACCOUNTS = [
    "mum.mx",
    "lebump.oficial",
    "momanmx",
    "mumpreggo.gt",
    "labarriguitademama"
]

def scrape_instagram_data():

    L = instaloader.Instaloader(download_pictures=False,
                                download_videos=False,
                                download_video_thumbnails=False,
                                download_comments=False,
                                save_metadata=False,
                                compress_json=False)

    data_rows = []

    # Fecha de extracción
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    for username in ACCOUNTS:
        try:
            profile = instaloader.Profile.from_username(L.context, username)

            # Datos básicos
            followers = profile.followers
            following = profile.followees
            posts_count = profile.mediacount
            full_name = profile.full_name
            bio = profile.biography

            # Últimas 5 publicaciones
            posts = profile.get_posts()
            last_posts = []

            for i, post in enumerate(posts):
                if i >= 5:
                    break
                last_posts.append({
                    "post_shortcode": post.shortcode,
                    "post_date": post.date.strftime("%Y-%m-%d"),
                    "likes": post.likes,
                    "comments": post.comments,
                    "caption": post.caption[:120] if post.caption else ""  # solo primeras 120 letras
                })

            # Una fila por perfil
            data_rows.append({
                "username": username,
                "full_name": full_name,
                "biography": bio,
                "followers": followers,
                "following": following,
                "total_posts": posts_count,
                "timestamp": timestamp,
                "last_posts": last_posts
            })

            print(f"Datos obtenidos de {username}")

        except Exception as e:
            print(f"Error al procesar {username}: {e}")

    # Convertir a un dataframe plano
    df = pd.json_normalize(data_rows, "last_posts",
                           ["username", "full_name", "biography", "followers",
                            "following", "total_posts", "timestamp"])

    # Guardar CSV
    filename = f"instagram_data_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.csv"
    df.to_csv(filename, index=False)

    print(f"Archivo CSV guardado: {filename}")


if __name__ == "__main__":
    scrape_instagram_data()
