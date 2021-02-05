
backend = ""
// Para rodar sem a intermediação do nginx, descomente esta linha
//backend = "http://127.0.0.1:8001"
var backend = document.getElementById("backend_url_prefix").value;



addpalavra = new Vue({
  el: '#adicionapalavras',
  data () {
    return {
      palavras: null,
      loading: true,
      errored: false,
      palavra: [],
      novasPalavras: "",
      votoPortugues: "0",
      votoIngles: "0"
    }
  },
  mounted () {
    axios
      .get(backend+'/backend/lerpalavras')
      .then(response => {
        this.palavras = response.data.palavras
      })
      .catch(error => {
        console.log(error)
        this.errored = true
      })
      .finally(() => this.loading = false)
    },
  computed: {
    palavrasUnicas: function () {
      palavrasUnicas = this.novasPalavras.replace().toLowerCase().split(' ').sort()
      excluiRepetidas = [...new Set(palavrasUnicas)]
      return excluiRepetidas
    },
    votoPortugues: function () {
      return parseInt(this.votoPortugues)
    },
    votoIngles: function () {
      return parseInt(this.votoIngles)
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
    apagarpalavra(palavra) {
      axios.post("/backend/apagarpalavra",palavra)
      .then(response => {
        window.location.reload();
      })
      .catch(console.error)
    }
  }
})

