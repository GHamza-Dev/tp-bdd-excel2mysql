Voici un guide pour utiliser le script pour la première fois :

---

## **Guide d'utilisation du script d'importation de données MySQL**

### **Introduction**
Ce script permet d'importer des données depuis un fichier Excel dans une base de données MySQL. Il prend en charge la création de tables dans MySQL en fonction des feuilles de calcul du fichier Excel et permet de réorganiser les colonnes avant l'insertion.

---

### **Prérequis**

Avant d'exécuter le script, assurez-vous d'avoir les éléments suivants :

1. **Python installé** sur votre machine (version recommandée : 3.8 ou supérieure).
2. **MySQL** installé et configuré sur votre machine ou un serveur accessible.
3. **Accès à la base de données MySQL** avec les informations de connexion appropriées.
4. **Fichier Excel** contenant les données à importer, situé dans le répertoire `in/`.

---

### **Étapes d'installation et de configuration**

#### 1. **Cloner ou télécharger le projet**

Clonez ou téléchargez ce projet depuis le dépôt.

```bash
git clone <repository>
```

#### 2. **Configurer MySQL**

1. **Vérifier la configuration de MySQL** : 
   - Si vous souhaitez utiliser une base de données existante ou en créer une nouvelle, assurez-vous que les informations de connexion (hôte, utilisateur, mot de passe, base de données) sont correctement définies dans le fichier `config.py`.

2. **Exécuter le script `init.py` pour créer la base de données de test (facultatif)** :
   Le script `init.py` permet de supprimer une base de données existante et de créer une nouvelle base pour les tests. Exécutez-le avant d'utiliser le script principal.

   ```bash
   python init.py
   ```

#### 3. **Installer les dépendances**

1. Installez les dépendances requises à partir du fichier `requirements.txt` :

   ```bash
   pip install -r requirements.txt
   ```

---

### **Utilisation du script**

#### 1. **Vérifier le fichier Excel**

Assurez-vous que votre fichier Excel (`employes_data.xlsx`) est placé dans le répertoire `in/` et que chaque feuille correspond à une table MySQL à créer ou à mettre à jour.

#### 2. **Exécuter le script principal**

Pour importer les données dans la base de données MySQL, exécutez le script `main.py` :

```bash
python main.py
```

Le script se connectera à la base de données MySQL et lira les données du fichier Excel. Vous devrez fournir l'ordre des colonnes que vous souhaitez lors de l'exécution.

#### 3. **Réorganiser les colonnes (si nécessaire)**

Lorsque le script demande l'ordre des colonnes, entrez la liste d'indices des colonnes dans l'ordre souhaité. Par exemple, pour réorganiser les colonnes en `[2, 0, 1]`, tapez :

```python
[2, 0, 1]
```

Cela permettra de réorganiser les colonnes avant l'insertion dans MySQL.

---

### **Gestion des logs**

Le script génère des logs détaillés dans le fichier `import_log.log` et les affiche également dans la console. Vous pouvez consulter ce fichier pour vérifier l'état de l'importation et résoudre d'éventuels problèmes.