<template>
  <div class="container">
    <h1>Buscar</h1>
    <!-- Seção de Busca -->
    <div class="buscar">
      <input v-model="termo" placeholder="Digite o nome da operadora" />
      <button @click="buscar">Buscar</button>
    </div>

    <!-- Exibição dos resultados de busca com scroll -->
    <h2>Resultado da Busca</h2>
    <div class="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>Operadora</th>
            <th>Detalhes</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="operadora in operadoras" :key="operadora[0]">
            <td>{{ operadora[1] }}</td>
            <td>{{ operadora[2] }}</td> <!-- Exibindo os dados da operadora -->
          </tr>
        </tbody>
      </table>
    </div>

    <h1>Maiores Despesas</h1>
    <h2>Último Trimestre</h2>
    <div class="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>Operadora</th>
            <th>Valor</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="operadora in operadorasTrimestre" :key="operadora[0]">
            <td>{{ operadora[0] }}</td>
            <td>{{ operadora[1] }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <h2>Último Ano</h2>
    <div class="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>Operadora</th>
            <th>Valor</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="operadora in operadorasAno" :key="operadora[0]">
            <td>{{ operadora[0] }}</td>
            <td>{{ operadora[1] }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  data() {
    return {
      termo: '',
      operadoras: [],
      operadorasTrimestre: [],
      operadorasAno: []
    };
  }, 
  mounted() {
    this.buscarMaioresDespesasTrimestre();
    this.buscarMaioresDespesasAno();
  },
  methods: {
    async buscar() {
      const response = await axios.get(`http://localhost:5000/buscar_operadora?termo=${this.termo}`);
      this.operadoras = response.data;
    },
    async buscarMaioresDespesasTrimestre() {
      try {
        const response = await axios.get('http://localhost:5000/maiores_despesas_trimestre');
        this.operadorasTrimestre = response.data;
      } catch (error) {
        console.error('Erro ao buscar maiores despesas do trimestre:', error);
      }
    },
    async buscarMaioresDespesasAno() {
      try {
        const response = await axios.get('http://localhost:5000/maiores_despesas_ano');
        this.operadorasAno = response.data;
      } catch (error) {
        console.error('Erro ao buscar maiores despesas do ano:', error);
      }
    }
  }
};
</script>

