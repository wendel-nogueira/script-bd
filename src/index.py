import requests
import json
from bs4 import BeautifulSoup
import re
from peewee import *
import os
from dotenv import load_dotenv

load_dotenv()


class Database:
    def __init__(self):
        self.database = PostgresqlDatabase(
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
        )

        try:
            self.database.connect()
        except:
            print('Não foi possível conectar ao banco de dados!')

    def close(self):
        self.database.close()
        print('Conexão com o banco de dados encerrada!')

    def table_exists(self, table_name):
        return self.database.table_exists(table_name, schema='private')

    def getDatabase(self):
        return self.database


class Consumer:
    def __init__(self):
        self.url = 'https://valorant-api.com/v1/'
        self. resources = {
            'buddies': 'buddies',
            'bundles': 'bundles',
            'content_tiers': 'contentTiers',
            'player_cards': 'playerCards',
            'player_titles': 'playerTitles',
            'sprays': 'sprays',
            'themes': 'themes',
            'weapons': 'weapons',
            'tiers': 'contenttiers'
        }

    def get(self, resource):
        return requests.get(self.url + resource).json()

    def getByUUID(self, resource, uuid):
        return requests.get(self.url + resource + '/' + uuid).json()

    def getAllWeaponsAndSkins(self):
        weaponsApi = self.get(self.resources['weapons']).get('data')
        weaponsObj = []

        for weapon in weaponsApi:
            if (weapon != None):
                weaponObj = {
                    'uuid': weapon.get('uuid'),
                    'displayName': weapon.get('displayName') if weapon.get('displayName') else '',
                    'category': weapon.get('shopData').get('category') if weapon.get('shopData') else weapon.get('category'),
                    'displayIcon': weapon.get('displayIcon').replace('displayicon.png', '') if weapon.get('displayIcon') else '',
                }

                # Get Weapon Details
                weaponInfo = {
                    'shopCost': weapon.get('shopData').get('cost') if weapon.get('shopData') else None,
                    'fireRate': weapon.get('weaponStats').get('fireRate') if weapon.get('weaponStats') else None,
                    'magazineSize': weapon.get('weaponStats').get('magazineSize') if weapon.get('weaponStats') else None,
                    'runSpeedMultiplier': weapon.get('weaponStats').get('runSpeedMultiplier') if weapon.get('weaponStats') else None,
                    'equipTimeSeconds': weapon.get('weaponStats').get('equipTimeSeconds') if weapon.get('weaponStats') else None,
                    'reloadTimeSeconds': weapon.get('weaponStats').get('reloadTimeSeconds') if weapon.get('weaponStats') else None,
                    'firstBulletAccuracy': weapon.get('weaponStats').get('firstBulletAccuracy') if weapon.get('weaponStats') else None,
                    'shotgunPelletCount': weapon.get('weaponStats').get('shotgunPelletCount') if weapon.get('weaponStats') else None,
                }

                weaponObj.update({'weaponInfo': weaponInfo})

                # Get Skins
                skinsObj = []

                for skin in weapon.get('skins'):
                    tier = self.getByUUID(self.resources['tiers'], skin.get('contentTierUuid')).get('data') if skin.get('contentTierUuid') else None

                    skinObj = {
                        'uuid': skin.get('uuid'),
                        'idBundle': '',
                        'idWeapon': weapon.get('uuid'),
                        'displayName': skin.get('displayName') if skin.get('displayName') else '',
                        'tier': tier.get('displayName') if tier else '',
                        'theme': skin.get('themeUuid') if skin.get('themeUuid') else '',
                        'icon': skin.get('displayIcon').replace('displayicon.png', '') if skin.get('displayIcon') else '',
                    }

                    skinsObj.append(skinObj)

                    # Get Theme
                    theme = self.getByUUID(
                        self.resources['themes'], skin.get('themeUuid')).get('data')

                    if (theme != None):
                        skinObj.update(
                            {'theme': theme.get('displayName')})

                    # Get Chromas
                    chromasObj = []

                    for chroma in skin.get('chromas'):
                        chromaObj = {
                            'uuid': chroma.get('uuid'),
                            'idSkin': skin.get('uuid'),
                            'displayName': chroma.get('displayName') if chroma.get('displayName') else '',
                            'icon': chroma.get('displayIcon').replace('displayicon.png', '') if chroma.get('displayIcon') else '',
                        }

                        chromasObj.append(chromaObj)

                    skinObj.update({'chromas': chromasObj})

                    # Get Levels
                    levelsObj = []

                    for level in skin.get('levels'):
                        levelObj = {
                            'uuid': level.get('uuid'),
                            'idSkin': skin.get('uuid'),
                            'displayName': level.get('displayName') if level.get('displayName') else '',
                            'icon': level.get('displayIcon').replace('displayicon.png', '') if level.get('displayIcon') else '',
                        }

                        levelsObj.append(levelObj)

                    skinObj.update({'levels': levelsObj})

                weaponObj.update({'skins': skinsObj})
                weaponsObj.append(weaponObj)

        return weaponsObj

    def getAllBundles(self):
        bundlesApi = self.get(self.resources['bundles']).get('data')
        bundlesObj = []

        for bundle in bundlesApi:
            if (bundle != None):
                bundleObj = {
                    'uuid': bundle.get('uuid'),
                    'displayName': bundle.get('displayName') if bundle.get('displayName') else '',
                    'description': bundle.get('description') if bundle.get('description') else '',
                    'displayIcon': bundle.get('displayIcon').replace('displayicon.png', '') if bundle.get('displayIcon') else '',
                }

                bundlesObj.append(bundleObj)

        return bundlesObj

    def getAllSprays(self):
        spraysApi = self.get(self.resources['sprays']).get('data')
        spraysObj = []

        for spray in spraysApi:
            if (spray != None):
                sprayObj = {
                    'uuid': spray.get('uuid'),
                    'idBundle': '',
                    'displayName': spray.get('displayName') if spray.get('displayName') else '',
                    'category': spray.get('category') if spray.get('category') else '',
                    'theme': spray.get('themeUuid') if spray.get('themeUuid') else '',
                    'icon': spray.get('displayIcon').replace('displayicon.png', '') if spray.get('displayIcon') else '',
                    'animation': spray.get('animationPng').replace('animation.png', '') if spray.get('animationPng') else '',
                }

                spraysObj.append(sprayObj)

        return spraysObj

    def getAllTitles(self):
        playerTitlesApi = self.get(self.resources['player_titles']).get('data')
        playerTitlesObj = []

        for playerTitle in playerTitlesApi:
            if (playerTitle != None):
                playerTitleObj = {
                    'uuid': playerTitle.get('uuid'),
                    'idBundle': '',
                    'displayName': playerTitle.get('displayName') if playerTitle.get('displayName') else '',
                    'titleText': playerTitle.get('titleText') if playerTitle.get('titleText') else '',
                }

                playerTitlesObj.append(playerTitleObj)

        return playerTitlesObj

    def getAllPlayerCards(self):
        playerCardsApi = self.get(self.resources['player_cards']).get('data')
        playerCardsObj = []

        for playerCard in playerCardsApi:
            if (playerCard != None):
                playerCardObj = {
                    'uuid': playerCard.get('uuid'),
                    'idBundle': '',
                    'theme': playerCard.get('themeUuid') if playerCard.get('themeUuid') else '',
                    'displayName': playerCard.get('displayName') if playerCard.get('displayName') else '',
                    'icon': playerCard.get('displayIcon').replace('displayicon.png', '') if playerCard.get('displayIcon') else '',
                }

                playerCardsObj.append(playerCardObj)

        return playerCardsObj

    def getAllBuddies(self):
        buddiesApi = self.get(self.resources['buddies']).get('data')
        buddiesObj = []

        for buddy in buddiesApi:
            if (buddy != None):
                buddyObj = {
                    'uuid': buddy.get('uuid'),
                    'idBundle': '',
                    'theme': buddy.get('themeUuid') if buddy.get('themeUuid') else '',
                    'displayName': buddy.get('displayName') if buddy.get('displayName') else '',
                    'icon': buddy.get('displayIcon').replace('displayicon.png', '') if buddy.get('displayIcon') else '',
                }

                # Get Theme
                if (buddyObj['theme'] != ''):
                    theme = self.getByUUID(
                        self.resources['themes'], buddyObj['theme']).get('data')

                    if (theme != None):
                        buddyObj.update(
                            {'theme': theme.get('displayName')})

                buddiesObj.append(buddyObj)

        return buddiesObj

    def getAllSkinsPrice(self):
        page = requests.get('https://valorant.fandom.com/wiki/Weapon_Skins')
        soup = BeautifulSoup(page.content, 'html.parser')
        tables = soup.find_all('table', class_='wikitable')

        skinsPriceObj = []

        for i in range(len(tables)):
            if (i == 1 or i == 4):
                for row in tables[i].find_all('tr'):
                    cells = row.find_all('td')

                    if (len(cells) > 0):
                        price = cells[4].text.strip(
                        ) if i == 1 else cells[3].text.strip()
                        price = price.replace('2021', '').replace('2022', '')
                        price = re.sub('[^0-9]', '', price)

                        weapon = cells[3].find(
                            'a')['title'] if i == 1 else cells[2].find('a')['title']
                        weapon = 'Melee' if weapon == 'Tactical Knife' else weapon

                        skinPriceObj = {
                            'displayName': cells[2].text.strip(),
                            'price': price if price != '' else '0',
                            'weapon': weapon,
                        }

                        skinsPriceObj.append(skinPriceObj)

        return skinsPriceObj


