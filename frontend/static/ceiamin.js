
backend = ""
// Para rodar sem a intermediação do nginx, descomente esta linha
//backend = "http://127.0.0.1:8001"

new Vue({
  el: '#app',
  data () {
    return {
      palavras: null,
      loading: true,
      errored: false
    }
  },
  mounted () {
    axios
      .get(backend+'/backend/palavras')
      .then(response => {
        this.palavras = response.data.palavras
      })
      .catch(error => {
        console.log(error)
        this.errored = true
      })
      .finally(() => this.loading = false)
  }
})