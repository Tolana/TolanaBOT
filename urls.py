from my_db.db import DBManager


urls = []
urls.append('https://www.audible.com/series/Legend-of-Randidly-Ghosthound-Audiobooks/B09CTR3Q6K')
urls.append('https://www.audible.com/series/The-Primal-Hunter-Audiobooks/B09MZKWFTB')
urls.append('https://www.audible.com/series/Cradle-Audiobooks/B07GVRN95T')
urls.append('https://www.audible.com/series/Beware-of-Chicken-Audiobooks/B09Y5DYRBM')
urls.append('https://www.audible.com/series/Heirs-of-Sun-and-Storm-Audiobooks/B09X77P76R')
urls.append('https://www.audible.com/series/Immortal-Great-Souls-Audiobooks/B09RT8Z372')
urls.append('https://www.audible.com/series/The-Menocht-Loop-Audiobooks/B09JJKF1CS')
urls.append('https://www.audible.com/series/Murderbot-Diaries-Audiobooks/B07CJMTVQC')
urls.append('https://www.audible.com/series/Dungeon-Crawler-Carl-Audiobooks/B0937JMKYV')
urls.append('https://www.audible.com/series/Skyward-Audiobooks/B07JZCTPDR')
urls.append('https://www.audible.com/series/Blessed-Time-Audiobooks/B09KGP84DS')
urls.append('https://www.audible.com/series/Mage-Errant-Audiobooks/B07WJH9SKF')
urls.append('https://www.audible.com/series/Arcane-Ascension-Audiobooks/B0731RZ6L7')
urls.append('https://www.audible.com/series/Red-Rising-Audiobooks/B00U1UJCU8')
urls.append('https://www.audible.com/series/Stormweaver-Series-Audiobooks/B08V4VK4KZ')
urls.append('https://www.audible.com/series/Starships-Mage-Audiobooks/B0195SUQ6A')
urls.append('https://www.audible.com/series/Mistborn-Audiobooks/B006K1P698')
urls.append('https://www.audible.com/series/Siege-Audiobooks/B09N9VYV6G')
urls.append('https://www.audible.com/series/The-Dresden-Files-Audiobooks/B005NB2IG0')
urls.append('https://www.audible.com/series/Stormlight-Archive-Audiobooks/B006K1RP8I')

for url in urls:
    with DBManager('example.db') as cur:
        cur.execute(f'INSERT INTO url VALUES("{url}")')
    