def verifyTablesExists(database, databaseTables):
    if (database.table_exists(databaseTables['weapons'])):
        pass
    else:
        print('Tabela {} não existe'.format(databaseTables['weapons']))
        exit()

    if (database.table_exists(databaseTables['weaponsinfo'])):
        pass
    else:
        print('Tabela {} não existe'.format(databaseTables['weaponsinfo']))
        exit()

    if (database.table_exists(databaseTables['skins'])):
        pass
    else:
        print('Tabela {} não existe'.format(databaseTables['skins']))
        exit()

    if (database.table_exists(databaseTables['chromas'])):
        pass
    else:
        print('Tabela {} não existe'.format(databaseTables['chromas']))
        exit()

    if (database.table_exists(databaseTables['levels'])):
        pass
    else:
        print('Tabela {} não existe'.format(databaseTables['levels']))
        exit()

    if (database.table_exists(databaseTables['bundles'])):
        pass
    else:
        print('Tabela {} não existe'.format(databaseTables['bundles']))
        exit()

    if (database.table_exists(databaseTables['sprays'])):
        pass
    else:
        print('Tabela {} não existe'.format(databaseTables['sprays']))
        exit()

    if (database.table_exists(databaseTables['titles'])):
        pass
    else:
        print('Tabela {} não existe'.format(databaseTables['titles']))
        exit()

    if (database.table_exists(databaseTables['buddies'])):
        pass
    else:
        print('Tabela {} não existe'.format(databaseTables['buddies']))
        exit()

    if (database.table_exists(databaseTables['cards'])):
        pass
    else:
        print('Tabela {} não existe'.format(databaseTables['cards']))
        exit()


