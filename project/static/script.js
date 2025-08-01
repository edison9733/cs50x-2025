
// Handles dynamic functionality and user interactions

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all functionality when DOM is loaded
    // document = entire webpage || addEventListener = listen to smth to happen || DOMContentLoaded=when the page is fully loaded || function()=then do this stuff
    initializeCalorieCalculator();
    initializeWorkoutCalculator();
    initializeCharts();
    initializeFormValidation();
    initializeMotivationalQuotes();
    initializeProgressTracking();
});

// Calorie Calculator for Food Items
function initializeCalorieCalculator() {
    // Find the items where they are displayed
    const foodSelect = document.querySelector('#food_id');
    const quantityInput = document.querySelector('#quantity');
    const nutritionInfo = document.querySelector('#nutrition-info');

    if (foodSelect && quantityInput && nutritionInfo) {
        // Update nutrition info when food or quantity changes
        const updateNutrition = () => {
            const selectedOption = foodSelect.options[foodSelect.selectedIndex];
            if (selectedOption && selectedOption.value) {
                // Convert to number or 0
                const calories = parseFloat(selectedOption.dataset.calories) || 0;
                const carbs = parseFloat(selectedOption.dataset.carbs) || 0;
                const protein = parseFloat(selectedOption.dataset.protein) || 0;
                const fat = parseFloat(selectedOption.dataset.fat) || 0;
                // Default to 100g if not specified
                const servingSize = parseFloat(selectedOption.dataset.servingSize) || 100;
                // Calculate the serving size
                const quantity = parseFloat(quantityInput.value) || 0;
                const multiplier = quantity / servingSize;

                // Update nutrition display
                // Calculate total calories, carbs, protein, fat
                nutritionInfo.innerHTML = `
                    <div class="nutrition-grid">
                        <div class="nutrition-item">
                            <span class="nutrition-value">${(calories * multiplier).toFixed(1)}</span>
                            <span class="nutrition-label">Calories</span>
                        </div>
                        <div class="nutrition-item">
                            <span class="nutrition-value">${(carbs * multiplier).toFixed(1)}g</span>
                            <span class="nutrition-label">Carbs</span>
                        </div>
                        <div class="nutrition-item">
                            <span class="nutrition-value">${(protein * multiplier).toFixed(1)}g</span>
                            <span class="nutrition-label">Protein</span>
                        </div>
                        <div class="nutrition-item">
                            <span class="nutrition-value">${(fat * multiplier).toFixed(1)}g</span>
                            <span class="nutrition-label">Fat</span>
                        </div>
                    </div>
                `;
            }
        };
        // When the user changes food selection, it recalculate nutrition
        foodSelect.addEventListener('change', updateNutrition);
        quantityInput.addEventListener('input', updateNutrition);
    }
}

// Workout Calculator
// same as calories calculator but not so much complicated
function initializeWorkoutCalculator() {
    const workoutSelect = document.querySelector('#workout_id');
    const durationInput = document.querySelector('#duration');
    const caloriesDisplay = document.querySelector('#calories-display');

    if (workoutSelect && durationInput && caloriesDisplay) {
        const calculateCalories = () => {
            const selectedOption = workoutSelect.options[workoutSelect.selectedIndex];
            if (selectedOption && selectedOption.value) {
                const caloriesPerMinute = parseFloat(selectedOption.dataset.caloriesPerMinute) || 0;
                const duration = parseFloat(durationInput.value) || 0;
                const totalCalories = caloriesPerMinute * duration;
                // Display results
                caloriesDisplay.innerHTML = `
                    <div class="calories-burn-display">
                        <h3>${totalCalories.toFixed(1)}</h3>
                        <p>Calories to be burned</p>
                    </div>
                `;

                // Add visual feedback
                // If calories more than 0, there is a an animation effect
                if (totalCalories > 0) {
                    caloriesDisplay.classList.add('pulse');
                    setTimeout(() => caloriesDisplay.classList.remove('pulse'), 1000); // after 1000 milliseconds = 1 second
                }
            }
        };
        // changes the result when the user changes the selections
        workoutSelect.addEventListener('change', calculateCalories);
        durationInput.addEventListener('input', calculateCalories);
    }
}

