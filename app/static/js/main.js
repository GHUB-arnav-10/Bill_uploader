document.addEventListener('DOMContentLoaded', function () {
    
    try {
        
        const categoryCtx = document.getElementById('spendByCategoryChart');
        if (categoryCtx && typeof spendByCategoryData !== 'undefined' && Object.keys(spendByCategoryData).length > 0) {
            new Chart(categoryCtx, {
                type: 'doughnut',
                data: {
                    labels: Object.keys(spendByCategoryData),
                    datasets: [{
                        label: 'Spend',
                        data: Object.values(spendByCategoryData),
                        backgroundColor: ['#3b82f6', '#10b981', '#f97316', '#ef4444', '#8b5cf6', '#ec4899', '#f59e0b', '#6b7280'],
                        borderColor: '#ffffff',
                        borderWidth: 2,
                        hoverOffset: 8
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    aspectRatio: 1,
                    plugins: {
                        legend: {
                            position: 'right',
                            labels: { boxWidth: 12, padding: 20, font: { size: 14 } }
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    let label = context.label || '';
                                    if (label) { label += ': '; }
                                    if (context.parsed !== null) {
                                        label += new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(context.parsed);
                                    }
                                    return label;
                                }
                            }
                        }
                    }
                }
            });
        }

        
        const timeCtx = document.getElementById('spendOverTimeChart');
        if (timeCtx && typeof spendOverTimeData !== 'undefined' && Object.keys(spendOverTimeData).length > 0) {
            new Chart(timeCtx, {
                type: 'bar',
                data: {
                    labels: Object.keys(spendOverTimeData),
                    datasets: [{
                        label: 'Monthly Spend',
                        data: Object.values(spendOverTimeData),
                        backgroundColor: 'rgba(59, 130, 246, 0.6)',
                        borderColor: 'rgba(59, 130, 246, 1)',
                        borderWidth: 1,
                        borderRadius: 5
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    aspectRatio: 2.5,
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: { callback: function(value) { return '$' + value.toLocaleString(); } }
                        }
                    },
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    let label = context.dataset.label || '';
                                    if (label) { label += ': '; }
                                    if (context.parsed.y !== null) {
                                        label += new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(context.parsed.y);
                                    }
                                    return label;
                                }
                            }
                        }
                    }
                }
            });
        }
    } catch (error) {
        console.error("Error rendering charts:", error);
    }

    
    
    try {
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
    } catch (error) {
        console.error("Error creating Lucide icons:", error);
    }
});