def collectData(consumer):
    info = {}

    try:
        weaponsAndSkins = consumer.getAllWeaponsAndSkins()
        info.update({'weaponsAndSkins': weaponsAndSkins})
    except Exception as e:
        print('Erro ao coletar as armas e skins!')
        print(e)
        exit()

    try:
        bundles = consumer.getAllBundles()
        info.update({'bundles': bundles})
    except Exception as e:
        print('Erro ao coletar os bundles!')
        print(e)
        exit()

    try:
        sprays = consumer.getAllSprays()
        info.update({'sprays': sprays})
    except Exception as e:
        print('Erro ao coletar os sprays!')
        print(e)
        exit()

    try:
        titles = consumer.getAllTitles()
        info.update({'titles': titles})
    except Exception as e:
        print('Erro ao coletar os títulos!')
        print(e)
        exit()

    try:
        buddies = consumer.getAllBuddies()
        info.update({'buddies': buddies})
    except Exception as e:
        print('Erro ao coletar os buddies!')
        print(e)
        exit()

    try:
        cards = consumer.getAllPlayerCards()
        info.update({'cards': cards})
    except Exception as e:
        print('Erro ao coletar os cards!')
        print(e)
        exit()

    try:
        skinsPrice = consumer.getAllSkinsPrice()
        info.update({'skinsPrice': skinsPrice})
    except Exception as e:
        print('Erro ao coletar os preços das skins!')
        print(e)
        exit()

    return info