// Initialize Charts for History Page
function initializeCharts() {
    // Weight/BMI Chart
    const weightChartCanvas = document.querySelector('#weight-chart');
    if (weightChartCanvas && window.Chart) {
        // Get the 2D drawing content
        const ctx = weightChartCanvas.getContext('2d');
        // Get weight data from HTML then convert to Javascript
        const weightData = JSON.parse(weightChartCanvas.dataset.weights || '[]');
        // Get BMI data from HTML and convert to array
        const bmiData = JSON.parse(weightChartCanvas.dataset.bmi || '[]');
        const dates = JSON.parse(weightChartCanvas.dataset.dates || '[]');
        // Create new Chart.js
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: dates,
                datasets: [{
                    label: 'Weight (kg)',
                    data: weightData,
                    borderColor: '#00ff88', // green colour
                    backgroundColor: 'rgba(0, 255, 136, 0.1)', // light green
                    tension: 0.4, // Smooth curved lines
                    yAxisID: 'y' //use left y-axis
                }, {
                    label: 'BMI',
                    data: bmiData,
                    borderColor: '#4ecdc4', // teal color
                    backgroundColor: 'rgba(78, 205, 196, 0.1)', // light teal
                    tension: 0.4,
                    yAxisID: 'y1' //use right y-axis
                }]
            },
            // Create chart options for adjusts to screen size
            options: {
                responsive: true,
                interaction: {
                    mode: 'index',
                    intersect: false,
                },
                // linear scale
                scales: {
                    // show on left side
                    y: {
                        type: 'linear',
                        display: true,
                        position: 'left',
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)' // light grid lines
                        },
                        ticks: {
                            color: '#b0b0b0' // gray text colour
                        }
                    },
                    // show on right side
                    y1: {
                        type: 'linear',
                        display: true,
                        position: 'right',
                        grid: {
                            drawOnChartArea: false, // Dont draw grid lines to avoid clutter
                        },
                        ticks: {
                            color: '#b0b0b0'
                        }
                    },
                    x: {
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        },
                        ticks: {
                            color: '#b0b0b0'
                        }
                    }
                },
                plugins: {
                    legend: {
                        labels: {
                            color: '#ffffff'
                        }
                    }
                }
            }
        });
    }

    // Calorie Chart
    const calorieChartCanvas = document.querySelector('#calorie-chart');
    if (calorieChartCanvas && window.Chart) {
        const ctx = calorieChartCanvas.getContext('2d');
        const consumedData = JSON.parse(calorieChartCanvas.dataset.consumed || '[]');
        const burntData = JSON.parse(calorieChartCanvas.dataset.burnt || '[]');
        const dates = JSON.parse(calorieChartCanvas.dataset.dates || '[]');

        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: dates,
                datasets: [{
                    label: 'Calories Consumed',
                    data: consumedData,
                    backgroundColor: '#ff6b6b',
                }, {
                    label: 'Calories Burnt',
                    data: burntData,
                    backgroundColor: '#00ff88',
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        },
                        ticks: {
                            color: '#b0b0b0'
                        }
                    },
                    x: {
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        },
                        ticks: {
                            color: '#b0b0b0'
                        }
                    }
                },
                plugins: {
                    legend: {
                        labels: {
                            color: '#ffffff'
                        }
                    }
                }
            }
        });
    }
}

