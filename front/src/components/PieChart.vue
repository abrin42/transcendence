<template>
    <div>
        <canvas ref="chart"></canvas>
    </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { Chart, DoughnutController, ArcElement, Tooltip } from 'chart.js';

Chart.register(DoughnutController, ArcElement, Tooltip);

const props = defineProps({
    winRate: Number,
    loseRate: Number,
});

const chart = ref(null);

onMounted(() => {
    chart.value = new Chart(chart.value, {
        type: 'doughnut',
        data: {
            labels: ['Win Rate', 'Lose Rate'],
            datasets: [{
                data: [props.winRate, props.loseRate],
                backgroundColor: ['#47a145', '#a14545'],
            }]
        },
        options: {
            responsive: true,
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            return `${context.label}: ${context.raw}%`;
                        }
                    }
                }
            }
        }
    });
});

watch(() => [props.winRate, props.loseRate], (newValues) => {
    chart.value.data.datasets[0].data = newValues;
    chart.value.update();
});
</script>

<style scoped>
canvas {
    max-width: 20vw;
    max-height: 20vh;
}
</style>
