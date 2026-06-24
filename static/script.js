// Aether Calculator JavaScript Logic

document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const exprDisplay = document.getElementById('expr-display');
    const resultDisplay = document.getElementById('result-display');
    const displayCard = document.querySelector('.calc-display');
    const keys = document.querySelectorAll('.key');
    
    const historyToggle = document.getElementById('history-toggle');
    const historyPanel = document.getElementById('history-panel');
    const historyList = document.getElementById('history-list');
    const clearHistoryBtn = document.getElementById('clear-history');

    // App State
    let currentExpression = '';
    let isEvaluated = false;
    let history = JSON.parse(localStorage.getItem('calc_history')) || [];

    // Initialize History
    renderHistory();

    // Event Listeners for Keys
    keys.forEach(key => {
        key.addEventListener('click', () => {
            const keyValue = key.getAttribute('data-key');
            handleInput(keyValue);
        });
    });

    // Keyboard Support
    document.addEventListener('keydown', (e) => {
        const keyMap = {
            'Enter': '=',
            '=': '=',
            'Backspace': 'Backspace',
            'Escape': 'Clear',
            'Delete': 'Clear',
            'c': 'Clear',
            'C': 'Clear',
            '+': '+',
            '-': '-',
            '*': '*',
            'x': '*',
            'X': '*',
            '/': '/',
            '^': '^',
            '.': '.',
            '(': '(',
            ')': ')',
            '0': '0',
            '1': '1',
            '2': '2',
            '3': '3',
            '4': '4',
            '5': '5',
            '6': '6',
            '7': '7',
            '8': '8',
            '9': '9'
        };

        if (keyMap[e.key] !== undefined) {
            e.preventDefault(); // Prevent standard browser behaviors
            handleInput(keyMap[e.key]);
        }
    });

    // Core Input Handler
    function handleInput(value) {
        if (value === 'Clear') {
            currentExpression = '';
            isEvaluated = false;
            updateDisplay();
        } else if (value === 'Backspace') {
            if (isEvaluated) {
                // If it was just evaluated, clear it
                currentExpression = '';
                isEvaluated = false;
            } else if (currentExpression.length > 0) {
                currentExpression = currentExpression.slice(0, -1);
            }
            updateDisplay();
        } else if (value === '=') {
            if (currentExpression.trim() === '') return;
            evaluateExpression();
        } else {
            // If it was evaluated, start a new expression or extend the result
            if (isEvaluated) {
                const isOperator = ['+', '-', '*', '/', '^'].includes(value);
                if (isOperator) {
                    // Extend calculation on top of last result
                    currentExpression = resultDisplay.textContent + value;
                } else {
                    // Start new calculation
                    currentExpression = value;
                }
                isEvaluated = false;
            } else {
                currentExpression += value;
            }
            updateDisplay();
        }
    }

    // Update the UI Display
    function updateDisplay() {
        // Clear error style if any
        resultDisplay.classList.remove('error');
        
        // Show expression with human-friendly operators
        let displayExpr = currentExpression
            .replace(/\*/g, ' × ')
            .replace(/\//g, ' ÷ ')
            .replace(/\^/g, ' ^ ');
            
        exprDisplay.textContent = displayExpr || '';
        
        // If we are currently typing, show '0' or active progress as default result
        if (!isEvaluated) {
            resultDisplay.textContent = currentExpression ? ' ' : '0';
        }
        
        // Auto-scroll displays to the right
        exprDisplay.scrollLeft = exprDisplay.scrollWidth;
        resultDisplay.scrollLeft = resultDisplay.scrollWidth;
    }

    // Asynchronous Evaluation via Backend API
    async function evaluateExpression() {
        // Show status loading
        resultDisplay.classList.remove('error');
        resultDisplay.textContent = 'Calculating...';

        try {
            const response = await fetch('/calculate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ expression: currentExpression })
            });

            const data = await response.json();

            if (response.ok) {
                const finalResult = data.result;
                
                // Add to history list
                addToHistory(currentExpression, finalResult);
                
                // Update display state
                resultDisplay.textContent = finalResult;
                isEvaluated = true;
            } else {
                // Backend validation or evaluation error
                handleError(data.error || 'Evaluation failed.');
            }
        } catch (err) {
            // Network or unknown server error
            handleError('Could not connect to Server.');
        }
    }

    // Error Feedback Handler
    function handleError(errorMessage) {
        resultDisplay.classList.add('error');
        resultDisplay.textContent = errorMessage;
        isEvaluated = true; // Set to true so typing a new character starts fresh
        
        // Add screen shake effect
        displayCard.classList.add('shake');
        setTimeout(() => {
            displayCard.classList.remove('shake');
        }, 400);
    }

    // Toggle History Sidebar
    historyToggle.addEventListener('click', () => {
        historyPanel.classList.toggle('collapsed');
    });

    // Clear All History
    clearHistoryBtn.addEventListener('click', () => {
        history = [];
        localStorage.removeItem('calc_history');
        renderHistory();
    });

    // Add Item to History
    function addToHistory(expr, result) {
        // Prevent duplicate consecutive entries
        if (history.length > 0 && history[0].expr === expr) return;

        history.unshift({ expr, result });
        
        // Keep last 50 entries
        if (history.length > 50) {
            history.pop();
        }
        
        localStorage.setItem('calc_history', JSON.stringify(history));
        renderHistory();
    }

    // Render History Items UI
    function renderHistory() {
        historyList.innerHTML = '';
        
        if (history.length === 0) {
            historyList.innerHTML = `
                <div class="empty-history">
                    <i class="fa-solid fa-clock-rotate-left"></i>
                    <p>No history yet</p>
                </div>
            `;
            return;
        }

        history.forEach((item, index) => {
            const historyItem = document.createElement('div');
            historyItem.className = 'history-item';
            
            // Format expression for history view
            const formattedExpr = item.expr
                .replace(/\*/g, ' × ')
                .replace(/\//g, ' ÷ ')
                .replace(/\^/g, ' ^ ');
                
            historyItem.innerHTML = `
                <div class="hist-expr">${formattedExpr}</div>
                <div class="hist-result">${item.result}</div>
            `;
            
            // Click to restore expression
            historyItem.addEventListener('click', () => {
                currentExpression = item.expr;
                isEvaluated = false;
                updateDisplay();
                // Optionally auto focus or scroll back to calculator on mobile
                if (window.innerWidth <= 768) {
                    historyPanel.classList.add('collapsed');
                }
            });
            
            historyList.appendChild(historyItem);
        });
    }
});
