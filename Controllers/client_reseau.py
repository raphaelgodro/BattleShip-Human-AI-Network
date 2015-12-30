# -*- coding: utf-8 -*-

import json
import socket


class Protestation(Exception):
    pass


class ClientReseau(object):
    """Client réseau pour jeu en-ligne.

    :param pseudo: votre pseudonyme.
    :param adversaire: le pseudonyme de l'adversaire que vous désirez affronter, None fera un pairage aléatoire.
    :param serveur: l'adresse ou le nom de l'hôte du serveur de jeu.
    :param port: le port du serveur de jeu.
    """

    def __init__(self, pseudo, *, adversaire=None, serveur="python.gel.ulaval.ca", port=31415):
        self.pseudo = pseudo
        self.adv = adversaire
        self.serveur = serveur
        self.port = port
        self.socket = socket.create_connection((self.serveur, self.port))
        self.tampon = ""
        partie = self.__connecter()
        self.attaque_envoyee = False
        self.rapport_envoyee = False
        if self.adv is None:
            if partie['hote'] == self.pseudo:
                self.adv = partie['adversaire']
            else:
                self.adv = partie['hote']

    def adversaire(self):
        """Retourne le pseudonyme de votre adversaire."""
        return self.adv

    def attaquer(self, cellule=None):
        """Transmet au serveur la cellule de votre attaque. Cette cellule est constituée d'un
        tuple de deux indices compris entre 0 et 9.

        :param cellule: La cellule à attaquer sous la forme d'un tuple de deux indices compris
        entre 0 et 9. Pour vérifier si la réponse de l'adversaire est arriver, il faut mettre l'argument à None.
        :return: La cellule attaquée par votre adversaire si celle-ci est disponible; None autrement.

        Cette fonction retourne None si aucune réponse de votre adversaire n'a été obtenue
        à temps par le serveur de jeu. Dans ce cas, vous devez rappeler la fonction sans argument
        jusqu'à ce vous obteniez une réponse (de préférence, introduire un délai entre les appels).
        """
        assert cellule is None or self.attaque_envoyee == False, ("Vous devez attendre la réponse"
                                                                  "avant d'envoyer une nouvelle"
                                                                  "attaque")
        if cellule is not None:
            requete = {'requête': 'attaquer', 'cellule': cellule}
            self.__envoyer(requete)
            self.attaque_envoyee = True
        reponse = self.__recevoir_async()
        if reponse is not None:
            if not 'cellule' in reponse:
                raise ValueError(
                    'Votre adversaire a renvoyé le message suivant: {}'.format(reponse))
            self.attaque_envoyee = False
            return reponse['cellule']
        else:
            return None

    def rapporter(self, message=None):
        """Rapporte au serveur le message du résultat de la dernière attaque de votre adversaire.

        :param message: la chaîne de caractères de votre rapport.
        :returns: Le rapport de votre adversaire s'il est disponible; None autrement.

        Cette fonction retourne None si aucune réponse de votre adversaire n'a été obtenue
        à temps par le serveur de jeu. Dans ce cas, vous devez rappeler la fonction sans argument
        jusqu'à ce vous obteniez une réponse (de préférence, introduire un délai entre les appels).
        """
        assert message is None or not self.attaque_envoyee, ("Vous devez attendre la réponse"
                                                             " avant d'envoyer un nouveau"
                                                             " rapport")
        if message is not None:
            requete = {"requête": "rapporter", "message": message}
            self.__envoyer(requete)
            self.rapport_envoyee = True

        reponse = self.__recevoir_async()
        if reponse is not None:
            self.rapport_envoyee = False
            return reponse['message']
        else:
            return None

    def protester(self, message):
        """Soulève une exception du type 'Protestation' aux deux joueurs de la partie.
        :param message: Le message de l'exception.
        """
        requete = {'requête': 'protester', 'message': message}
        self.__envoyer(requete)
        self.__recevoir_async()  # On reçoit une copie du message envoyé
        raise Protestation(message)

    def __connecter(self):
        """Communique avec le serveur de jeu pour créer une partie.

        :returns: un dictionnaire contenant une clé 'joueurs' à laquelle
        est associée un tuple de pseudonymes de joueurs.
        """
        requete = {"requête": "créer", "pseudo": self.pseudo, "adversaire": self.adv}

        self.__envoyer(requete)
        return self.__recevoir_sync()

    def __envoyer(self, requete):
        """Envoie une requête au serveur de jeu sous la forme d'une chaîne
        de caractères JSON.
        """
        self.socket.sendall(bytes("\x02" + json.dumps(requete) + "\x03", "utf-8"))

    def __recevoir(self):
        """Reçoit du serveur de jeu une chaîne de caractères et retourne
        un dictionnaire ou None si aucune réponse valide n'a été reçue.
        """
        self.tampon += str(self.socket.recv(4096), "utf-8")
        fin = self.tampon.rfind("\x03")
        debut = self.tampon[:fin].rfind("\x02")

        if debut < 0 or fin < 0:
            return None

        try:
            reponse = json.loads(self.tampon[debut + 1:fin])
        except ValueError:
            raise ValueError("Le serveur nous a répondu un message "
                             "incompréhensible: '{}'".format(self.tampon))
        else:
            self.tampon = self.tampon[fin + 1:]

        if "erreur" in reponse:
            raise Exception(reponse["erreur"])
        if reponse.get('requête') == 'protester':
            raise Protestation(reponse['message'])
        return reponse

    def __recevoir_sync(self):
        """Reçoit un message complet de façon synchrone, c'est-à-dire qu'on
        attend qu'un dictionnaire complet ait pu être décodé avant de quitter
        la fonction.
        """
        ret = None
        while ret is None:
            ret = self.__recevoir()
        return ret

    def __recevoir_async(self):
        """Reçoit un message du serveur de jeu façon asynchrone. Si le
        serveur ne renvoit rien, la fonction retourne simplement None.
        """
        self.socket.setblocking(0)
        try:
            reponse = self.__recevoir()
        except socket.error:
            reponse = None
        self.socket.setblocking(1)
        return reponse
