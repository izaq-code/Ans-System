<template>
  <div class="container1">
    <!-- Cabeçalho dos Gráficos -->
    <div class="cabecalho-graficos">
      <h2>Gráficos</h2>
      <div class="mostrar-todos-crafts">
      </div>
    </div>


    <div id="container-graficos">
      <!-- Gráfico do Último Trimestre -->
      <div class="graficos">
        <canvas id="graficoTrimestre"></canvas>
      </div>

      <!-- Gráfico do Último Ano -->
      <div class="graficos">
        <canvas id="graficoAno"></canvas>
      </div>
    </div>

    <!-- Seção de Busca -->
    <div class="container">
    <div class="cabecalho-historico">
      <i class="bi bi-file-earmark-bar-graph"></i><h1>Buscar</h1>
      <div id="filtro">
        <input class="filtro-input" v-model="termo" placeholder="Digite o registro_ans" />
        <button @click="buscar" class="filtro-botao">Buscar</button>
      </div>
    </div>
    <div class="table-wrapper">
      <table class="tabela-historico">
        <thead>
          <tr class="linha-abaixo">
            <th>Operadora</th>
            <th>Registro</th>
          </tr>
        </thead>
        <tbody>
          <tr class="linha-abaixo" v-for="operadora in operadoras" :key="operadora[0]">
            <td>{{ operadora[1] }}</td>
            <td>{{ operadora[2] }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
  </div>
</template>

<script>
import axios from "axios";
import { Chart, registerables } from "chart.js";

Chart.register(...registerables);

export default {
  data() {
    return {
      termo: "",
      operadoras: [],
      operadorasTrimestre: [],
      operadorasAno: [],
    };
  },
  mounted() {
    // Inicia a busca dos dados e os gráficos
    this.buscarMaioresDespesasTrimestre();
    this.buscarMaioresDespesasAno();
  },
  methods: {
    async buscar() {
      const response = await axios.get(
        `http://localhost:5000/buscar_operadora?termo=${this.termo}`
      );
      this.operadoras = response.data;
    },

    // Função para buscar maiores despesas do último trimestre
    async buscarMaioresDespesasTrimestre() {
      try {
        const response = await axios.get(
          "http://localhost:5000/maiores_despesas_trimestre"
        );
        this.operadorasTrimestre = response.data;
        console.log("Dados do último trimestre:", this.operadorasTrimestre); 
        this.criarGraficoTrimestre();
      } catch (error) {
        console.error(
          "Erro ao buscar maiores despesas do trimestre:",
          error
        );
      }
    },

    // Função para buscar maiores despesas do último ano
    async buscarMaioresDespesasAno() {
      try {
        const response = await axios.get(
          "http://localhost:5000/maiores_despesas_ano"
        );
        this.operadorasAno = response.data;
        console.log("Dados do último ano:", this.operadorasAno); 
        this.criarGraficoAno(); 
      } catch (error) {
        console.error("Erro ao buscar maiores despesas do ano:", error);
      }
    },

    // Função para criar o gráfico de despesas do último trimestre
    criarGraficoTrimestre() {
      if (this.operadorasTrimestre.length === 0) {
        console.warn("Nenhum dado disponível para o gráfico do último trimestre.");
        return;
      }

      const ctx = document.getElementById("graficoTrimestre").getContext("2d");
      new Chart(ctx, {
        type: "bar", 
        data: {
          labels: this.operadorasTrimestre.map((operadora) => operadora[0]), 
          datasets: [
            {
              label: "Despesas do Último Trimestre",
              data: this.operadorasTrimestre.map((operadora) => operadora[1]), 
              backgroundColor: "rgba(54, 162, 235, 0.2)",
              borderColor: "rgba(54, 162, 235, 1)",
              borderWidth: 1,
            },
          ],
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true,
            },
          },
        },
      });
    },

   
    criarGraficoAno() {
      if (this.operadorasAno.length === 0) {
        console.warn("Nenhum dado disponível para o gráfico do último ano.");
        return;
      }

      const ctx = document.getElementById("graficoAno").getContext("2d");
      new Chart(ctx, {
        type: "bar",
        data: {
          labels: this.operadorasAno.map((operadora) => operadora[0]),
          datasets: [
            {
              label: "Despesas do Último Ano",
              data: this.operadorasAno.map((operadora) => operadora[1]), 
              backgroundColor: "rgba(255, 99, 132, 0.2)",
              borderColor: "rgba(255, 99, 132, 1)",
              borderWidth: 1,
            },
          ],
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true,
            },
          },
        },
      });
    },
  },
};
</script>