def saveData(database, databaseTables, schema, info):
    for bundle in info['bundles']:
        database.execute_sql('insert into {} (id, name, description, icon) values (%(id)s, %(name)s, %(description)s, %(icon)s)'.format(
            schema + '.' + databaseTables['bundles']
        ), {
            'id': bundle['uuid'],
            'name': bundle['displayName'],
            'description': bundle['description'],
            'icon': bundle['displayIcon'],
        })

    for weapon in info['weaponsAndSkins']:
        database.execute_sql('insert into {} (id, name, category, icon) values (%(id)s, %(name)s, %(category)s, %(icon)s)'.format(
            schema + '.' + databaseTables['weapons']
        ), {
            'id': weapon['uuid'],
            'name': weapon['displayName'],
            'category': weapon['category'],
            'icon': weapon['displayIcon'],
        })

        if (weapon['weaponInfo']):
            for key, value in weapon['weaponInfo'].items():
                database.execute_sql('insert into {} (id_weapon, info) values (%(id_weapon)s, %(info)s)'.format(
                    schema + '.' + databaseTables['weaponsinfo']
                ), {
                    'id_weapon': weapon['uuid'],
                    'info': str(key) + ': ' + str(value),
                })

        if (weapon['skins']):
            for skin in weapon['skins']:
                cursor = database.execute_sql('select id from {} where name like %(name)s'.format(
                    schema + '.' + databaseTables['bundles']
                ), {
                    'name': '%' + skin['theme'] + '%'
                })

                if (cursor.rowcount > 0):
                    database.execute_sql('insert into {} (id, id_bundle, id_weapon, name, tier, theme, icon) values (%(id)s, %(id_bundle)s, %(id_weapon)s, %(name)s, %(tier)s, %(theme)s, %(icon)s)'.format(
                        schema + '.' + databaseTables['skins']
                    ), {
                        'id': skin['uuid'],
                        'id_bundle': cursor.fetchall()[0][0],
                        'id_weapon': skin['idWeapon'],
                        'name': skin['displayName'],
                        'tier': skin['tier'],
                        'theme': skin['theme'],
                        'icon': skin['icon']
                    })
                else:
                    database.execute_sql('insert into {} (id, id_weapon, name, tier, theme, icon) values (%(id)s, %(id_weapon)s, %(name)s, %(tier)s, %(theme)s, %(icon)s)'.format(
                        schema + '.' + databaseTables['skins']
                    ), {
                        'id': skin['uuid'],
                        'id_weapon': skin['idWeapon'],
                        'name': skin['displayName'],
                        'tier': skin['tier'],
                        'theme': skin['theme'],
                        'icon': skin['icon']
                    })

                if (skin['chromas']):
                    for chroma in skin['chromas']:
                        database.execute_sql('insert into {} (id_skin, name, icon) values (%(id_skin)s, %(name)s, %(icon)s)'.format(
                            schema + '.' + databaseTables['chromas']
                        ), {
                            'id_skin': chroma['idSkin'],
                            'name': chroma['displayName'],
                            'icon': chroma['icon']
                        })

                if (skin['levels']):
                    for level in skin['levels']:
                        database.execute_sql('insert into {} (id_skin, name, icon) values (%(id_skin)s, %(name)s, %(icon)s)'.format(
                            schema + '.' + databaseTables['levels']
                        ), {
                            'id_skin': chroma['idSkin'],
                            'name': level['displayName'],
                            'icon': level['icon']
                        })

    for price in info['skinsPrice']:
        cursor = database.execute_sql('select ps.id, ps.name from {} ps join {} pb on ps.id_bundle = pb.id join {} pw on ps.id_weapon = pw.id where pw.name like %(weaponname)s and ps.theme like %(theme)s'.format(
            schema + '.' + databaseTables['skins'],
            schema + '.' + databaseTables['bundles'],
            schema + '.' + databaseTables['weapons']
        ), {
            'weaponname': '%' + price['weapon'] + '%',
            'theme': '%' + price['displayName'] + '%'
        })

        if (cursor.rowcount > 0):
            idSkin = cursor.fetchall()[0][0]
            database.execute_sql('update {} set price = %(price)s where id = %(id)s'.format(
                schema + '.' + databaseTables['skins']
            ), {
                'id': idSkin,
                'price': float(price['price'])
            })

    for spray in info['sprays']:
        cursor = database.execute_sql('select id from {} where name like %(name)s'.format(
            schema + '.' + databaseTables['bundles']
        ), {
            'name': '%' + spray['theme'] + '%'
        })

        if (cursor.rowcount > 0):
            database.execute_sql('insert into {} (id, id_bundle, name, category, theme, icon, animation) values (%(id)s, %(id_bundle)s, %(name)s, %(category)s, %(theme)s, %(icon)s, %(animation)s)'.format(
                schema + '.' + databaseTables['sprays']
            ), {
                'id': spray['uuid'],
                'id_bundle': cursor.fetchall()[0][0],
                'name': spray['displayName'],
                'category': spray['category'],
                'theme': spray['theme'],
                'icon': spray['icon'],
                'animation': spray['animation'],
            })
        else:
            database.execute_sql('insert into {} (id, name, category, theme, icon, animation) values (%(id)s, %(name)s, %(category)s, %(theme)s, %(icon)s, %(animation)s)'.format(
                schema + '.' + databaseTables['sprays']
            ), {
                'id': spray['uuid'],
                'name': spray['displayName'],
                'category': spray['category'],
                'theme': spray['theme'],
                'icon': spray['icon'],
                'animation': spray['animation'],
            })

    for title in info['titles']:
        cursor = database.execute_sql('select id from {} where name like %(name)s'.format(
            schema + '.' + databaseTables['bundles']
        ), {
            'name': '%' + title['titleText'] + '%'
        })

        if (cursor.rowcount > 0):
            database.execute_sql('insert into {} (id, id_bundle, name, txt) values (%(id)s, %(id_bundle)s, %(name)s, %(txt)s)'.format(
                schema + '.' + databaseTables['titles']
            ), {
                'id': title['uuid'],
                'id_bundle': cursor.fetchall()[0][0],
                'name': title['displayName'],
                'txt': title['titleText']
            })
        else:
            database.execute_sql('insert into {} (id, name, txt) values (%(id)s, %(name)s, %(txt)s)'.format(
                schema + '.' + databaseTables['titles']
            ), {
                'id': title['uuid'],
                'name': title['displayName'],
                'txt': title['titleText']
            })

    for buddy in info['buddies']:
        cursor = database.execute_sql('select id from {} where name like %(name)s'.format(
            schema + '.' + databaseTables['bundles']
        ), {
            'name': '%' + buddy['theme'] + '%'
        })

        if (cursor.rowcount > 0):
            database.execute_sql('insert into {} (id, id_bundle, theme, icon, name) values (%(id)s, %(id_bundle)s, %(theme)s, %(icon)s, %(name)s)'.format(
                schema + '.' + databaseTables['buddies']
            ), {
                'id': buddy['uuid'],
                'id_bundle': cursor.fetchall()[0][0],
                'theme': buddy['theme'],
                'icon': buddy['icon'],
                'name': buddy['displayName']
            })
        else:
            database.execute_sql('insert into {} (id, theme, icon, name) values (%(id)s, %(theme)s, %(icon)s, %(name)s)'.format(
                schema + '.' + databaseTables['buddies']
            ), {
                'id': buddy['uuid'],
                'theme': buddy['theme'],
                'icon': buddy['icon'],
                'name': buddy['displayName']
            })

    for card in info['cards']:
        cursor = database.execute_sql('select id from {} where name like %(name)s'.format(
            schema + '.' + databaseTables['bundles']
        ), {
            'name': '%' + card['theme'] + '%'
        })

        if (cursor.rowcount > 0):
            database.execute_sql('insert into {} (id, id_bundle, theme, name, icon) values (%(id)s, %(id_bundle)s, %(theme)s, %(name)s, %(icon)s)'.format(
                schema + '.' + databaseTables['cards']
            ), {
                'id': card['uuid'],
                'id_bundle': cursor.fetchall()[0][0],
                'theme': card['theme'],
                'name': card['displayName'],
                'icon': card['icon']
            })
        else:
            database.execute_sql('insert into {} (id, theme, name, icon) values (%(id)s, %(theme)s, %(name)s, %(icon)s)'.format(
                schema + '.' + databaseTables['cards']
            ), {
                'id': card['uuid'],
                'theme': card['theme'],
                'name': card['displayName'],
                'icon': card['icon']
            })


if __name__ == '__main__':
    consumer = Consumer()
    database = Database()

    databaseTables = {
        'buddies': 'buddies',
        'bundles': 'bundle',
        'cards': 'cards',
        'chromas': 'chroma',
        'levels': 'level',
        'skins': 'skins',
        'sprays': 'spray',
        'titles': 'title',
        'weapons': 'weapons',
        'weaponsinfo': 'weaponsinfo',
        'tiers': 'contenttiers'
    }
    schema = 'private'

    print('Iniciando a coleta de dados...')

    info = collectData(consumer)

    print('Dados coletados com sucesso!')

    print('Iniciando o salvamento dos dados...')

    verifyTablesExists(database, databaseTables)
    saveData(database.getDatabase(), databaseTables, schema, info)

    print('Dados salvos com sucesso!')

    print('Finalizando o script...')

    for key, value in info.items():
        with open(f'{key}.json', 'w') as f:
            json.dump(value, f, indent=4)
