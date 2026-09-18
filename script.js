// Function to calculate factorial
function factorial(n) {
    if (n === 0 || n === 1) return 1;
    let result = 1;
    for (let i = 2; i <= n; i++) {
        result *= i;
    }
    return result;
}

// Function to calculate Poisson probability P(X = k)
function poissonProbability(lambda, k) {
    return (Math.pow(lambda, k) * Math.exp(-lambda)) / factorial(k);
}

function calculateProbability() {
    const lambda = parseFloat(document.getElementById('lambda').value);
    const threshold = parseInt(document.getElementById('threshold').value);
    const resultDiv = document.getElementById('result');

    if (isNaN(lambda) || isNaN(threshold) || lambda < 0 || threshold < 0) {
        alert("Please enter valid non-negative numbers.");
        return;
    }

    // P(X >= threshold) = 1 - P(X < threshold)
    let probLessThanThreshold = 0;
    for (let i = 0; i < threshold; i++) {
        probLessThanThreshold += poissonProbability(lambda, i);
    }

    const probRequiresAction = 1 - probLessThanThreshold;
    const percentage = (probRequiresAction * 100).toFixed(1);

    let riskClass = 'risk-low';
    let riskText = 'Low Risk';
    
    if (probRequiresAction >= 0.5) {
        riskClass = 'risk-high';
        riskText = 'High Risk';
    } else if (probRequiresAction >= 0.2) {
        riskClass = 'risk-medium';
        riskText = 'Moderate Risk';
    }

    resultDiv.innerHTML = `
        <div class="result-header">Probability of Treatment</div>
        <div class="prob-value">${percentage}<span>%</span></div>
        <div class="risk-level ${riskClass}">
            ${riskText} (≥ ${threshold} sightings)
        </div>
        <div class="result-footer">
            Based on Poisson model (λ = ${lambda})
        </div>
    `;
    
    // Trigger animation
    resultDiv.classList.remove('show');
    // Trigger reflow to restart animation
    void resultDiv.offsetWidth;
    resultDiv.classList.add('show');
}
