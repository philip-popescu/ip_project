Popescu Philip-Cristian 335CB

Oprea Radu 335CB

Tene Teodora 335CB

<h2>Comenzi rulare flask LOCAL</h2>

    export FLASK_APP=app        // optional
    flask run

Pentru a instal Flask:
    
    apt install python3-flask

<h2>Comenzi GIT</h2>

Pentru a adauga un fisier nou:

    git add <file_name>         // daca fisierul nu este deja urmarit in cadrul repo-ului.

Pentru a trimite modificarile:

    git commit -m "message"
    git push

Pentru a updata:
    
    git stash
    git pull
    git stash pop


<h1>WARNING!!!</h1>

CAND TESTATI IN BROWSER MODIFICARI STERGETI CACHE-UL DEOARECE NU VA DA CERERE LA SERVER PENTRU NOILE DATE, 
CI LE VA RETURNA PE CELE CACHE-UITE!!!


<h1>Detalii utile sprint 1</h1>

Pentru comunicarea paginii cu server se vor folosi metode POST (vezi: https://www.w3schools.com/tags/ref_httpmethods.asp)

Pentru a usura creearea templeturilor puteti utiliza expresii jinja 
(vezi: https://jinja.palletsprojects.com/en/3.1.x/templates/#builtin-tests). Aveti template pt index in care se poate 
observa cum este utilizat acest standard.

De asemenea va rog sa trimiteti pe branch-ul 'sprint_1' toate implementarile.


