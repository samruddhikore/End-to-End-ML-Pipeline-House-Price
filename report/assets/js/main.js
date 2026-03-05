// Chart.js Integration
const chartColors = {
    primary: '#2c3e50',
    secondary: '#3498db',
    accent: '#e74c3c',
    success: '#27ae60',
    warning: '#f39c12',
    lightBlue: '#5dade2',
    lightGreen: '#58d68d',
    lightRed: '#f1948a'
};

// Initialize all charts
function initCharts() {
    const chartElements = document.querySelectorAll('[data-chart]');
    chartElements.forEach(el => {
        const chartType = el.getAttribute('data-chart');
        const chartData = JSON.parse(el.getAttribute('data-chart-data'));
        
        if (window.Chart) {
            createChart(el, chartType, chartData);
        }
    });
}

function createChart(container, type, data) {
    const ctx = container.getContext('2d');
    
    const options = {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
            legend: {
                labels: {
                    font: {
                        size: 12
                    }
                }
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                ticks: {
                    font: {
                        size: 11
                    }
                }
            },
            x: {
                ticks: {
                    font: {
                        size: 11
                    }
                }
            }
        }
    };
    
    new Chart(ctx, {
        type: type,
        data: data,
        options: options
    });
}

// Tab Functionality
function initTabs() {
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tabId = button.getAttribute('data-tab');
            
            // Remove active class from all
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            // Add active class to clicked tab
            button.classList.add('active');
            document.getElementById(tabId).classList.add('active');
        });
    });
    
    // Set first tab as active by default
    if (tabButtons.length > 0) {
        tabButtons[0].classList.add('active');
        tabContents[0].classList.add('active');
    }
}

// Smooth Scroll
function smoothScroll(target) {
    const element = document.querySelector(target);
    if (element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// Number Animation
function animateValue(element, start, end, duration) {
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        const value = Math.floor(progress * (end - start) + start);
        element.textContent = value;
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}

// Initialize on document load
document.addEventListener('DOMContentLoaded', () => {
    initTabs();
    initCharts();
    
    // Animate metric values on scroll
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && entry.target.classList.contains('metric-value')) {
                const targetValue = parseFloat(entry.target.getAttribute('data-value'));
                if (!isNaN(targetValue)) {
                    animateValue(entry.target, 0, targetValue, 1000);
                    observer.unobserve(entry.target);
                }
            }
        });
    });
    
    document.querySelectorAll('.metric-value').forEach(el => {
        observer.observe(el);
    });
});

// Print page function
function printPage() {
    window.print();
}

// Export to PDF (requires html2pdf library)
function exportPDF(filename) {
    const element = document.body;
    const options = {
        margin: 10,
        filename: filename || 'report.pdf',
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2 },
        jsPDF: { orientation: 'portrait', unit: 'mm', format: 'a4' }
    };
    
    if (typeof html2pdf !== 'undefined') {
        html2pdf().set(options).from(element).save();
    } else {
        console.log('html2pdf library not loaded');
    }
}

// Search functionality
function setupSearch() {
    const searchBox = document.getElementById('search-box');
    if (!searchBox) return;
    
    searchBox.addEventListener('input', (e) => {
        const searchTerm = e.target.value.toLowerCase();
        const contentElements = document.querySelectorAll('.content, .card');
        
        contentElements.forEach(el => {
            const text = el.textContent.toLowerCase();
            if (text.includes(searchTerm)) {
                el.style.display = 'block';
            } else {
                el.style.display = 'none';
            }
        });
    });
}

// Initialize search when DOM is ready
document.addEventListener('DOMContentLoaded', setupSearch);
