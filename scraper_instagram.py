import instaloader
import pandas as pd
from datetime import datetime
import os

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
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    for username in ACCOUNTS:
        try:
            profile = instaloader.Profile.from_username(L.context, username)

            followers = profile.followers
            following = profile.followees
            posts_count = profile.mediacount
            full_name = profile.full_name
            bio = profile.biography

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
                    "caption": post.caption[:120] if post.caption else ""
                })

            for post_info in last_posts:
                data_rows.append({
                    "timestamp": timestamp,
                    "username": username,
                    "full_name": full_name,
                    "biography": bio,
                    "followers": followers,
                    "following": following,
                    "total_posts": posts_count,
                    **post_info
                })

            print(f"Datos obtenidos de {username}")

        except Exception as e:
            print(f"Error al procesar {username}: {e}")

    df_new = pd.DataFrame(data_rows)

    # Cargar histórico anterior si existe
    historico_file = "historico_instagram.csv"

    if os.path.exists(historico_file):
        df_old = pd.read_csv(historico_file)
        df_final = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df_final = df_new

    # Guardar histórico actualizado
    df_final.to_csv(historico_file, index=False)

    print(f"Histórico actualizado: {historico_file}")


if __name__ == "__main__":
    scrape_instagram_data()
