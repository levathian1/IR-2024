# Presentation
Ceci est un repertoire git utilise pour centralise les travaux realises pour un projet de recherche. 
Le contenu de ce repertoire permet a un utilisateur de pouvoir, pour un fichier de donnees d'acquisition GPS et de donnees d'acquisition de vehicule, de pouvoir predire, pour une position donnee et les vitesses prises par le vehicule au paravant, la vitesse suivante ainsi que l'etat de charge de certaines batteries du vehicule

# Organisation des fichiers

functions.py -> les fonctions de traitement des donnees ecrites sont ici et sont alors appelables et utilisables en important ce fichier dans un programme python
not_parser_v2.py -> notre fichier de traitement principal, dependant de functions.py pour fonctionner
write_docs.sh -> ecrit vers un fichier "readme.txt", la documentation des fonctions de functions.py et not_parserv2.py

# Lancement

L'execution de ces fichiers est confirmee sur une machine Ubuntu 22.04 LTS, avec python 3.10 avec les packets python suivants:
```
matplotlib, numpy, pandas, geopy
```
Ces packets sont installables avec un manager de packets python ou via le manager de packet natifs du systeme d'exploitation

Pour lancer le traitement principal:
```
python3 not_parserv2.py donnees_d'acquisition donnees_gps
```
Ces donnees doivent etre de meme format qu'un fichier csv utilisant un/des espaces comme separateur de donnees

Pour obtenir la documentation:
```
./write_docs.sh
```
Cette commande sortira un fichier "readme.txt" dans lequel la documentation des fonctions des divers fichiers y est inscrit. Cette commande ne fonctionnera uniquement sur des systemes avec un environement bash installe. De plus, il peut-etre necessaire sur certains systemes de donner les droits d'execution au fichier afin de pouvoir le lancer

