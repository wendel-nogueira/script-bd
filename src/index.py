import requests
import json


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
                    'displayName': weapon.get('displayName'),
                    'category': weapon.get('shopData').get('category') if weapon.get('shopData') else weapon.get('category'),
                    'displayIcon': weapon.get('displayIcon').replace('displayicon.png', ''),
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
                    skinObj = {
                        'uuid': skin.get('uuid'),
                        'idBundle': '',
                        'idWeapon': weapon.get('uuid'),
                        'displayName': skin.get('displayName'),
                        'tier': skin.get('contentTierUuid'),
                        'theme': skin.get('themeUuid'),
                        'icon': skin.get('displayIcon').replace('displayicon.png', '') if skin.get('displayIcon') else '',
                    }

                    skinsObj.append(skinObj)


                    # Get Theme
                    theme = self.getByUUID(self.resources['themes'], skin.get('themeUuid')).get('data')

                    if (theme != None):
                        skinObj.update({'theme': theme.get('displayName')})


                    # Get Chromas
                    chromasObj = []

                    for chroma in skin.get('chromas'):
                        chromaObj = {
                            'uuid': chroma.get('uuid'),
                            'idSkin': skin.get('uuid'),
                            'displayName': chroma.get('displayName'),
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
                            'displayName': level.get('displayName'),
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
                    'displayName': bundle.get('displayName'),
                    'description': bundle.get('uuid'),
                    'displayIcon': bundle.get('displayIcon').replace('displayicon.png', '')
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
                    'displayName': spray.get('displayName'),
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
                    'displayName': playerTitle.get('displayName'),
                    'titleText': playerTitle.get('titleText'),
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
                    'displayName': playerCard.get('displayName'),
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
                    'displayName': buddy.get('displayName'),
                    'icon': buddy.get('displayIcon').replace('displayicon.png', '') if buddy.get('displayIcon') else '',
                }

                # Get Theme
                if (buddyObj['theme'] != ''):
                    theme = self.getByUUID(self.resources['themes'], buddyObj['theme']).get('data')

                    if (theme != None):
                        buddyObj.update({'theme': theme.get('displayName')})


                buddiesObj.append(buddyObj)

        return buddiesObj


if __name__ == '__main__':
    consumer = Consumer()

    with open('result.json', 'w') as outfile:
        json.dump(consumer.getAllSprays(), outfile, indent=4)