const LABELS = ASTEROID_DATA.map(item => item.name);
const SCORES = ASTEROID_DATA.map(item => item.threat_score);

const CTX    = document.getElementById('threatChart').getContext('2d');
new Chart(CTX, 
    {
        type: 'bar',
        data: {
            labels: LABELS,
            datasets: [{
                label: 'Threat Score',
                data: SCORES,
                backgroundColor: 'rgba(0, 240, 255, 0.4)',
                borderColor: '#00F0FF',
                borderWidth: 1.5,
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    grid: {color: '#1E293B'},
                    ticks: { color: '#64748B' }
                },
                x: {
                    grid: { color: '#1E293B' },
                    ticks: { color: '#64748B' }
                }
            },
            plugins: {
                legend: { 
                    labels: { color: '#F8FAFC' } }
            }
        }
    }
)