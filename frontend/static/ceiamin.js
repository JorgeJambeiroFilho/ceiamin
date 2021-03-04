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
      palavrasaVotar: [ 
        {
          vocabulo: "banana",
          conhecimento:  "0.987654321",
          votos: "2"
        },
        {
          vocabulo: "chocolate",
          conhecimento:  "0.54321",
          votos: "4"
        },
        {
          vocabulo: "incredible",
          conhecimento:  "0.78535023",
          votos: "8"
        }
      ],
      palavrasVotadas: [ 
        {
          vocabulo: "banana",
          votoI: "2",
          votoP: "2"
        },
        {
          vocabulo: "chocolate",
          votoI: "2",
          votoP: "2"
        },
        {
          vocabulo: "incredible",
          votoI: "2",
          votoP: "2"
        }
      ]
    }
  },
  mounted () {
    axios
      .get(backend+'/backend/lerpalavras')
      .then(response => {
        this.palavras = response.data.palavras.sort()
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
      axios.post("/backend/votarpalavra", this.palavrasVotadas)
      .then(response => {
        window.location.reload();
      })
      .catch(console.error)
    }
  }
})
