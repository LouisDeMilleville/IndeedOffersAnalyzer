# What is Indeed Offers Analyzer ?

It's a tool written in Python and using Selenium, which allows you to search for a wide range of job offers on Indeed and compare each offer with your resume to create a score for each offer. If an offer's score
is equal or higher than the one you defined in the config, you will receive the offer's details and link on Discord using a webhook, so you can apply to it manually.

To make it short, by just starting this tool, you will be able to:
- Search for a large amount of job tiles and get the most recent offers
- Search for offers in differents locations or countries
- Automatically exclude some offers by criterias you can define
- Receive only the job offers which are corresponding to your resume, and gain a lot of time

# How to install it ?

(Please note that this tool has been developped and tested on Ubuntu 24.04. It should still work on other systems like Windows or MacOS since it's a Python program, but you may have to do some adjustements in this case.)

First, clone this repository, open a terminal and move to its folder.

Now, create a virtual environnement to install all the necessary dependancies:
> virtualenv venv
> 
> source venv/bin/activate
> 
> pip3 install -r requirements.txt

Now open the config.py file and change each value:
- API_KEY : You can get one from your openai account.
- WEBHOOK_URL : You can create one on a personnal Discord server.
- MINIMUM : You can keep it at the same value or set it higher or lower depending on if the offers selected with that score are interesting enough for you or not. (0 = lowest interest, 100 = highest interest).
- RESUME : Paste all the textual informations in your resume there. It will be used to evaluate if each offer is interesting or not for you.

Now open the search.txt file and prepare your search links.
For each search you want to add to you bot, go on Indeed and search for jobs, specify the city and other criterias, then paste the link which should now contain all those criterias in the search.txt file, one link by line.

Install chromium or google chrome on your desktop if it's not already installed

# How to use it

Before using it, make sure you followed all the install instructions. It won't work if you missed a step

Open a terminal and type those commands (You can skip this step and use the one you used for install if it's still open):
> cd to/the/folder/of/the/project
>
> source venv/bin/activate
>
> python3 main.py

Now you should see an automated instance of Chromium appear an visit many Indeed links. You can ignore it and do something else, since it will message you trough the Discord webhook link each time it finds an interesting offer.

# Bonus

If you want to add specific conditions in which the AI should deny an offer anyway(for example if the lenght is too short), you just have to edit the prompt on l118 of the main.py file and tell it explicitly.
For example, add "If you detect that the job offer lenght is 1 month or lower, answer with 0"

==============================================================================================================================================

# Qu'est-ce que Indeed Offers Analyzer ?

Il s'agit d'un outil écrit en Python et utilisant Selenium, qui vous permet de rechercher une grande quantité d'offres d'emploi sur Indeed et comparer chaque offre avec votre CV pour créer un score d'"intérêt" à chaque offre. Si le score d'une offre
est égal ou supérieur à celui que vous avez défini dans la configuration, vous reçevrez automatiquement les informations et le lien de l'offre sur Discord via un webhook, ce qui vous permettra d'y répondre manuellement.

Pour la faire courte, juste en lançant cet outil, vous serez en mesure de:
- Chercher une grande quantité d'offres d'emplois et obtenir les plus récentes
- Chercher des offres dans différentes villes ou pays en simultané
- Exclure automatiquement certaines offres par des critères que vous pourrez définir
- Recevoir uniquement les offres vous intéressant réellement et gagner du temps.

# Comment l'installer ?

(Merci de noter que cet outil a été développé et testé sur Ubuntu 24.04. Il devrait fonctionner sur d'autres systèmes comme Windows ou MacOS puisqu'il s'agit d'un programme Python, mais vous aurez peut-être à effectuer quelques ajustements dans ce cas.)

Premièrement, clonez ce dépôt, ouvrez un terminal et déplacez vous dans son dossier

Maintenant, créez un environnement virtuel et installez-y les dépendances nécessaires:
> virtualenv venv
> 
> source venv/bin/activate
> 
> pip3 install -r requirements.txt

Maintenant ouvre le fichier config.py file et modifiez chaque valeur:
- API_KEY : Vous pouvez en obtenir une depuis votre compte openai.
- WEBHOOK_URL : Vous pouvez en créer un sur un serveur Discord personnel.
- MINIMUM : Vous pouvez le laisser à la même valeur, ou bien l'ajuster en fonction de si les offres à partir de ce score vous intéressent beaucoup ou non. (0 = intérêt le plus faible, 100 = intérêt le plus élevé).
- RESUME : Collez toutes les informations textuelles de votre CV ici. Cela sera utilisé pour évaluer si chaque offre vous correspond ou non.

Maintenant ouvrez le fichier search.txt file et préparez vos liens de recherche.
Pour chaque recherche que vous souhaitez ajouter à l'outil, allez sur indeed et recherchez des offres, spécifiez la ville et d'autres critères, puis collez le lien qui devrait désormais contenir tous les crières dans le fichier search.txt, Un lien par ligne.

Installez Chromium ou Chrome sur votre machine si ce n'est pas déjà le cas

# Comment l'utiliser

Avant de l'utiliser, vérifiez que vous avez suivi chaque étape de l'installation. Cela ne marchera pas si vous en loupez une.

Ouvrez un terminal et tapez les commandes suivantes (Vous pouvez passer cette étape si vous avez encore le terminal utilisé pour l):
> cd to/the/folder/of/the/project
>
> source venv/bin/activate
>
> python3 main.py

Maintenant vous devriez voir apparaitre une instance automatisée de Chromium, qui visite de nombreux liens Indeed. Vous pouvez l'ignorer et faire autre chose, puisque l'outil vous enverra automatiquement chaque offre qu'il juge intéressante via le webhook Discord.

# Bonus

Si vous souhaitez ajouter des conditions spécifique pour lesquelles l'IA devra refuser d'office une offre(par exemple si la durée est trop courte), il vous suffit de lui dire tel quel dans le prompt qui lui est envoyé l118 du fichier main.py
Par exemple, rajoutez "If you detect that the job offer lenght is 1 month or lower, answer with 0"