// Form Validation
function initializeFormValidation() {
    // Add custom validation to forms
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            // Check if form is valid
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();

                // Add visual feedback
                const invalidInputs = form.querySelectorAll(':invalid');
                invalidInputs.forEach(input => {
                    input.classList.add('is-invalid');

                    // Add error message
                    const errorDiv = document.createElement('div');
                    errorDiv.className = 'invalid-feedback';
                    errorDiv.textContent = input.validationMessage;

                    if (!input.nextElementSibling || !input.nextElementSibling.classList.contains('invalid-feedback')) {
                        input.parentNode.appendChild(errorDiv);
                    }
                });
            }

            form.classList.add('was-validated');
        });

        // Remove error styling when user fixes the input
        const inputs = form.querySelectorAll('input, select');
        inputs.forEach(input => {
            input.addEventListener('input', function() {
                if (input.checkValidity()) {
                    input.classList.remove('is-invalid');
                    const errorDiv = input.nextElementSibling;
                    if (errorDiv && errorDiv.classList.contains('invalid-feedback')) {
                        errorDiv.remove();
                    }
                }
            });
        });
    });
}

// Motivational Quotes
function initializeMotivationalQuotes() {
    const quotes = [
        "The only bad workout is the one that didn't happen.",
        "Your body can stand almost anything. It's your mind that you have to convince.",
        "Success isn't always about greatness. It's about consistency.",
        "Don't stop when you're tired. Stop when you're done.",
        "The pain you feel today will be the strength you feel tomorrow.",
        "A one hour workout is 4% of your day. No excuses.",
        "Strive for progress, not perfection.",
        "The hardest lift of all is lifting your butt off the couch.",
        "Sweat is just fat crying.",
        "You don't have to be great to start, but you have to start to be great."
    ];

    const quoteElement = document.querySelector('#motivational-quote');
    if (quoteElement) {
        // Display random quote
        const randomQuote = quotes[Math.floor(Math.random() * quotes.length)];
        quoteElement.textContent = randomQuote;

        // Change quote every 30 seconds
        setInterval(() => {
            const newQuote = quotes[Math.floor(Math.random() * quotes.length)];
            quoteElement.style.opacity = '0';
            setTimeout(() => {
                quoteElement.textContent = newQuote;
                quoteElement.style.opacity = '1';
            }, 500);
        }, 30000);
    }
}

// Progress Tracking
function initializeProgressTracking() {
    // Update progress bars with animation
    const progressBars = document.querySelectorAll('.progress-bar');
    progressBars.forEach(bar => {
        const targetWidth = bar.style.width;
        bar.style.width = '0%';

        setTimeout(() => {
            bar.style.width = targetWidth;
        }, 100);
    });

    // Add daily goal tracking
    const dailyGoalElement = document.querySelector('#daily-goal-progress');
    if (dailyGoalElement) {
        const consumed = parseFloat(dailyGoalElement.dataset.consumed) || 0;
        const burnt = parseFloat(dailyGoalElement.dataset.burnt) || 0;
        const goal = parseFloat(dailyGoalElement.dataset.goal) || 2000;

        const net = consumed - burnt;
        const percentage = Math.min((net / goal) * 100, 100);

        dailyGoalElement.innerHTML = `
            <div class="progress" style="height: 30px;">
                <div class="progress-bar" role="progressbar"
                     style="width: ${percentage}%;"
                     aria-valuenow="${percentage}"
                     aria-valuemin="0"
                     aria-valuemax="100">
                    ${percentage.toFixed(1)}% of daily goal
                </div>
            </div>
            <p class="text-center mt-2">
                ${net.toFixed(0)} / ${goal} calories
            </p>
        `;
    }
}

// Utility function to format numbers
function formatNumber(num) {
    return new Intl.NumberFormat('en-US').format(num);
}

// Add smooth scrolling
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add loading states
function showLoading(element) {
    element.innerHTML = '<div class="spinner"></div>';
}

function hideLoading(element, content) {
    element.innerHTML = content;
}

// Auto-hide alerts after 5 seconds
const alerts = document.querySelectorAll('.alert');
alerts.forEach(alert => {
    setTimeout(() => {
        alert.style.opacity = '0';
        setTimeout(() => alert.remove(), 500);
    }, 5000);
});
