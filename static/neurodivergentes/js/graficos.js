document.addEventListener('DOMContentLoaded', function() {
    const graficoContainer = document.getElementById('grafico-container');
    if (!graficoContainer) return;

    const neurodivergente_id = graficoContainer.dataset.neurodivergente;
    
    // Carregar dados do gráfico
    fetch(`/neurodivergentes/grafico/${neurodivergente_id}/`)
        .then(response => response.json())
        .then(data => {
            const grafico = JSON.parse(data.grafico);
            Plotly.newPlot('grafico-container', grafico.data, grafico.layout);
        })
        .catch(error => {
            console.error('Erro ao carregar gráfico:', error);
            graficoContainer.innerHTML = '<p class="error">Erro ao carregar o gráfico. Por favor, tente novamente.</p>';
        });

    // Responsividade
    window.addEventListener('resize', function() {
        Plotly.Plots.resize('grafico-container');
    });
});