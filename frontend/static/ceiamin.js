backend = ""
// Para rodar sem a intermediação do nginx, descomente esta linha
//backend = "http://127.0.0.1:8001"
var backend = document.getElementById("backend_url_prefix").value;


app = new Vue({
  el: '#usapalavras',
  data () {
    return {
      palavras: null,
      loading: true,
      errored: false,
      palavra: [],
      novasPalavras: "",
      votoPortugues: parseInt(0),
      votoIngles: parseInt(0),
      palavrasaVotar: []
    }
  },
  mounted () {
    axios
      .get(backend+'/backend/lerpalavras')
      .then(response => {
        this.palavras = response.data.palavras.sort();
        this.listaaVotar()
      })
      .catch(error => {
        console.log(error)
        this.errored = true
      })
      .finally(() => this.loading = false)  
  },
  computed: {
    palavrasUnicas: function () {
      palavrasUnicas = this.novasPalavras.toLowerCase().replace(/\n/gi,' ').replace(/([^a-zà-ü]|-\s)/gi,' ').split(' ').sort()
      
      // Will remove all falsy values: undefined, null, 0, false, NaN and "" (empty string)
      function cleanArray(actual) {
        var newArray = new Array();
        for (var i = 0; i < actual.length; i++) {
          if (actual[i]) {
            newArray.push(actual[i]);
          }
        }
        return newArray;
      }

      palavrasUnicas = cleanArray(palavrasUnicas);
      excluiRepetidas = [...new Set(palavrasUnicas)]
      return excluiRepetidas
    }
  },
  methods: {
    inserirpalavras() {
      axios.post("/backend/inserirpalavra", {
        palavras_unicas: this.palavrasUnicas,
        voto_ingles: this.votoIngles,
        voto_portugues: this.votoPortugues
      })
      .then(response => {
        window.location.reload();
      })
      .catch(console.error)
    },
    apagarpalavra: function(alvo) {
      axios.post("/backend/apagarpalavra", {
        deletepalavra: alvo
      })
      .then(response => {
        window.location.reload();
      })
      .catch(console.error)
    },
    votarpalavras() {
      for (var i=0; i < this.palavrasaVotar.length; i++) {
        axios.post("/backend/votarpalavra", this.palavrasaVotar[i])
        .then(response => {
          window.location.reload();
        })
        .catch(console.error)              
      }
    },
    listaaVotar: function () {
      for (var i=0; i < this.palavras.length; i++) {
        this.palavrasaVotar.push({
          "vocabulo" : this.palavras[i][0],
          "votos" : this.palavras[i][1]+this.palavras[i][2],
          "conhecimento" : Math.max(this.palavras[i][3],this.palavras[i][4])          
        })
      }      
    }
  }
})
