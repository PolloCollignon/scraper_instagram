import instaloader
import sqlite3
from datetime import datetime

# Lista de cuentas
ACCOUNTS = [
    "mum.mx",
    "lebump.oficial",
    "momanmx",
    "mumpreggo.gt",
    "labarriguitademama"
]

DB_NAME = "instagram.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS datos_instagram (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        username TEXT,
        full_name TEXT,
        biography TEXT,
        followers INTEGER,
        following INTEGER,
        total_posts INTEGER,
        post_shortcode TEXT UNIQUE,
        post_date TEXT,
        likes INTEGER,
        comments INTEGER,
        caption TEXT
    )
    """)

    conn.commit()
    return conn, cursor


def scrape_instagram_data():
    conn, cursor = init_db()

    L = instaloader.Instaloader(
        download_pictures=False,
        download_videos=False,
        download_video_thumbnails=False,
        download_comments=False,
        save_metadata=False,
        compress_json=False
    )

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    total_insertados = 0

    for username in ACCOUNTS:
        try:
            print(f"\n🔍 Scrapeando: {username}")

            profile = instaloader.Profile.from_username(L.context, username)

            followers = profile.followers
            following = profile.followees
            posts_count = profile.mediacount
            full_name = profile.full_name
            bio = profile.biography

            posts = profile.get_posts()

            encontrados = 0

            for i, post in enumerate(posts):
                if i >= 5:
                    break

                encontrados += 1

                cursor.execute("""
                INSERT OR IGNORE INTO datos_instagram (
                    timestamp, username, full_name, biography,
                    followers, following, total_posts,
                    post_shortcode, post_date, likes, comments, caption
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    timestamp,
                    username,
                    full_name,
                    bio,
                    followers,
                    following,
                    posts_count,
                    post.shortcode,
                    post.date.strftime("%Y-%m-%d"),
                    post.likes,
                    post.comments,
                    post.caption[:120] if post.caption else ""
                ))

                total_insertados += cursor.rowcount

            print(f"✅ {username} → {encontrados} posts encontrados")

        except Exception as e:
            print(f"❌ Error con {username}: {e}")

    # 🔍 DEBUG FINAL
    cursor.execute("SELECT COUNT(*) FROM datos_instagram")
    total_db = cursor.fetchone()[0]

    print(f"\n📊 TOTAL REGISTROS EN DB: {total_db}")
    print(f"🆕 INSERTADOS EN ESTA EJECUCIÓN: {total_insertados}")

    conn.commit()
    conn.close()

    print("💾 Datos guardados en instagram.db")


if __name__ == "__main__":
    scrape_instagram_data()
