<!-- Filename: index.tpl
     Authors: Acácia dos Campos da Terra, João Pedro Winckler Bernardi, Matheus
              Henrique Trichez and  Vladimir Belinski
     Description: client side of the application.
-->

<!DOCTYPE html>
<html>
  <head>
    <!--Import Google Icon Font-->
    <link href="http://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <!--Import materialize.css-->
    <link type="text/css" rel="stylesheet" href="static/css/materialize.min.css"  media="screen,projection"/>
    <link type="text/css" rel="stylesheet" href="static/css/chat.css"/>
    <!--Let browser know website is optimized for mobile-->
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>BD distribuído</title>
  </head>

  <body>
    <div class="row">
      <div class="input-field col s12 m12 l12">
        <div class="card">
          <div class="card-image">
            <img src="static/teal.jpg">
          </div>
          <div class="card-content">
            <span class="card-title grey-text text-darken-4">Computação Distribuída 2017.1 - Projeto Final</span>
          </div>
        </div>
      </div>
    </div>
    <div class="row">
      <form class="col s12 m6" action="send" method="post">
        <div class="row">
          <div class="input-field col s12">
      	    <select name="select" id="select" required>
      	      <option value="" disabled selected>Escolha uma opção</option>
      	      <option value="c">Criar/editar variável</option>
      	      <option value="r">Remover variável</option>
      	      <option value="a">Soma variável com variável</option>
      	      <option value="ai">Soma variável com inteiro</option>
      	    </select>
      	    <label>Ação</label>
      	  </div>
        </div>
        <div class="row">
	         <div class="input-field col s12 m6">
              <input name="par1" placeholder="Parâmetro 1" id="par1" type="text" class="validate" required>
              <label for="par1">Parâmetro 1</label>
          </div>
          <div class="input-field col s12 m6">
            <input name="par2" placeholder="Parâmetro 2" id="par2" type="text">
            <label for="par2">Parâmetro 2</label>
          </div>
        </div>
        <div class="row">
          <div class="col offset-s5">
            <button class="btn waves-effect waves-light" type="submit" name="action" style="margin-top: 2em">Enviar
              <i class="material-icons right">send</i>
            </button>
          </div>
        </div>
      </form>
      <div id="chat" class="col s12 m6">
        <div id="inchat">
          <strong>Variáveis do BD:</strong>
          <ul>
           %for k in dados.keys():
          <li><b>{{k}}</b>: {{dados[k]}}</li>
          %end
          </ul>
        </div>
      </div>
    </div>
    <script type="text/javascript" src="https://code.jquery.com/jquery-2.1.1.min.js"></script>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
    <script type="text/javascript" src="static/js/materialize.min.js"></script>
    <!-- To reload only the chat div: using AJAX and realoading every 1000 milliseconds -->
    <script type="text/javascript">
      var auto_refresh = setInterval(function (){ $("#chat").load("/ #inchat"); }, 1000);
    </script>
    <script>
      $(document).ready(function() {
      $('select').material_select();
      });
    </script>
  </body>
</html>
